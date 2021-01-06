# sbc is used by pulseaudio, which is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 1
%define libname %mklibname %{name} %{major}
%define libnamedevel %mklibname -d %{name}
%define lib32name %mklib32name %{name} %{major}
%define lib32namedevel %mklib32name -d %{name}

Name:		sbc
Version:	1.5
Release:	1
Summary:	Bluetooth SBC utilities
Group:		Communications
License:	GPLv2+
Source0:	http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.xz
Patch0:		sbc-1.2-clang-build-flags.patch
Patch1:		sbc-1.5-non-x86.patch
Url:		http://www.bluez.org/

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	dbus-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(sndfile)
%if %{with compat32}
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libbluetooth)
BuildRequires:	devel(libsndfile)
%endif

%description
Bluetooth SBC utilities.

%package -n %{libname}
Summary:	Bluetooth SBC library
Group:		System/Libraries

%description -n %{libname}
Bluetooth SBC library.

%package -n %{libnamedevel}
Summary:	Bluetooth SBC development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libnamedevel}
Bluetooth SBC development files.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Bluetooth SBC library (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
Bluetooth SBC library.

%package -n %{lib32namedevel}
Summary:	Bluetooth SBC development files (32-bit)
Group:		Development/C
Requires:	%{libnamedevel} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{lib32namedevel}
Bluetooth SBC development files.
%endif

%prep
%autosetup -p1
#sed -i 's!-fgcse-after-reload \\!!g' Makefile.*
export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32
cd ..
%endif

mkdir build
cd build
%configure
cd ..

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%files
%{_bindir}/sbcdec
%{_bindir}/sbcenc
%{_bindir}/sbcinfo

%files -n %{libname}
%{_libdir}/libsbc.so.%{major}*

%files -n %{libnamedevel}
%{_includedir}/%{name}
%{_libdir}/libsbc.so
%{_libdir}/pkgconfig/%{name}.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libsbc.so.%{major}*

%files -n %{lib32namedevel}
%{_prefix}/lib/libsbc.so
%{_prefix}/lib/pkgconfig/%{name}.pc
%endif
