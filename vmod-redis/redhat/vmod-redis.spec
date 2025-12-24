# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

Name:           vmod-redis
%global srcversion %(source ../pkg.env && echo ${VARS[%{name}_version]})
Version:	%{varnishver}
Release:        %(source ../pkg.env && echo ${package_release})%{?dist}
Group:          System Environment/Libraries
Summary:        VMOD using the synchronous hiredis library API to access Redis servers from VCL
URL:            https://github.com/varnish/libvmod-redis
License:        BSD-2-Clause
Source:         %(source ../pkg.env && echo ${VARS[%{name}_source]})


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
%if 0%{?rhel} >= 10 || 0%{?amzn} >= 2023
BuildRequires: valkey
%else
BuildRequires: redis
%endif

BuildRequires:  pkgconfig(varnishapi) >= 6

# varnish-devel may not require Python or Varnish as it should
BuildRequires:  python(abi) >= 3.4

Requires:       varnish = %{varnishver}
Requires: 	hiredis
Requires: 	libev


%description
TODO: description

%prep
%setup -q -n lib%{name}-%{srcversion}


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
* Thu Jan 01 1970 Varnish Software <opensource@varnish-software.com> - 1.0.0
- Changelog not maintained
