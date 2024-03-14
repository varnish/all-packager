#!/usr/bin/env bash

set -eux

export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true
echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_ARCH: $PARAM_ARCH"
PDIR=/packages/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH

apt-get update
apt-get install -y dpkg-dev debhelper devscripts equivs pkg-config apt-utils fakeroot

# Ubuntu 20.04 aarch64 fails when using fakeroot-sysv with:
#    semop(1): encountered an error: Function not implemented
update-alternatives --set fakeroot /usr/bin/fakeroot-tcp

mkdir /workdir/varnish
cd /workdir/varnish 

echo "Untar debian..."
cp -a ../varnish-debian debian

echo "Untar orig..."
tar xavf ../src-tarballs/varnish/*.tar.gz --strip 1

# we need varnish first so we know which version to use everywhere
VERSION=$(./configure --version | awk 'NR == 1 {print $NF}')-1~$PARAM_RELEASE
sed -i -e "s|@VERSION@|$VERSION|"  "debian/changelog"

echo "Install Build-Depends packages..."
yes | mk-build-deps --install debian/control || true

echo "Build the packages..."
dpkg-buildpackage -us -uc -j16

echo "Prepare the packages for storage..."

cd /workdir/
mkdir -p $PDIR
mv *.deb *.dsc $PDIR
