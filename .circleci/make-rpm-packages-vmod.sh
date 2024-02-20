#!/usr/bin/env bash

set -eux

echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_DIRECTORY: $PARAM_DIRECTORY"
ARCH=`uname -m`
cd "$PARAM_DIRECTORY"

if [ -z "$PARAM_RELEASE" ]; then
    echo "Env variable PARAM_RELEASE is not set! For example PARAM_RELEASE=stream, for CentOS stream"
    exit 1
elif [ -z "$PARAM_DIST" ]; then
    echo "Env variable PARAM_DIST is not set! For example PARAM_DIST=centos"
    exit 1
fi

case "$PARAM_DIST:$PARAM_RELEASE" in
    almalinux:9)
        dnf install -y 'dnf-command(config-manager)'
        yum config-manager --set-enabled crb
        yum install -y epel-release
        ;;
    centos:stream|almalinux:8)
        dnf install -y 'dnf-command(config-manager)'
        yum config-manager --set-enabled powertools
        yum install -y epel-release
        ;;
    centos:7)
        yum install -y epel-release
        ;;
esac

find /deps/ -type f
yum install -y rpm-build yum-utils /deps/$PARAM_DIST/$PARAM_RELEASE/*.rpm

yum-builddep -y *.spec
rpmbuild -bb \
        --define "_smp_mflags -j10" \
	--define "_topdir `pwd`" \
	--undefine=_disable_source_fetch \
	*.spec

echo "Prepare the packages for storage..."
mkdir -p /packages/$PARAM_DIST/$PARAM_RELEASE/
mv RPMS/*/*.rpm /packages/$PARAM_DIST/$PARAM_RELEASE/
