# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

Name:    vmod-uuid
Version: %{varnishver}.0
%global version 1.10
Release: 1%{?dist}
Summary: Generate UUIDs in VCL

License: BSD-2-Clause
URL:     https://github.com/otto-de/libvmod-uuid
Source:  https://github.com/otto-de/libvmod-uuid/archive/refs/tags/v%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish
BuildRequires: uuid-devel

# Build from a git checkout
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: %docutils
BuildRequires: autoconf-archive

Requires: varnish = %varnishver
Requires: uuid

%description
This is a collection of modules ("vmods") extending Varnish VCL used
for describing HTTP request/response policies with additional
capabilities. This collection contains the following vmods:
bodyaccess, header, saintmode, tcp, var, vsthrottle, xkey


%prep
%setup -q -n lib%{name}-%{version}


%build
#sh bootstrap
export RST2MAN=%{rst2man}
./autogen.sh
%configure 
%make_build


%install
%make_install docdir=%_pkgdocdir
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'


%check
%ifarch %ix86 %arm ppc
# 64-bit specific test
sed -i 's,tests/xkey/test12.vtc,,' src/Makefile
%endif
%make_build check VERBOSE=1


%files
#doc docs AUTHORS CHANGES.rst COPYING README.rst
%doc COPYING README.rst
%license LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*


%changelog
* Thu Jul 24 2014 Varnish Software <opensource@varnish-software.com> - 3.0.0-1
- This changelog is not in use.
