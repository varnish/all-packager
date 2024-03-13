#!/bin/bash

set -eux

if apk -v; then
	apk add --allow-untrusted $PDIR/*.apk
elif apt-get -v; then
	apt-get install -y $PDIR/*.deb
else
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
import vsthrottle:
import xkey;

backend
EOF

varnishd -C -f /tmp/test.vcl
