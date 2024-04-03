#!/usr/bin/env bash

set -eux

echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_DIRECTORY: $PARAM_DIRECTORY"
echo "PARAM_ARCH: $PARAM_ARCH"
PDIR=/packages/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH

cd "$PARAM_DIRECTORY"

## Source the configurations from conf file
source ../conf

dnf install -y 'dnf-command(config-manager)' || true
yum config-manager --set-enabled powertools || true
yum config-manager --set-enabled crb || true
yum install -y epel-release || true
yum install -y make

find /deps/ -type f
yum install -y rpm-build yum-utils /deps/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH/*.rpm

VVERSION="$(rpm -qa varnish | awk -F'-' '{print $2}')"
LONG_DESC=$(echo "${LONG_DESC}" | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/\\n/g' )

sed -i -e "s#@VVERSION@#$VVERSION#g" \
    -e "s#@NAME@#$NAME#g" \
    -e "s#@VERSION@#$VERSION#g" \
    -e "s#@DESC@#$DESC#g" \
    -e "s#@LONG_DESC@#$LONG_DESC#g" \
    -e "s#@URL@#$URL#g" \
    -e "s#@DOWNLOAD_URL@#$DOWNLOAD_URL#g" \
    -e "s#@UNTAR_DIR@#$UNTAR_DIR#g" \
    -e "s#@MAINTAINER@#$MAINTAINER#g" \
    -e "s#@CHANGELOG_DATE@#$CHANGELOG_DATE#g" \
    *

mkdir SOURCES
yum-builddep -y *.spec
rpmbuild -bb \
        --define "_smp_mflags -j10" \
	--define "_topdir `pwd`" \
	--undefine=_disable_source_fetch \
	*.spec

echo "Prepare the packages for storage..."
mkdir -p $PDIR
mv RPMS/*/*.rpm $PDIR
