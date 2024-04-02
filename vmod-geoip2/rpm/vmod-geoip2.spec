# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

%global srccommit 976c551b5584034dde80ac30f8baa07f1bc92834

Name:           libvmod-geoip2
Version: %{varnishver}.0
%global version 1.3.0
Release:        1%{?dist}
Group:          System Environment/Libraries
Summary:        A Varnish 6.0, 7.3 and 7.4 VMOD to query MaxMind GeoIP2 DB files.
URL:            https://github.com/varnish/libvmod-geoip2
License:        GPLv2
Source:         https://github.com/varnishcache-friends/libvmod-geoip2/archive/%{srccommit}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: varnish
BuildRequires: libmaxminddb
BuildRequires: libmaxminddb-devel

# Build from a git checkout
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: %docutils
BuildRequires: autoconf-archive

BuildRequires:  pkgconfig(varnishapi) >= 6

# varnish-devel may not require Python or Varnish as it should
BuildRequires:  varnish >= 6.0.6
BuildRequires:  python(abi) >= 3.4

Requires:       varnish >= %(varnishd -V 2>&1 | awk -F '[- ]' '{print $3; exit}')


%description
A Varnish master VMOD to query MaxMind GeoIP2 DB files.


%prep
%setup -q -n %{name}-%{srccommit}

%build
export RST2MAN=%{rst2man}
./autogen.sh
%configure CFLAGS="%{optflags}"
%make_build


%install
%make_install
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'


%check
%make_build check VERBOSE=1


%files
%{_mandir}/man?/*
%{_docdir}/*
%{_libdir}/*/vmods/*.so


%changelog
* Tue May 30 2023 Federico G. Schwindt <fgsch@lodoss.net> - @VERSION@-1
- Changelog not maintained
