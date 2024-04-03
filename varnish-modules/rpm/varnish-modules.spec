# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec

%global docutils python3-docutils
%global rst2man rst2man

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

Name:    @NAME@
Version: @VERSION@.0
%global version @VERSION@
Release: 1%{?dist}
Summary: @DESC@

License: BSD-2-Clause
URL:     @URL@
Source:  @DOWNLOAD_URL@

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish

# Build from a git checkout
#BuildRequires: automake
#BuildRequires: autoconf
#BuildRequires: libtool
BuildRequires: %docutils

Requires: varnish = @VVERSION@

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
@LONG_DESC@


%prep
%autosetup -n @UNTAR_DIR@


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
* @CHANGELOG_DATE@ @MAINTAINER@ - @VERSION@-1
- This changelog is not in use.
