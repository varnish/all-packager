%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)

%global docutils python3-docutils
%global rst2man rst2man

# no debugsource, no debuginfo
%global debug_package %{nil}
%global _debugsource_template %{nil}

Name:    vmod-fileserver
Version: %{varnishver}.0
%global version 0.0.6-1
Release: 1%{?dist}
Summary: TODO: summary

#Fix the tar-ball extracted dir name
%global d_name %(echo %{name} | sed 's/-/_/g')

License: BSD 3-Clause License
URL:     https://github.com/gquintard/vmod-fileserver
Source:  https://github.com/gquintard/%{d_name}/archive/refs/tags/v%{version}.tar.gz


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
%autosetup -n %{d_name}-%{version}
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
