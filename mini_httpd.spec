Summary:	small, simple http daemon, supports SSL
Summary(pl):	ma³y, prosty serwer http ze wsparciem dla SSL
Name:		mini_httpd
Version:	1.14
Release:	1
License:	Freely Redistributable
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
URL:		http://www.acme.com/software/mini_httpd/
Source0:	http://www.acme.com/software/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Prereq:		/sbin/chkconfig
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
	IPV6_DEFS='-DUSE_IPV6' \
	BINDIR=%{_bindir} \
	MANDIR=%{_mandir} \
	CFLAGS="-DUSE_SSL -DUSE_IPV6 -I%{_includedir}/openssl %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}
install -d $RPM_BUILD_ROOT/home/httpd/html

install mini_httpd	$RPM_BUILD_ROOT%{_sbindir}
install	htpasswd	$RPM_BUILD_ROOT%{_bindir}/mini-htpasswd
install *.1		$RPM_BUILD_ROOT%{_mandir}/man1
install *.8		$RPM_BUILD_ROOT%{_mandir}/man8

install index.html	$RPM_BUILD_ROOT/home/httpd/html
install %{SOURCE1}	$RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/%{name}

gzip -9nf README

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig %{name} reset
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = "0" ]; then
	%{_sysconfdir}/rc.d/init.d/%{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
/home/httpd/html/index.html
%attr(0755,root,root) /etc/rc.d/init.d/mini_httpd
%{_mandir}/man*/*
