Summary:	Small, simple HTTP daemon, supports SSL
Summary(pl):	Ma³y, prosty serwer HTTP ze wsparciem dla SSL
Name:		mini_httpd
Version:	1.19
Release:	2
License:	freely distributable
Group:		Networking/Daemons
URL:		http://www.acme.com/software/mini_httpd/
Source0:	http://www.acme.com/software/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	792a529dfe974355aad8ba6c80e54e7a
Source1:	%{name}.init
Source2:	%{name}.config
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	sed
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		httpdir		/home/services/httpd
%define		htmldir		%{httpdir}/html

%description
Simple and small HTTP daemon supporting SSL.

%description -l pl
Prosty i ma³y serwer HTTP ze wsparciem dla SSL.

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
install htpasswd	$RPM_BUILD_ROOT%{_bindir}/mini_htpasswd
install htpasswd.1	$RPM_BUILD_ROOT%{_mandir}/man1/mini_htpasswd.1
install *.8		$RPM_BUILD_ROOT%{_mandir}/man8

install index.html	$RPM_BUILD_ROOT%{htmldir}
install %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

sed -e 's,@DOCROOT@,%{htmldir},' %{SOURCE2} > $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig %{name} reset
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = "0" ]; then
	/etc/rc.d/init.d/%{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%dir %{httpdir}
%dir %{htmldir}
%{htmldir}/index.html
%attr(754,root,root) /etc/rc.d/init.d/mini_httpd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}
%{_mandir}/man*/*
