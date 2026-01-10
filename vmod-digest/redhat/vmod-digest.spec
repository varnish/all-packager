Name:           vmod-digest
Version: 	%{versiontag}
Release:        %{releasetag}%{?dist}
Group:          System Environment/Libraries
Summary:        Varnish Module (vmod) for computing HMAC, message digests and working with base64.
URL:            https://github.com/varnish/libvmod-digest
License:        BSD-2-Clause
Source:         %{srcurl}


BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	mhash-devel
BuildRequires:	varnish-devel = %{version}-%{release}

# Build from a git checkout
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	python3-docutils
BuildRequires:	autoconf-archive

BuildRequires:  pkgconfig(varnishapi) >= 6

Requires:	varnish = %{version}-%{release}

%description
Varnish Module (vmod) for computing HMAC, message digests and working with base64.
All HMAC- and hash-functionality is provided by libmhash, while base64 is implemented locally.


%prep
%setup -q -n libvmod-digest-libvmod-digest-%{srcversion}


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
