%define major 1
%define libname %mklibname %{name} %{major}
%define libnamedevel %mklibname -d %{name}

Name:		sbc
Version:	1.3
Release:	1
Summary:	Bluetooth SBC utilities
Group:		Communications
License:	GPLv2+
Source0:	http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.xz
Patch0:		sbc-1.2-clang-build-flags.patch
Url:		http://www.bluez.org/

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	dbus-devel
BuildRequires:	bluez-devel
BuildRequires:	pkgconfig(sndfile)

%description
Bluetooth SBC utilities

%package -n %{libname}
Summary:	Bluetooth SBC library
Group:		System/Libraries

%description -n %{libname}
Bluetooth SBC library

%package -n %{libnamedevel}
Summary:	Bluetooth SBC development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libnamedevel}
Bluetooth SBC development files

%prep
%setup -q
%apply_patches
#sed -i 's!-fgcse-after-reload \\!!g' Makefile.*

%build
%configure --disable-static
%make

%install
%makeinstall_std

rm -f %{buildroot}%{_libdir}/*.la

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
