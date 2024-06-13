#!/usr/bin/env bash

set -eux

source ./pkg.env
PKG_NAME=$(basename $(pwd))

export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true
echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_ARCH: $PARAM_ARCH"
PDIR=/packages/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH

find  /deps/ -type f
apt-get update
apt-get install -y dpkg-dev debhelper devscripts equivs pkg-config apt-utils fakeroot $(find /deps/ -name '*.deb')
apt-get install -y python*-docutils

VERSION="$(dpkg -l varnish | awk '$2 == "varnish" {print $3}')"
DEB_ORIG=${VARS[${PKG_NAME}_version]}.orig.tar.gz

sed -i -e "s/@VERSION@/$VERSION/" debian/*

# Ubuntu 20.04 aarch64 fails when using fakeroot-sysv with:
#    semop(1): encountered an error: Function not implemented
update-alternatives --set fakeroot /usr/bin/fakeroot-tcp

echo "Install Build-Depends packages..."
yes | mk-build-deps --install debian/control || true

# Create build folder and copy debian folder there
# needed for format v3.0
mkdir -p ./pkgbuild/distdir/
cd pkgbuild/distdir/

# Save the tarball source file one level up, 
# needed for format v3.0
curl -L "${VARS[${PKG_NAME}_source]}" -o ../$DEB_ORIG
tar xvfz ../$DEB_ORIG --strip 1
# remove potential debian/ package included in the tarball
rm -rf debian

cp -r ../../debian .

echo "Build the packages..."
dpkg-buildpackage -us -uc -j16

cd ..
mkdir -p $PDIR
mv *.deb *.dsc $PDIR
