# from https://src.fedoraproject.org/rpms/vmod-reqwest/raw/rawhide/f/vmod-reqwest.spec
%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

%global docutils python3-docutils
%global rst2man rst2man

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

Name:    vmod-reqwest
%global srcversion %(source ../pkg.env && echo ${VARS[%{name}_version]})
Version: %{varnishver}
Release: %(source ../pkg.env && echo ${package_release})%{?dist}
Summary: Use dynamic vmods and HTTP request inside Varnish

License: BSD-3-Clause
URL:     https://github.com/varnish-rs/vmod-reqwest
Source:  %(source ../pkg.env && echo ${VARS[%{name}_source]})


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
%autosetup -n %{name}-%{srcversion}
cargo fetch --locked


%build

cargo build --frozen --release -j12


%install
install -Dt %{buildroot}/$(pkg-config varnishapi --variable=vmoddir) target/release/*.so


%check
export RUST_BACKTRACE=1
# VARNISHTEST_DURATION=20s is needed because some test may go slightly over the 5s timeout
export VARNISHTEST_DURATION=20s
#cargo test --frozen --release


%files
#doc docs AUTHORS CHANGES.rst COPYING README.rst
%doc README.md
%license LICENSE
%{_libdir}/varnish/vmods/*


%changelog
* Thu Jan 01 1970 Varnish Software <opensource@varnish-software.com> - 1.0.0
- This changelog is not in use.
