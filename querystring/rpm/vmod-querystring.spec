# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

Name:    vmod-querystring
Version: 2.0.3
Release: 1%{?dist}
Summary: A fine-grained control over a URL's query-string in Varnish Cache

License: BSD-2-Clause
URL:     https://github.com/Dridi/libvmod-querystring
Source:  https://github.com/Dridi/libvmod-querystring/archive/refs/tags/v%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish

# Build from a git checkout
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: %docutils
BuildRequires: autoconf-archive

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
The purpose of this module is to give you a fine-grained 
control over a URL's query-string in Varnish Cache. It's 
possible to remove the query-string, clean it, sort its 
parameters or filter it to only keep a subset of them.


%prep
%autosetup
#%setup -q -n lib%{name}-%{version}


%build
sh bootstrap
export RST2MAN=%{rst2man}
%configure 
%make_build


%install
%make_install docdir=%_pkgdocdir
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'


%check
%make_build check VERBOSE=1


%files
#doc docs AUTHORS CHANGES.rst COPYING README.rst
%doc COPYING README.rst
%license LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*


%changelog
* Thu Nov 2 2021 Dridi v{version}
- Support for the VCL REGEX type when available
- Varnish 6.6 support
- Varnish 7.0 support
