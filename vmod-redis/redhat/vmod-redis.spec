Name:           vmod-redis
Version:	%{versiontag}
Release:        %{releasetag}%{?dist}
Group:          System Environment/Libraries
Summary:        VMOD using the synchronous hiredis library API to access Redis servers from VCL
URL:            https://github.com/varnish/libvmod-redis
License:        BSD-2-Clause
Source:         %{srcurl}


BuildRequires: gcc
BuildRequires: make
BuildRequires: varnish-devel = %{version}-%{release}
BuildRequires: hiredis-devel

# Build from a git checkout
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: python3-docutils
BuildRequires: autoconf-archive
BuildRequires: libev-devel
%if 0%{?rhel} >= 10 || 0%{?amzn} >= 2023
BuildRequires: valkey
%else
BuildRequires: redis
%endif

BuildRequires:  pkgconfig(varnishapi) >= 6

Requires:	varnish = %{version}-%{release}
Requires: 	hiredis
Requires: 	libev


%description
TODO: description


%prep
%setup -q -n lib%{name}-%{srcversion}


%build
./autogen.sh
%configure CFLAGS="%{optflags}" --disable-tls
%make_build


%install
%make_install
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'


%check
# TODO: fix tests
#%make_build check VERBOSE=1


%files
%{_mandir}/man?/*
%{_docdir}/*
%{_libdir}/*/vmods/*.so


%changelog
* Mon Dec 01 2025 Varnish Software <opensource@varnish-software.com> - 1.0.0
- Changelog not maintained
