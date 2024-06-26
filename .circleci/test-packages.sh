#!/bin/sh

set -eux

if apk -V; then
	## Needed for VMOD-Digest
	apk add libmhash-dev --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing/
	##
	apk add --allow-untrusted $PDIR/*.apk
elif apt-get -v; then
	export DEBIAN_FRONTEND=noninteractive
	export DEBCONF_NONINTERACTIVE_SEEN=true
	apt-get update
	apt-get install -y $PDIR/*.deb
else
	dnf install -y 'dnf-command(config-manager)' || true
	yum config-manager --set-enabled powertools || true
	yum config-manager --set-enabled crb || true
	yum install -y epel-release || true
	yum install -y redhat-rpm-config || true
	yum install -y $PDIR/*.rpm
fi

cat > /tmp/test.vcl << EOF
vcl 4.1;

import digest;
import fileserver;
import jq;
import querystring;
import redis;
import reqwest;
import rers;
import uuid;
import geoip2;

# varnish-modules
import accept;
import bodyaccess;
import header;
import saintmode;
import str;
import tcp;
import var;
import vsthrottle;
import xkey;

backend default none;

sub vcl_init {
	new re_cache = rers.init(100);
}
EOF

varnishd -C -f /tmp/test.vcl

if [ ! grep 'DISTRIB_CODENAME=focal' /etc/lsb-release ]; then
	varnishlog-json -h
fi
