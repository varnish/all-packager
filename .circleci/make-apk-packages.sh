#!/usr/bin/env sh

set -eux

echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_ARCH: $PARAM_ARCH"
PDIR=/packages/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH

cd /workdir
tar xazf alpine.tar.gz --strip 1
apk add -q --no-progress --update tar alpine-sdk sudo


adduser -D builder
echo "builder ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers
addgroup builder abuild
mkdir -p /var/cache/distfiles
chmod -R a+w /var/cache/distfiles

echo "Generate key"
su builder -c "abuild-keygen -nai"

echo "Fix APKBUILD's variables"
tar xavf varnish-*.tar.gz
VERSION=$(varnish-*/configure --version | awk 'NR == 1 {print $NF}')
echo "Version: $VERSION"
sed -i "s/@VERSION@/$VERSION/" APKBUILD
rm -rf varnish-*/

echo "Change the ownership so that abuild is able to write its logs"
chown builder -R .
echo "Fix checksums, build"
su builder -c "abuild checksum"
su builder -c "abuild -r"

echo "Import the packages into the workspace"
mkdir -p $PDIR
mv /home/builder/packages/*/$(uname -m)/*.apk $PDIR

echo "Allow to read the packages by 'circleci' user outside of Docker after 'chown builder -R .' above"
chmod -R a+rwx .
