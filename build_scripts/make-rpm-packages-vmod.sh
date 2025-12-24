#!/usr/bin/env bash

set -eux

cd redhat

dnf install -y 'dnf-command(config-manager)' || true
yum config-manager --set-enabled powertools || true
yum config-manager --set-enabled crb || true
yum install -y epel-release || true
yum install -y make findutils

yum install -y rpm-build yum-utils $(find /deps/ -name '*.rpm')

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
