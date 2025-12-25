# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

Name:    vmod-jq
%global srcversion %(source ../pkg.env && echo ${VARS[%{name}_version]})
Version: %{varnishver}
Release: %(source ../pkg.env && echo ${package_release})%{?dist}
Summary: Use jq programs from VCL

License: BSD-2-Clause
URL:     https://github.com/varnishcache-friends/libvmod-jq
Source:  %(source ../pkg.env && echo ${VARS[%{name}_source]})

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish
BuildRequires: jq-devel

# Build from a git checkout
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: %docutils
BuildRequires: autoconf-archive

Requires: varnish = %varnishver
Requires: jq

%description
TODO: description

%prep
%setup -q -n lib%{name}-%{srcversion}


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
#doc docs AUTHORS CHANGES.md README.md
%license %{_docdir}/vmod-jq/LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*


%changelog
* Mon Dec 01 2025 Varnish Software <opensource@varnish-software.com> - 1.0.0
- This changelog is not in use.
