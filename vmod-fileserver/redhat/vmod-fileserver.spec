Name:    vmod-fileserver
Version: %{versiontag}
Release: %{releasetag}%{?dist}
Summary: TODO: summary

License: BSD-3-Clause
URL:     https://github.com/varnish-rs/vmod-fileserver
Source:  %{srcurl}


BuildRequires: 	openssl-devel
BuildRequires: 	jq
BuildRequires: 	cargo
BuildRequires: 	clang-devel
BuildRequires:	varnish-devel = %{version}-%{release}

Requires:	varnish = %{version}-%{release}

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
cargo test --frozen --release


%files
%doc README.md
%license LICENSE
%{_libdir}/varnish/vmods/*


%changelog
* Mon Dec 01 2025 Varnish Software <opensource@varnish-software.com> - 1.0.0
- This changelog is not in use.
