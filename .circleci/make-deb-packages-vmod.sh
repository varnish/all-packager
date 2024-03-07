#!/usr/bin/env bash

set -eux

export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true

echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_DIRECTORY: $PARAM_DIRECTORY"
ARCH=`uname -m`
# FIXME: we should just pass the right directory
cd $(dirname "$PARAM_DIRECTORY")

if [ "`uname -m`" = "x86_64" ]; then
  ARCH="amd64"
else
  ARCH="arm64"
fi

if [ -z "$PARAM_RELEASE" ]; then
    echo "Env variable PARAM_RELEASE is not set! For example PARAM_RELEASE=focal for Ubuntu 20.04"
    exit 1
elif [ -z "$PARAM_DIST" ]; then
    echo "Env variable PARAM_DIST is not set! For example PARAM_DIST=debian"
    exit 1
fi

apt-get update
apt-get install -y dpkg-dev debhelper devscripts equivs pkg-config apt-utils fakeroot /deps/$PARAM_DIST/$PARAM_RELEASE/*.deb
apt-get install -y python*-docutils

VVERSION="$(dpkg -l | awk '$2 == "varnish" {print $3}')"
PVERSION="$(cat debian/orig_url | sed 's/^.*v\(.*\)\.t.*/\1/' | sed 's/-.*//')"
DEB_ORIG=$(grep Source debian/control | awk -F' ' '{print $2}')_${PVERSION}.orig.tar.gz

sed -i "s/@VVERSION@/$VVERSION/" debian/*

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
curl -L "$(cat ../../debian/orig_url)" -o ../$DEB_ORIG 
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
mkdir -p /packages/$PARAM_DIST/$PARAM_RELEASE/
mv *.deb /packages/$PARAM_DIST/$PARAM_RELEASE/

DSC_FILE=$(ls *.dsc)
DSC_FILE_WO_EXT=$(basename ${DSC_FILE%.*})
mv $DSC_FILE /packages/$PARAM_DIST/$PARAM_RELEASE/${DSC_FILE_WO_EXT}_${ARCH}.dsc
