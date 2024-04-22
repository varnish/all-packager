#!/usr/bin/env bash

set -eux

echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_ARCH: $PARAM_ARCH"
PDIR=/packages/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH

dnf install -y 'dnf-command(config-manager)' || true
yum config-manager --set-enabled powertools || true
yum config-manager --set-enabled crb || true
yum install -y epel-release || true
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
