#!/usr/bin/env bash

set -eux

echo "PARAM_RELEASE: $PARAM_RELEASE"
echo "PARAM_DIST: $PARAM_DIST"
echo "PARAM_ARCH: $PARAM_ARCH"
PDIR=/packages/$PARAM_DIST/$PARAM_RELEASE/$PARAM_ARCH

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
esac

yum install -y rpm-build yum-utils

export DIST_DIR=build

cd /workdir
rm -rf $DIST_DIR
mkdir $DIST_DIR


echo "Untar redhat..."
tar xavf redhat.tar.gz -C $DIST_DIR

echo "Untar orig..."
tar xavf varnish-*.tar.gz -C $DIST_DIR --strip 1

echo "Build Packages..."
if [ -e .is_weekly ]; then
    WEEKLY='.weekly'
else
    WEEKLY=
fi
VERSION=$("$DIST_DIR"/configure --version | awk 'NR == 1 {print $NF}')$WEEKLY

cp -r -L "$DIST_DIR"/redhat/* "$DIST_DIR"/
tar zcf "$DIST_DIR.tgz" --exclude "$DIST_DIR/redhat" "$DIST_DIR"/

RPMVERSION="$VERSION"

RESULT_DIR="rpms"
CUR_DIR="$(pwd)"

rpmbuild() {
    command rpmbuild \
        --define "_smp_mflags -j10" \
        --define "_sourcedir $CUR_DIR" \
        --define "_srcrpmdir $CUR_DIR/${RESULT_DIR}" \
        --define "_rpmdir $CUR_DIR/${RESULT_DIR}" \
        --define "versiontag ${RPMVERSION}" \
        --define "releasetag 1" \
        --define "srcname $DIST_DIR" \
        --define "nocheck 1" \
        "$@"
}

yum-builddep -y "$DIST_DIR"/redhat/varnish.spec
rpmbuild -bs "$DIST_DIR"/redhat/varnish.spec
rpmbuild --rebuild "$RESULT_DIR"/varnish-*.src.rpm

echo "Prepare the packages for storage..."
mkdir -p $PDIR
mv rpms/*/*.rpm $PDIR
