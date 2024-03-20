# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

%global srccommit 109482b5d720d12d74e1fd5002ab4c72a648293b

Name:    varnishlog-json
Version: %{varnishver}.0
Release: 1%{?dist}
Summary: Output Varnish logs in JSON

License: BSD-2-Clause
URL:     https://github.com/varnish/varnishlog-json
Source:  https://github.com/varnish/varnishlog-json/archive/%{srccommit}.tar.gz

BuildRequires: gcc
BuildRequires: cmake
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish
BuildRequires: cjson-devel
BuildRequires: jq

BuildRequires: %docutils

Requires: varnish = %varnishver
Requires: cjson

%description
TODO: description

%prep
%setup -q -n %{name}-%{srccommit}


%build
%cmake
%cmake_build


%install
%cmake_install


%check
%ctest


%files
%doc README.md
%license LICENSE
%{_bindir}/varnishlog-json
%{_mandir}/varnishlog-json.1


%changelog
* Thu Jul 24 2014 Varnish Software <opensource@varnish-software.com> - 3.0.0-1
- This changelog is not in use.
