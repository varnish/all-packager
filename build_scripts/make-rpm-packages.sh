#!/usr/bin/env bash

set -eux

source /etc/os-release
case "$PLATFORM_ID" in
    platform:el8)
        dnf -y install 'dnf-command(config-manager)'
        dnf config-manager --set-enabled powertools
        dnf -y install epel-release
        ;;
    platform:el*)
        dnf -y install 'dnf-command(config-manager)'
        dnf config-manager --set-enabled crb
        dnf -y install epel-release
        ;;
esac

dnf -y install rpm-build dnf-utils

export DIST_DIR=build

cd /varnish-cache
source ./pkg.env
rm -rf $DIST_DIR
mkdir $DIST_DIR


echo "Untar redhat..."
tar xavf redhat.tar.gz -C $DIST_DIR

echo "Untar orig..."
tar xavf varnish-*.tgz -C $DIST_DIR --strip 1

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
        --define "releasetag ${package_release}" \
        --define "srcname $DIST_DIR" \
        --define "nocheck 1" \
        "$@"
}

dnf builddep -y "$DIST_DIR"/redhat/varnish.spec
rpmbuild -bs "$DIST_DIR"/redhat/varnish.spec
rpmbuild --rebuild "$RESULT_DIR"/varnish-*.src.rpm

echo "Prepare the packages for storage..."
mkdir -p $PDIR
mv rpms/*/*.rpm $PDIR
