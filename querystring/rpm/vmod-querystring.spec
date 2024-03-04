Name:           vmod-querystring
Version:        2.0.3
Release:        1%{?dist}
Group:          System Environment/Libraries
Summary:        QueryString module for Varnish Cache
URL:            https://github.com/Dridi/libvmod-querystring
License:        GPLv3+

Source:         %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(varnishapi) >= 6

# varnish-devel may not require Python or Varnish as it should
BuildRequires:  varnish >= 6.0.6
BuildRequires:  python(abi) >= 3.4

Requires:       varnish >= %(varnishd -V 2>&1 | awk -F '[- ]' '{print $3; exit}')


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
%setup -q


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
* Wed Feb 06 2019 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - @VERSION@-1
- Changelog not maintained