Summary:	Dynamic Kernel Module Support Framework
Summary(pl.UTF-8):	Obsługa dynamicznych modułów jądra
Name:		dkms
Version:	2.2.0.3
Release:	4
License:	GPL v2+
Group:		Base/Kernel
Source0:	http://linux.dell.com/dkms/permalink/%{name}-%{version}.tar.gz
# Source0-md5:	11a8aaade2ebec2803653837c7593030
Source1:	%{name}.modprobe.conf
Patch0:		kernel.conf.patch
URL:		http://linux.dell.com/dkms/
Requires:	bash >= 3.0
Requires:	coreutils
Requires:	cpio
Requires:	findutils
Requires:	gawk
Requires:	gcc
Requires:	grep
Requires:	gzip
Requires:	kmod
Requires:	lsb-release
Requires:	sed
Requires:	tar
Suggests:	kernel-module-build
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DKMS stands for Dynamic Kernel Module Support. It is designed to
create a framework where kernel dependant module source can reside so
that it is very easy to rebuild modules as you upgrade kernels. This
will allow Linux vendors to provide driver drops without having to
wait for new kernel releases while also taking out the guesswork for
customers attempting to recompile modules for new kernels.

%description -l pl.UTF-8
DKMS (Dynamic Kernel Module Support) to obsługa dynamicznych modułów
jądra. Została zaprojektowana aby stworzyć szkielet do przechowywania
źródeł modułów zależnych od jądra w sposób łatwy do zbudowania modułów
po uaktualnieniu jądra. Pozwala to dostawcom Linuksa udostępniać
sterowniki bez czekania na nowe wydania jądra ani rozwiązywania
problemów klientów próbujących przebudować moduły dla nowych jąder.

%package -n bash-completion-dkms
Summary:	Bash completion for dkms command
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla polecenia dkms
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion

%description -n bash-completion-dkms
Bash completion for dkms command.

%description -n bash-completion-dkms -l pl.UTF-8
Bashowe uzupełnianie parametrów dla polecenia dkms.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/modprobe.d

%{__make} install \
	SHELL=/bin/sh \
	DESTDIR=$RPM_BUILD_ROOT

# not in pld
%{__rm} $RPM_BUILD_ROOT/etc/kernel/postinst.d/dkms
%{__rm} $RPM_BUILD_ROOT/etc/kernel/prerm.d/dkms
%{__rm} $RPM_BUILD_ROOT/usr/lib/dkms/dkms_autoinstaller

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/modprobe.d/dkms.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README.dkms TODO sample.spec
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/framework.conf
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/dkms.conf
%attr(755,root,root) %{_sbindir}/dkms
%{_mandir}/man8/dkms.8*
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/common.postinst
%dir %{_localstatedir}/lib/%{name}
%{_localstatedir}/lib/%{name}/dkms_dbversion

%files -n bash-completion-dkms
%defattr(644,root,root,755)
/etc/bash_completion.d/dkms
