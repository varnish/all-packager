# from https://src.fedoraproject.org/rpms/varnish-modules/raw/rawhide/f/varnish-modules.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

%global docutils python3-docutils
%global rst2man rst2man

Name:    @NAME@
Version: @VERSION@
Release: 1%{?dist}
Summary: @DESC@

License: BSD-2-Clause
URL:     @URL@
Source:  @DOWNLOAD_URL@

BuildRequires: gcc
BuildRequires: cmake
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish
BuildRequires: cjson-devel
BuildRequires: jq

BuildRequires: %docutils

Requires: varnish = @VVERSION@
Requires: cjson

%description
@LONG_DESC@

%prep
%setup -q -n @UNTAR_DIR@


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
* @CHANGELOG_DATE@ @MAINTAINER@ - @VERSION@-1
- This changelog is not in use.
