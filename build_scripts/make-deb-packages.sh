#!/usr/bin/env bash

set -eux

source /etc/os-release
source ./pkg.env

export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true

PKG_NAME=$(basename $(pwd))
DEB_ORIG=${VARS[${PKG_NAME}_version]}.orig.tar.gz
if [ "`uname -m`" = "x86_64" ]; then
	ARCH="amd64"
else
	ARCH="arm64"
fi
PDIR="$PDIR/$ID/${VERSION_CODENAME}/${ARCH}"

apt-get update
apt-get install -y \
	-o Acquire::ForceIPv4=true \
	curl \
	apt-utils \
	debhelper \
	devscripts \
	dpkg-dev \
	equivs \
	pkg-config \
	python*-docutils \
	$(test -d /deps && find /deps/ -name '*.deb')
# Create build folder and copy debian folder there
mkdir -p ./pkgbuild
cd pkgbuild

# Save the tarball source file one level up 
curl -L "${VARS[${PKG_NAME}_source]}" -o ../$DEB_ORIG
tar xvfz ../$DEB_ORIG --strip 1

# Update changelog version
if [ "$PKG_NAME" == "varnish" ]; then
	if [ -e .is_weekly ]; then
		WEEKLY='-weekly'
	else
		WEEKLY=
	fi
	VERSION=$(./configure --version | awk 'NR == 1 {print $NF}')$WEEKLY-${package_release}~${VERSION_CODENAME}
	./configure --version
else
	VERSION="$(dpkg -l varnish | awk '$2 == "varnish" {print $3}')"
	dpkg -l varnish
fi

# remove potential debian/ package included in the tarball
rm -rf debian
cat << EOF > ../debian/changelog
${PKG_NAME} (${VERSION}) unstable; urgency=low

  * Changelog not maintained, please see
    https://github.com/varnish/all-packager/releases/tag/v${VERSION%~*}

 -- Varnish Software <opensource@varnish-software.com>
EOF
ls -halt ../debian
cp -Lrf ../debian .

cat debian/changelog
# Install Build-Depends packages
yes | mk-build-deps \
	--tool "apt-get -o Debug::pkgProblemResolver=yes --no-install-recommends -o Acquire::ForceIPv4=true" \
	--install debian/control || true

# Build the packages
dpkg-buildpackage -us -uc -j16

# Prepare the packages for storage
mkdir -p "$PDIR"
mv ../*.deb "$PDIR"

DSC_FILE=$(ls ../*.dsc)
DSC_FILE_WO_EXT=$(basename ${DSC_FILE%.*})
mv $DSC_FILE $PDIR/${DSC_FILE_WO_EXT}_${ARCH}.dsc
