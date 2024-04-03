# from https://src.fedoraproject.org/rpms/vmod-reqwest/raw/rawhide/f/vmod-reqwest.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

%global docutils python3-docutils
%global rst2man rst2man

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

Name:    @NAME@
Version: @VERSION@
%global version 0.0.12
Release: 1%{?dist}
Summary: @DESC@

License: BSD-2-Clause
URL:     @URL@
Source:  @DOWNLOAD_URL@

BuildRequires: openssl-devel
BuildRequires: jq
BuildRequires: cargo
BuildRequires: clang-devel
BuildRequires: varnish
BuildRequires: %docutils

Requires: varnish = %varnishver

%description
@LONG_DESC@


%prep
%autosetup -n @UNTAR_DIR@
cargo fetch --locked


%build

cargo build --frozen --release -j12


%install
install -Dt %{buildroot}/$(pkg-config varnishapi --variable=vmoddir) target/release/*.so


%check
export RUST_BACKTRACE=1
cargo test --frozen --release


%files
#doc docs AUTHORS CHANGES.rst COPYING README.rst
%doc README.md
%license LICENSE
%{_libdir}/varnish/vmods/*


%changelog
* @CHANGELOG_DATE@ @MAINTAINER@ - @VERSION@-1
- This changelog is not in use.
