# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

%global docutils python3-docutils
%global rst2man rst2man

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

Name:    varnish-modules
Version: %{varnishver}.0
%global version 0.24.0
Release: 1%{?dist}
Summary: A collection of modules ("vmods") extending Varnish VCL

License: BSD-2-Clause
URL:     https://github.com/varnish/varnish-modules
Source:  https://github.com/varnish/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish

# Build from a git checkout
#BuildRequires: automake
#BuildRequires: autoconf
#BuildRequires: libtool
BuildRequires: %docutils

Requires: varnish = %varnishver

Provides: vmod(accept)%{_isa} = %{version}-%{release}
Provides: vmod(bodyaccess)%{_isa} = %{version}-%{release}
Provides: vmod(header)%{_isa} = %{version}-%{release}
Provides: vmod(saintmode)%{_isa} = %{version}-%{release}
Provides: vmod(tcp)%{_isa} = %{version}-%{release}
Provides: vmod(var)%{_isa} = %{version}-%{release}
Provides: vmod(vsthrottle)%{_isa} = %{version}-%{release}
Provides: vmod(xkey)%{_isa} = %{version}-%{release}
Provides: vmod(str)%{_isa} = %{version}-%{release}

%description
This is a collection of modules ("vmods") extending Varnish VCL used
for describing HTTP request/response policies with additional
capabilities. This collection contains the following vmods:
bodyaccess, header, saintmode, tcp, var, vsthrottle, xkey


%prep
%autosetup -n %{name}-%{version}


%build
#sh bootstrap
export RST2MAN=%{rst2man}
%configure 
%make_build


%install
%make_install docdir=%_pkgdocdir
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'
rm %{buildroot}%{_pkgdocdir}/LICENSE # Rather use license macro


%check
%ifarch %ix86 %arm ppc
# 64-bit specific test
sed -i 's,tests/xkey/test12.vtc,,' src/Makefile
%endif
%make_build check VERBOSE=1


%files
#doc docs AUTHORS CHANGES.rst COPYING README.rst
%doc AUTHORS CHANGES.rst COPYING README.md
%license LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*


%changelog
* Thu Jul 24 2014 Varnish Software <opensource@varnish-software.com> - 3.0.0-1
- This changelog is not in use.
