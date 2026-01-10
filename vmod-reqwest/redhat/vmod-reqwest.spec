Name:    vmod-reqwest
Version: %{versiontag}
Release: %{releasetag}%{?dist}
Summary: Use dynamic vmods and HTTP request inside Varnish

License: BSD-3-Clause
URL:     https://github.com/varnish-rs/vmod-reqwest
Source:  %{srcurl}


BuildRequires:  openssl-devel
BuildRequires:  jq
BuildRequires:  cargo
BuildRequires:  clang-devel
BuildRequires:  varnish-devel = %{version}-%{release}

Requires: 	varnish = %{version}-%{release}

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
* Mon Dec 01 2025 Varnish Software <opensource@varnish-software.com> - 1.0.0
- This changelog is not in use.
