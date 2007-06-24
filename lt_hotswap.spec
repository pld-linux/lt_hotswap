%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
%define		_rel	0.1
%define		_mod_suffix	current
#
Summary:	ACPI kernel driver to support hot-swapping ultrabay type peripherals on laptops
Summary(pl.UTF-8):	Sterownik ACPI wspomagający wymianę urządzeń UltraBay w laptopach
Name:		lt_hotswap
Version:	0.3.6
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/lths/%{name}-%{version}.tar.gz
# Source0-md5:	99df18cfbadb92e8b987ac90d32110b2
URL:		http://lths.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The lt_hotswap kernel module enables hot-swapping of UltraBay disk
drives (PATA) under Linux, with DMA support.

%description -l pl.UTF-8
Moduł jądra włączający możliwość podłączania i odłączanie dysków w
UltraBay (PATA) w trakcie pracy.

%package -n kernel%{_alt_kernel}-misc-%{name}
Summary:	Linux kernel module for hot-swapping ultrabay type peripherals
Summary(pl.UTF-8):	Moduł jądra do podłączania i odłączania urządzeń ultrabay w trakcie pracy
Release:		%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):  /sbin/depmod
Requires:	 module-init-tools >= 3.2.2-2
Provides:	%{name}

%description -n kernel%{_alt_kernel}-misc-%{name}
This is a semi-'driver' to support hotswapping on standard PATA
(CD/DVD,HDD) in laptops Fujitsu and IBM.

%description -n kernel%{_alt_kernel}-misc-%{name} -l pl.UTF-8
lt_hotswap umożliwia podłączanie i odłączanie urządzeń PATA
(CD/DVD,HDD) w trakcie pracy w laptopach Fujitsu i IBM.

%prep
%setup -q

%build
%build_kernel_modules -m %{name}

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -s %{_mod_suffix} -n %{name} -m %{name} -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post   -n kernel%{_alt_kernel}-misc-%{name}
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-%{name}
%depmod %{_kernel_ver}

%if %{with dist_kernel}
%files -n kernel%{_alt_kernel}-misc-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/%{name}-%{_mod_suffix}.ko*
%{_sysconfdir}/modprobe.d/%{_kernel_ver}/%{name}.conf
%endif
