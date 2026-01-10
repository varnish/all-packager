Name:           vmod-geoip2
Version: 	%{versiontag}
Release:        %{releasetag}%{?dist}
Group:          System Environment/Libraries
Summary:        A Varnish 6.0, 7.3 and 7.4 VMOD to query MaxMind GeoIP2 DB files.
URL:            https://github.com/varnish/libvmod-geoip2
License:        BSD-2-Clause
Source:         %{srcurl}

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:	varnish-devel = %{version}-%{release}
BuildRequires:  libmaxminddb
BuildRequires:  libmaxminddb-devel

# Build from a git checkout
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  python3-docutils
BuildRequires:  autoconf-archive

Requires:	varnish = %{version}-%{release}

%description
A Varnish master VMOD to query MaxMind GeoIP2 DB files.


%prep
%setup -q -n lib%{name}-%{srcversion}

%build
./autogen.sh
%configure CFLAGS="%{optflags}"
%make_build


%install
%make_install
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'


%check
%make_build check VERBOSE=1


%files
%{_mandir}/man?/*
%{_docdir}/*
%{_libdir}/*/vmods/*.so


%changelog
* Mon Dec 01 2025 Varnish Software <opensource@varnish-software.com> - 1.0.0
- Changelog not maintained
