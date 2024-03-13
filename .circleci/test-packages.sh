#!/bin/sh

set -eux

if apk -V; then
	apk add --allow-untrusted $PDIR/*.apk
elif apt-get -v; then
	apt-get update
	apt-get install -y $PDIR/*.deb
else
	dnf install -y 'dnf-command(config-manager)'
	yum config-manager --set-enabled powertools || yum config-manager --set-enabled crb                
	yum install -y epel-release
	yum install -y $PDIR/*.rpm
fi

cat > /tmp/test.vcl << EOF
vcl 4.1;

import uuid;

import querystring;

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
EOF

varnishd -C -f /tmp/test.vcl