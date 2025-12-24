# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

Name:           vmod-digest
%global srcversion %(source ../pkg.env && echo ${VARS[%{name}_version]})
Version: 	%{varnishver}
Release:        %(source ../pkg.env && echo ${package_release})%{?dist}
Group:          System Environment/Libraries
Summary:        Varnish Module (vmod) for computing HMAC, message digests and working with base64.
URL:            https://github.com/varnish/libvmod-digest
License:        BSD-2-Clause
Source:         %(source ../pkg.env && echo ${VARS[%{name}_source]})


BuildRequires: gcc
BuildRequires: make
BuildRequires: varnish
BuildRequires: mhash-devel

# Build from a git checkout
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: %docutils
BuildRequires: autoconf-archive

BuildRequires:  pkgconfig(varnishapi) >= 6

# varnish-devel may not require Python or Varnish as it should
BuildRequires:  varnish >= 6.0.6
BuildRequires:  python(abi) >= 3.4

Requires:       varnish >= %(varnishd -V 2>&1 | awk -F '[- ]' '{print $3; exit}')


%description
Varnish Module (vmod) for computing HMAC, message digests and working with base64.
All HMAC- and hash-functionality is provided by libmhash, while base64 is implemented locally.


%prep
%setup -q -n libvmod-digest-libvmod-digest-%{srcversion}


%build
export RST2MAN=%{rst2man}
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
* Thu Jan 01 1970 Varnish Software <opensource@varnish-software.com> - 1.0.0
- Changelog not maintained
