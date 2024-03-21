#!/usr/bin/env bash

set -eux

export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true

echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_DIRECTORY: $PARAM_DIRECTORY"
echo "PARAM_ARCH: $PARAM_ARCH"

PDIR=/packages/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH
# FIXME: we should just pass the right directory
cd $(dirname "$PARAM_DIRECTORY")

apt-get update
apt-get install -y dpkg-dev debhelper devscripts equivs pkg-config apt-utils fakeroot /deps/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH/*.deb
apt-get install -y python*-docutils

VVERSION="$(dpkg -l | awk '$2 == "varnish" {print $3}')"
PVERSION="$(cat debian/orig_url | grep -v '^#' | sed 's/^\(.*\)::.*/\1/' | sed 's/-.*//')"
DEB_ORIG=$(grep Source debian/control | awk -F' ' '{print $2}')_${PVERSION}.orig.tar.gz

sed -i "s/@VVERSION@/$VVERSION/" debian/*
sed -i "s/@PVERSION@/$PVERSION/" debian/*

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
curl -L "$(cat ../../debian/orig_url | grep -v '^#' | sed 's/^\(.*\)::\(.*\)/\2/' )" -o ../$DEB_ORIG 
tar xvfz ../$DEB_ORIG --strip 1

cp -r ../../debian .

# If format file does not exist, assume Version 1 is used.
#
if [ ! -f debian/source/format ]; then
  if [ ! -d debian/source ]; then
    mkdir -p debian/source
  fi
  echo "1.0" >  debian/source/format
fi

echo "Build the packages..."
dpkg-buildpackage -us -uc -j16

cd ..
mkdir -p $PDIR
mv *.deb *.dsc $PDIR
