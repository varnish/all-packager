Name:    vmod-uuid
Version: %{versiontag}
Release: %{releasetag}%{?dist}
Summary: Generate UUIDs in VCL

License: BSD-2-Clause
URL:     https://github.com/otto-de/libvmod-uuid
Source:  %{srcurl}

BuildRequires: 	gcc
BuildRequires: 	make
BuildRequires:  varnish-devel = %{version}-%{release}
BuildRequires: 	uuid-devel

# Build from a git checkout
BuildRequires: 	automake
BuildRequires: 	autoconf
BuildRequires: 	libtool
BuildRequires: 	python3-docutils
BuildRequires: 	autoconf-archive

Requires:  	varnish = %{version}-%{release}
Requires: 	uuid

%description
TODO

%prep
%setup -q -n lib%{name}-%{srcversion}


%build
./autogen.sh
%configure 
%make_build


%install
%make_install docdir=%_pkgdocdir
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'


%check
%make_build check VERBOSE=1


%files
%doc COPYING README.rst
%license LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*


%changelog
* Mon Dec 01 2025 Varnish Software <opensource@varnish-software.com> - 1.0.0
- This changelog is not in use.
