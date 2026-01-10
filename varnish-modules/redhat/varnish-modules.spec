Name:    varnish-modules
Version: %{versiontag}
Release: %{releasetag}%{?dist}
Summary: A collection of modules ("vmods") extending Varnish VCL

License: BSD-2-Clause
URL:     https://github.com/varnish/varnish-modules
Source:  %{srcurl}

BuildRequires: gcc
BuildRequires: make
BuildRequires:  varnish-devel = %{version}-%{release}

# Build from a git checkout
#BuildRequires: automake
#BuildRequires: autoconf
#BuildRequires: libtool
BuildRequires: python3-docutils

Requires: varnish = %{version}-%{release}

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
%autosetup -n %{name}-%{srcversion}


%build
#sh bootstrap
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
%doc AUTHORS CHANGES.rst COPYING README.md
%license LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*


%changelog
* Mon Dec 01 2025 Varnish Software <opensource@varnish-software.com> - 1.0.0
- This changelog is not in use.
