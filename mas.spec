Summary:	The Media Application Server(TM)
Summary(pl.UTF-8):	Media Application Server - system dźwięku o architekturze klient-serwer
Name:		mas
Version:	0.6.3
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.mediaapplicationserver.net/%{name}-%{version}.tar.gz
# Source0-md5:	297dab763820f6ccc3b4f20f76944ac1
Source1:	http://www.mediaapplicationserver.net/%{name}-control-apps-%{version}.tar.gz
# Source1-md5:	3e6db156e8dcab89f513b1cb7164819d
Source2:	http://www.mediaapplicationserver.net/%{name}-devtools-%{version}.tar.gz
# Source2-md5:	bb6d66aa37a5b49613df4f8ecb63ce4b
Source3:	%{name}conf.desktop
Source4:	%{name}mix.desktop
Source5:	%{name}player.desktop
Patch0:		%{name}-path.dif
Patch1:		%{name}-byteswap-fix.dif
Patch2:		%{name}-add-components.dif
Patch3:		%{name}-lib64.dif
Patch4:		%{name}-0.6.0-x86_64.patch
Patch5:		%{name}-launch-fix.dif
Patch6:		%{name}-launch-lib64-fix.dif
Patch7:		%{name}-%{version}-logdir.patch
Patch8:		%{name}-0.6.2-fftw.patch
URL:		http://www.mediaapplicationserver.net/
BuildRequires:	gtk+2-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MAS (Media Application Server) is a multi-platform sound client/server
system. MAS supports the desktop and, transparently, the network. In
particular, MAS will provide complete support for the X Window System,
across the network. Run the mas server as root with mas-launch.

%description -l pl.UTF-8
MAS (Medai Application Server) to wieloplatformowy system dźwięku o
architekturze klient-serwer. MAS obsługuje pulpit i, w sposób
przezroczysty, sieć. W szczególności MAS dostarcza pełne wsparcie dla
X Window System po sieci. Serwer mas należy uruchomić jako root
poprzez mas-launch.

%package devel
Summary:	MAS development package
Summary(pl.UTF-8):	Pakiet programistyczny MAS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glibc-devel

%description devel
This package contains the files needed to compile programs that use
the MAS.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne do kompilowania programów
używajacych MAS-a.

%prep
%setup -q -a 1 -a 2
%patch0 -p1
%patch1 -p1
%patch2 -p1
#if [ "%_lib" == "lib64" ]; then
#%patch3
#fi
#%patch4
#%patch5
#if [ "%_lib" == "lib64" ]; then
#%patch6
#fi
%patch7 -p1
%patch8 -p1


%build
imake -I./config
%{__make} World
cd clients/util
# fix mas-config
echo '#!/bin/sh' > mas-config.new
cat mas-config.new mas-config > mas-config.tmp
mv mas-config.tmp mas-config
# fix mas-

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/log/mas

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MANPATH=%{_manpath} \
	LIBDIR=%{_libdir} \
	USRLIBDIR=%{_libdir}

%{__make} install.man \
	DESTDIR=$RPM_BUILD_ROOT \
	MANPATH=%{_manpath}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE PORTING README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*
%{_libdir}/mas
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%dir /var/log/mas

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/mas
%{_libdir}/config
