#!/bin/sh

set -eux

if apt-get -v; then
	export DEBIAN_FRONTEND=noninteractive
	export DEBCONF_NONINTERACTIVE_SEEN=true
	apt-get update
	apt-get install -y ./*deb
else
	dnf install -y 'dnf-command(config-manager)' || true
	yum config-manager --set-enabled powertools || true
	yum config-manager --set-enabled crb || true
	yum install -y epel-release || true
	yum install -y redhat-rpm-config || true
	yum install -y ./*.rpm
fi

varnishtest build_scripts/main.vtc
