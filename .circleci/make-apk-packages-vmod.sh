#!/usr/bin/env sh

set -eux

echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_DIRECTORY: $PARAM_DIRECTORY"
echo "PARAM_ARCH: $PARAM_ARCH"
PDIR=/packages/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH

cd "$PARAM_DIRECTORY"

if [ -z "$PARAM_RELEASE" ]; then
    echo "Env variable PARAM_RELEASE is not set! For example PARAM_RELEASE=8, for CentOS 8"
    exit 1
elif [ -z "$PARAM_DIST" ]; then
    echo "Env variable PARAM_DIST is not set! For example PARAM_DIST=centos"
    exit 1
fi

apk add --allow-untrusted /deps/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH/*.apk
apk add -q --no-progress --update tar alpine-sdk sudo


adduser -D builder
echo "builder ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers
addgroup builder abuild
mkdir -p /var/cache/distfiles
chmod -R a+w /var/cache/distfiles

echo "Generate key"
su builder -c "abuild-keygen -nai"

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
