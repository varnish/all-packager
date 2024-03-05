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
apt-get install -y dpkg-dev debhelper devscripts equivs pkg-config apt-utils fakeroot docutils-common python3-docutils python3-roman sgml-base xml-core /deps/$PARAM_DIST/$PARAM_RELEASE/*.deb
VVERSION="$(dpkg -l | awk '$2 == "varnish" {print $3}' | sed 's/-.*//' )"
sed -i "s/@VVERSION@/$VVERSION/" debian/*
curl -L "$(cat debian/orig_url)" -o ../$(cat debian/orig_packagename) 

tar xvfz ../$(cat debian/orig_packagename) --strip 1

# Ubuntu 20.04 aarch64 fails when using fakeroot-sysv with:
#    semop(1): encountered an error: Function not implemented
update-alternatives --set fakeroot /usr/bin/fakeroot-tcp

#echo "Install Build-Depends packages..."
#yes | mk-build-deps --install debian/control || true

echo "Build the packages..."
dpkg-buildpackage -us -uc -j16

cd ..
mkdir -p /packages/$PARAM_DIST/$PARAM_RELEASE/
mv *.deb /packages/$PARAM_DIST/$PARAM_RELEASE/

DSC_FILE=$(ls *.dsc)
DSC_FILE_WO_EXT=$(basename ${DSC_FILE%.*})
mv $DSC_FILE /packages/$PARAM_DIST/$PARAM_RELEASE/${DSC_FILE_WO_EXT}_${ARCH}.dsc
