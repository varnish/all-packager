#!/usr/bin/env bash

set -eux

export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true
apt-get update
apt-get install -y dpkg-dev debhelper devscripts equivs pkg-config apt-utils fakeroot

# Ubuntu 20.04 aarch64 fails when using fakeroot-sysv with:
#    semop(1): encountered an error: Function not implemented
update-alternatives --set fakeroot /usr/bin/fakeroot-tcp

cd /varnish-cache
ls -la

echo "Untar debian..."
tar xavf debian.tar.gz

echo "Untar orig..."
tar xavf varnish-*.tgz --strip 1

echo "Update changelog version..."
if [ -e .is_weekly ]; then
    WEEKLY='-weekly'
else
    WEEKLY=
fi
source /etc/os-release
VERSION=$(./configure --version | awk 'NR == 1 {print $NF}')$WEEKLY-1~$VERSION_CODENAME
sed -i -e "s|@VERSION@|$VERSION|"  "debian/changelog"

echo "Install Build-Depends packages..."
yes | mk-build-deps --install debian/control || true

echo "Build the packages..."
dpkg-buildpackage -us -uc -j16

echo "Prepare the packages for storage..."
mkdir -p $PDIR
mv ../*.deb $PDIR

if [ "`uname -m`" = "x86_64" ]; then
  ARCH="amd64"
else
  ARCH="arm64"
fi

DSC_FILE=$(ls ../*.dsc)
DSC_FILE_WO_EXT=$(basename ${DSC_FILE%.*})
mv $DSC_FILE $PDIR/${DSC_FILE_WO_EXT}_${ARCH}.dsc
