Name:           vmod-querystring
Version:	%{versiontag}
Release: 	%{releasetag}%{?dist}
Group:          System Environment/Libraries
Summary:        QueryString module for Varnish Cache
URL:            https://github.com/Dridi/libvmod-querystring
License:        GPL-3.0-or-later
Source: 	%{srcurl}

BuildRequires:	gcc
BuildRequires:  make
BuildRequires:  varnish-devel = %{version}-%{release}
BuildRequires:  python3-docutils

Requires:	varnish = %{version}-%{release}


%description
The purpose of this module is to give you a fine-grained control over a URL's
query-string in Varnish Cache. It's possible to remove the query-string, clean
it, sort its parameters or filter it to only keep a subset of them.

This can greatly improve your hit ratio and efficiency with Varnish, because
by default two URLs with the same path but different query-strings are also
different. This is what the RFCs mandate but probably not what you usually
want for your web site or application.

A query-string is just a character string starting after a question mark in a
URL. But in a web context, it is usually a structured key/values store encoded
with the `application/x-www-form-urlencoded` media type. This module deals
with this kind of query-strings.


%prep
%setup -q -n %{name}-%{srcversion}


%build
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
