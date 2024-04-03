# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

Name:           libvmod-redis
Version:        @VERSION@
Release:        1%{?dist}
Group:          System Environment/Libraries
Summary:        @DESC@
URL:            @URL@
License:        GPLv3+
Source:         @DOWNLOAD_URL@


BuildRequires: gcc
BuildRequires: make
BuildRequires: varnish-devel = %{varnishver}
BuildRequires: hiredis-devel

# Build from a git checkout
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: %docutils
BuildRequires: autoconf-archive
BuildRequires: libev-devel
BuildRequires: redis

BuildRequires:  pkgconfig(varnishapi) >= 6

# varnish-devel may not require Python or Varnish as it should
BuildRequires:  python(abi) >= 3.4

Requires:       varnish = %{varnishver}
Requires: 	hiredis
Requires: 	libev


%description
@LONG_DESC@

%prep
%setup -q -n @UNTAR_DIR@


%build
export RST2MAN=%{rst2man}
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
* @CHANGELOG_DATE@ @MAINTAINER@ - @VERSION@-1
- Changelog not maintained
