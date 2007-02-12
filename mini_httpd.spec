Summary:	Small, simple HTTP daemon, supports SSL
Summary(pl.UTF-8):   Mały, prosty serwer HTTP ze wsparciem dla SSL
Name:		mini_httpd
Version:	1.19
Release:	4
License:	freely distributable
Group:		Networking/Daemons
Source0:	http://www.acme.com/software/mini_httpd/%{name}-%{version}.tar.gz
# Source0-md5:	792a529dfe974355aad8ba6c80e54e7a
Source1:	%{name}.init
Source2:	%{name}.config
URL:		http://www.acme.com/software/mini_httpd/
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	htpasswd
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		httpdir		/home/services/httpd
%define		htmldir		%{httpdir}/html

%description
Simple and small HTTP daemon supporting SSL.

%description -l pl.UTF-8
Prosty i mały serwer HTTP ze wsparciem dla SSL.

%package -n htpasswd-%{name}
Summary:	mini_httpd htpasswd utility
Summary(pl.UTF-8):   Narzędzie htpasswd z mini_httpd
Group:		Networking/Utilities
Provides:	htpasswd
Obsoletes:	htpasswd

%description -n htpasswd-%{name}
htpasswd is used to create and update the flat-files used to store
usernames and password for basic authentication of HTTP users. This
package contains htpasswd from mini_httpd; it supports only CRYPT
encryption algorithm.

%description -n htpasswd-%{name} -l pl.UTF-8
htpasswd służy do tworzenia i uaktualniania płaskich plików służących
do przechowywania nazw użytkowników i haseł do uwierzytelnienia basic
użytkowników HTTP. Ten pakiet zawiera htpasswd z mini_httpd; ta wersja
obsługuje wyłącznie hasła zaszyfrowane przez CRYPT.

%prep
%setup -q

%build
%{__make} \
	SSL_INCDIR=%{_includedir}/openssl \
	SSL_LIBDIR=%{_libdir} \
	SSL_DEFS=-DUSE_SSL \
	SSL_INC=-I%{_includedir}/openssl \
	SSL_LIBS='-lssl -lcrypto' \
	BINDIR=%{_bindir} \
	MANDIR=%{_mandir} \
	CFLAGS="-DUSE_SSL -I%{_includedir}/openssl %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,8}
install -d $RPM_BUILD_ROOT%{htmldir}
install -d $RPM_BUILD_ROOT/etc/sysconfig

install mini_httpd	$RPM_BUILD_ROOT%{_sbindir}
install htpasswd	$RPM_BUILD_ROOT%{_bindir}/htpasswd
ln -sf %{_bindir}/htpasswd $RPM_BUILD_ROOT%{_sbindir}
install htpasswd.1	$RPM_BUILD_ROOT%{_mandir}/man1/htpasswd.1
install *.8		$RPM_BUILD_ROOT%{_mandir}/man8

install index.html	$RPM_BUILD_ROOT%{htmldir}
install %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

sed -e 's,@DOCROOT@,%{htmldir},' %{SOURCE2} > $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig %{name} reset
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/mini_httpd
%dir %{httpdir}
%dir %{htmldir}
%{htmldir}/index.html
%attr(754,root,root) /etc/rc.d/init.d/mini_httpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{_mandir}/man8/*

%files -n htpasswd-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/htpasswd
%attr(755,root,root) %{_sbindir}/htpasswd
%{_mandir}/man1/htpasswd.1*
