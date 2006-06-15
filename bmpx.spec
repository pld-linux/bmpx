Summary:	Sound player with the WinAmp GUI, for Unix-based systems for GTK+
Summary(pl):	Odtwarzacz d¼wiêku z interfejsem WinAmpa dla GTK+
Name:		bmpx
Version:	0.14.4
Release:	1
License:	GPL v2
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/beepmp/%{name}-%{version}.tar.bz2
# Source0-md5:	cd89d4afdf64bdf483c8ffcdacd7a009
Source1:	mp3license
Patch0:		%{name}-desktop.patch
URL:		http://beep-media-player.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	curl-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	esound-devel >= 0.2.8
BuildRequires:	flex
BuildRequires:	gamin-devel
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.4
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	hal-devel
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libmusicbrainz-devel >= 2.1.1
BuildRequires:	libtool
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	libxml2-devel >= 2.6.1
BuildRequires:	neon-devel >= 0.25.5
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	rpm-pythonprov
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	taglib-devel >= 1.4
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-plugins-base = %{version}-%{release}
Requires:	desktop-file-utils
Requires:	gstreamer-audio-effects-base
Requires:	gstreamer-audio-formats
Requires:	gstreamer-audiosink
Requires:	shared-mime-info
Obsoletes:	bmpx-curses
Obsoletes:	bmpx-remote
Obsoletes:	bmpx-remote-gtk
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

%package libs
Summary:	BMPx player libraries
Summary(pl):	Biblioteki odtwarzacza BMPx
Group:		X11/Libraries
Obsoletes:	libchroma
Obsoletes:	libhrel

%description libs
BMPx player libraries.

%description libs -l pl
Biblioteki odtwarzacza BMPx.

%package devel
Summary:	Header files for BMPx media player
Summary(pl):	Pliki nag³ówkowe odtwarzacza multimedialnego BMPx
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk+2-devel >= 2:2.8.0
Obsoletes:	libchroma-devel
Obsoletes:	libhrel-devel

%description devel
Header files required for compiling BMPx media player plugins.

%description devel -l pl
Pliki nag³ówkowe potrzebne do kompilowania wtyczek odtwarzacza
multimedialnego BMPx.

%package static
Summary:	Static BMPx library
Summary(pl):	Statyczna biblioteka BMPx
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	libchroma-static
Obsoletes:	libhrel-static

%description static
Static BMPx library.

%description static -l pl
Statyczna biblioteka BMPx.

%package plugins-base
Summary:	Base plugins for BMPx
Summary(pl):	Podstawowe wtyczki dla BMPx
Group:		X11/Applications/Sound
Requires:	%{name} = %{version}-%{release}
Obsoletes:	bmpx-plugin-container
Obsoletes:	bmpx-plugin-flow
Obsoletes:	bmpx-plugin-transport

%description plugins-base
Base plugins for BMPx.

%description plugins-base -l pl
Podstawowe wtyczki dla BMPx.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--enable-hal \
	--enable-shared \
	--enable-static \
	--with-dbus-services-dir=%{_datadir}/dbus-1/services
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

rm -f $RPM_BUILD_ROOT%{_libdir}/bmp-2.0/plugins/*/*.{a,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

umask 022
/usr/bin/update-mime-database %{_datadir}/mime || :

%banner %{name} -e << EOF
Remember to install appropriate GStreamer plugins for files
you want to play:
- gstreamer-flac (for FLAC)
- gstreamer-mad (for MP3s)
- gstreamer-vorbis (for Ogg Vorbis)
EOF

%postun
%update_desktop_database_postun
if [ $1 = 0 ]; then
        umask 022
        /usr/bin/update-mime-database %{_datadir}/mime
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/beep-media-player-2
%attr(755,root,root) %{_bindir}/bmp-enqueue-files-2.0 
%attr(755,root,root) %{_bindir}/bmp-enqueue-uris-2.0
%attr(755,root,root) %{_bindir}/bmp-play-files-2.0
%attr(755,root,root) %{_libexecdir}/beep-media-player-2-bin
%dir %{_libdir}/bmp-2.0
%dir %{_libdir}/bmp-2.0/plugins
%{_datadir}/bmpx
%{_datadir}/dbus-1/services/*.service
%{_mandir}/man*/*
%{_desktopdir}/*
%{_pixmapsdir}/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/bmp-2.0
%{_includedir}/libchroma
%{_includedir}/libhrel
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files plugins-base
%defattr(644,root,root,755)
%dir %{_libdir}/bmp-2.0/plugins/container
%dir %{_libdir}/bmp-2.0/plugins/flow
%dir %{_libdir}/bmp-2.0/plugins/transport
%attr(755,root,root) %{_libdir}/bmp-2.0/plugins/container/*.so*
%attr(755,root,root) %{_libdir}/bmp-2.0/plugins/flow/*.so*
%attr(755,root,root) %{_libdir}/bmp-2.0/plugins/transport/*.so*
