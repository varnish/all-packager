Name:    vmod-jq
Version: %{versiontag}
Release: %{releasetag}%{?dist}
Summary: Use jq programs from VCL

License: BSD-2-Clause
URL:     https://github.com/varnishcache-friends/libvmod-jq
Source:  %{srcurl}

BuildRequires: 	gcc
BuildRequires: 	make
BuildRequires: 	pkgconfig(varnishapi)
BuildRequires:	varnish-devel = %{version}-%{release}
BuildRequires: 	jq-devel

# Build from a git checkout
BuildRequires: 	automake
BuildRequires: 	autoconf
BuildRequires: 	libtool
BuildRequires: 	python3-docutils
BuildRequires: 	autoconf-archive

Requires:	varnish = %{version}-%{release}
Requires: 	jq

%description
TODO: description

%prep
%setup -q -n lib%{name}-%{srcversion}


%build
#sh bootstrap
./autogen.sh
%configure 
%make_build


%install
%make_install docdir=%_pkgdocdir
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'


%check
%make_build check VERBOSE=1


%files
#doc docs AUTHORS CHANGES.md README.md
%license %{_docdir}/vmod-jq/LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*


%changelog
* Mon Dec 01 2025 Varnish Software <opensource@varnish-software.com> - 1.0.0
- This changelog is not in use.
