#!/usr/bin/env bash

set -eux

echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_DIRECTORY: $PARAM_DIRECTORY"
echo "PARAM_ARCH: $PARAM_ARCH"
PDIR=/packages/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH

cd "$PARAM_DIRECTORY"

dnf install -y 'dnf-command(config-manager)'
yum config-manager --set-enabled powertools || yum config-manager --set-enabled crb
yum install -y epel-release
yum install -y make

find /deps/ -type f
yum install -y rpm-build yum-utils /deps/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH/*.rpm

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
