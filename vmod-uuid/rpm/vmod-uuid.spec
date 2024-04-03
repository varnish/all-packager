# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

Name:    @NAME@
Version: @VERSION@
Release: 1%{?dist}
Summary: @DESC@

License: BSD-2-Clause
URL:     @URL@
Source:  @DOWNLOAD_URL@

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
@LONG_DESC@


%prep
%setup -q -n @UNTAR_DIR@


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
* @CHANGELOG_DATE@ @MAINTAINER@ - @VERSION@-1
- This changelog is not in use.
