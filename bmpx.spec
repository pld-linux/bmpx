#
# Conditional build:
%bcond_with	gstreamer	# build with GStreamer support (instead of XINE)

Summary:	Sound player with the WinAmp GUI, for Unix-based systems for GTK+2
Summary(pl):	Odtwarzacz d¼wiêku z interfejsem WinAmpa dla GTK+2
Name:		bmpx
Version:	0.12.1
Release:	1
License:	GPL v2
Group:		X11/Applications/Sound
Source0:	http://download.berlios.de/bmpx/%{name}-%{version}.tar.gz
# Source0-md5:	40965fe0e9707a49a773c91eff777fb2
Source1:	mp3license
Patch0:		%{name}-embedded-images.patch
URL:		http://bmpx.berlios.de/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	curl-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	esound-devel >= 0.2.8
BuildRequires:	fam-devel
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	rpm-pythonprov
BuildRequires:	taglib-devel
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= 0.9.1
%else
BuildRequires:	xine-lib-devel
%endif
Requires:	%{name}-plugin-flow = %{epoch}:%{version}-%{release}
Requires:	%{name}-plugin-container = %{epoch}:%{version}-%{release}
Requires:	%{name}-plugin-transport = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BMPx is the follow-up of the BMP project with a codebase rewritten
from scratch and aims to maintain a stable audio player foundation,
and to provide a player with a consistent and easy to understand usage
experience.

%description -l pl
BMPx jest nastêpc± projektu BMP z przepisanym od zera kodem i skupia
siê na utrzymaniu stabilnej podstawy odtwarzacza d¼wiêku, aby
udostêpniæ odtwarzacz ze spójn± i ³atw± do zrozumienia obs³ug±.

%package devel
Summary:	Header files for BMPx media player
Summary(pl):	Pliki nag³ówkowe odtwarzacza multimedialnego BMPx
Group:		X11/Development/Libraries
#Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files required for compiling BMPx media player plugins.

%description devel -l pl
Pliki nag³ówkowe potrzebne do kompilowania wtyczek odtwarzacza
multimedialnego BMPx.

%package plugin-container
Summary:	Container plugin for BMPx
Summary(pl):	Wtyczka Container dla BMPx
Group:		X11/Applications/Sound
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description plugin-container
Plugin providing support for folders, m3u & pls playlist files, etc.

%description plugin-container -l pl
Wtyczka dodaj±ca obs³ugê folderów, playlist w formacie m3u i pls, itp.

%package plugin-flow
Summary:        Flow plugin for BMPx
Summary(pl):    Wtyczka Flow dla BMPx
Group:          X11/Applications/Sound
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description plugin-flow
Flow plugin for BMPx.

%description plugin-flow -l pl
Wtyczka Flow dla BMPx.

%package plugin-transport
Summary:	Transport plugin for BMPx
Summary(pl):	Wtyczka Transport dla BMPx
Group:		X11/Applications/Sound
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description plugin-transport
Transport plugin for BMPx.

%description plugin-transport -l pl
Wtyczka Transport dla BMPx.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
rm -rf autom4te.cache
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%if %{with gstreamer}
	--enable-gst \
	--disable-xine
%else
	--enable-xine \
%endif
	--enable-shared \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

rm -f $RPM_BUILD_ROOT%{_datadir}/bmpx/data/GPL.txt

install -d $RPM_BUILD_ROOT%{_pixmapsdir}
mv -f $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/bmpx.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/bmpx/plugins/*/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:

/sbin/ldconfig

%postun
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1

/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/bmp*
%attr(755,root,root) %{_libdir}/libskinned.so.*.*.*
%dir %{_libdir}/bmpx
%dir %{_libdir}/bmpx/plugins
%{_mandir}/man*/*
%{_desktopdir}/*
%{_datadir}/bmpx
%{_datadir}/bmp-remote
%{_pixmapsdir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/bmpx

%files plugin-container
%defattr(644,root,root,755)
%dir %{_libdir}/bmpx/plugins/container
%attr(755,root,root) %{_libdir}/bmpx/plugins/container/*.so*

%files plugin-flow
%defattr(644,root,root,755)
%dir %{_libdir}/bmpx/plugins/flow
%attr(755,root,root) %{_libdir}/bmpx/plugins/flow/*.so*

%files plugin-transport
%defattr(644,root,root,755)
%dir %{_libdir}/bmpx/plugins/transport
%attr(755,root,root) %{_libdir}/bmpx/plugins/transport/*.so*
