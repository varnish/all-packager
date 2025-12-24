# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

Name:    vmod-cfg
%global srcversion %(source ../pkg.env && echo ${VARS[%{name}_version]})
Version: %{varnishver}
Release: %(source ../pkg.env && echo ${package_release})%{?dist}
Summary: Config VMOD for Varnish

License: BSD-2-Clause
URL:     https://github.com/carlosabalde/libvmod-cfg
Source:  %(source ../pkg.env && echo ${VARS[%{name}_source]})

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish
BuildRequires: libcurl-devel
BuildRequires: luajit-devel
BuildRequires: jemalloc-devel
BuildRequires: vim-common
BuildRequires: python3-docutils

# Build from a git checkout
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: %docutils
BuildRequires: autoconf-archive

Requires: varnish = %varnishver
Requires: libcurl
Requires: luajit


%description
This is a collection of modules ("vmods") extending Varnish VCL used
for describing HTTP request/response policies with additional
capabilities. This collection contains the following vmods:
bodyaccess, header, saintmode, tcp, var, vsthrottle, xkey


%prep
%setup -q -n lib%{name}-%{srcversion}


%build
#sh bootstrap
export RST2MAN=%{rst2man}
./autogen.sh
%configure --disable-flush-jemalloc-tcache
%make_build


%install
%make_install
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'

# TODO fix for failing test on arm

%check
%ifarch %ix86 ppc
# 64-bit specific test
sed -i 's,tests/xkey/test12.vtc,,' src/Makefile
%make_build check VERBOSE=1
%endif


%files
#doc docs AUTHORS CHANGES.rst COPYING README.rst
%{_libdir}/varnish/vmods/*
%{_docdir}/*
%{_mandir}/man3/*.3*


%changelog
* Thu Jan 01 1970 Varnish Software <opensource@varnish-software.com> - 1.0.0
- This changelog is not in use.
