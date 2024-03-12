#!/usr/bin/env bash

set -eux

export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true
apt-get update
apt-get install -y dpkg-dev debhelper devscripts equivs pkg-config apt-utils fakeroot

echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_ARCH: $PARAM_ARCH"
PDIR=/packages/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH

# Ubuntu 20.04 aarch64 fails when using fakeroot-sysv with:
#    semop(1): encountered an error: Function not implemented
update-alternatives --set fakeroot /usr/bin/fakeroot-tcp

for component in varnish; do

	mkdir /workdir/$component
	cd /workdir/$component 

	echo "Untar debian..."
	cp -a ../$component-debian debian

	echo "Untar orig..."
	tar xavf ../src-tarballs/$component/*.tar.gz --strip 1

	# we need varnish first so we know which version to use everywhere
	if [ "$component" = "varnish" ]; then
		VERSION=$(./configure --version | awk 'NR == 1 {print $NF}')-1~$PARAM_RELEASE
	elif [ -z "$VERSION" ]; then
		echo "varnish should have given us a VERSION to work with by now"
		exit 1
	fi

	sed -i -e "s|@VERSION@|$VERSION|"  "debian/changelog"

	echo "Install Build-Depends packages..."
	yes | mk-build-deps --install debian/control || true

	echo "Build the packages..."
	dpkg-buildpackage -us -uc -j16

	echo "Prepare the packages for storage..."
done

cd /workdir/
mkdir -p $PDIR
mv *.deb *.dsc $PDIR
