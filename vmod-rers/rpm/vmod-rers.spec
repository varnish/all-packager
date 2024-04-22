# from https://src.fedoraproject.org/rpms/vmod-rers/raw/rawhide/f/vmod-rers.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

%global docutils python3-docutils
%global rst2man rst2man

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

Name:    vmod-rers
Version: %(source ../pkg.env && echo $TOOL_VERSION)
Release: %(source ../pkg.env && echo $PKG_RELEASE)%{?dist}
Summary: TODO: summary

License: BSD 3-Clause License
URL:     https://github.com/gquintard/vmod-rers
Source:  %(source ../pkg.env && echo $TOOL_SOURCE)

BuildRequires: openssl-devel
BuildRequires: jq
BuildRequires: cargo
BuildRequires: clang-devel
BuildRequires: varnish
BuildRequires: %docutils

Requires: varnish = %varnishver

%description
TODO: description

%prep
%autosetup
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
* Thu Jul 24 2014 Varnish Software <opensource@varnish-software.com> - 3.0.0-1
- This changelog is not in use.
