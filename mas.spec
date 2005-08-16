Name:		mas
Summary:	The Media Application Server(TM)
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
Patch7:		%{name}-%{version}-logdir.patch.bz2
Patch8:		%{name}-0.6.2-fftw.patch.bz2
URL:		http://www.mediaapplicationserver.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	gtk+2-devel
BuildRequires:	pkgconfig

%description
MAS (Media Application Server) is a multi-platform sound client/server
system. MAS supports the desktop and, transparently, the network. In
particular, MAS will provide complete support for the X Window System,
across the network. Run the mas server as root with mas-launch.

%package devel
Summary:	MAS development package
Group:		Libraries
License:	BSD
Requires:	glibc-devel
Requires:	mas

%description devel
This package contains the files needed to compile programs that use
the MAS.

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
%{__make} DESTDIR=$RPM_BUILD_ROOT MANPATH=%{_manpath} LIBDIR=%{_libdir} USRLIBDIR=%{_libdir} install
%{__make} DESTDIR=$RPM_BUILD_ROOT MANPATH=%{_manpath} install.man
install -d $RPM_BUILD_ROOT/var/log/mas/

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
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
%dir /var/log/mas/

%files devel
%defattr(644,root,root,755)
%{_includedir}/mas
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/config
