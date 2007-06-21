# TODO: use system libuuid instead of included one
# TODO: use browser-plugins if plugin works with something else than firefox (e.g. seamonkey)
#
# Conditional build:
%bcond_without	gaim	# build without D-BUS gaim support
%bcond_without	sid	# build without sid support
%bcond_without	ofa	# build without MusicIP support
#
Summary:	Sound player with the WinAmp GUI, for Unix-based systems for GTK+
Summary(pl.UTF-8):	Odtwarzacz dźwięku z interfejsem WinAmpa dla GTK+
Name:		bmpx
Version:	0.36.1
Release:	3
License:	GPL v2
Group:		X11/Applications/Sound
Source0:	http://files.beep-media-player.org/releases/0.36/%{name}-%{version}.tar.bz2
# Source0-md5:	03a55f8b5b3899f03d71ca9dd681545d
Source1:	mp3license
Patch0:		%{name}-desktop.patch
URL:		http://beep-media-player.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	boost-bind-devel
BuildRequires:	boost-call_traits-devel
BuildRequires:	boost-devel
BuildRequires:	boost-filesystem-devel
BuildRequires:	boost-regex-devel
BuildRequires:	cdparanoia-III-devel
BuildRequires:	curl-devel
BuildRequires:	dbus-glib-devel >= 0.62
BuildRequires:	esound-devel >= 0.2.8
BuildRequires:	fam-devel
BuildRequires:	flex
%{?with_gaim:BuildRequires:	gaim-devel}
BuildRequires:	gcc-c++ >= 5:4.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.10
BuildRequires:	gtkmm-devel >= 2.9.8
BuildRequires:	hal-devel >= 0.5.7
BuildRequires:	libglademm-devel >= 2.6.2
BuildRequires:	libnotify-devel >= 0.4.2
BuildRequires:	libmusicbrainz-devel >= 2.1.1
%{?with_ofa:BuildRequires:	libofa-devel >= 0.9.3}
BuildRequires:	librsvg-devel >= 1:2.14.0
%{?with_sid:BuildRequires:	libsidplay-devel}
BuildRequires:	libtool
#BuildRequires:	libuuid-devel
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	mpeg4ip-devel
BuildRequires:	neon-devel >= 0.25.5
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	rpm-pythonprov
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	taglib-devel >= 1.4-2
BuildRequires:	unzip
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2 >= 2:2.10.0
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires:	gstreamer-audio-effects-base >= 0.10.10
Requires:	gstreamer-audio-formats >= 0.10.3
Requires:	gstreamer-audiosink
Obsoletes:	bmpx-curses
Obsoletes:	bmpx-libs
Obsoletes:	bmpx-plugin-container
Obsoletes:	bmpx-plugin-flow
Obsoletes:	bmpx-plugins-base
Obsoletes:	bmpx-plugin-transport
Obsoletes:	bmpx-remote
Obsoletes:	bmpx-remote-gtk
Obsoletes:	bmpx-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/mozilla-firefox
%define		_chromedir	%{_firefoxdir}/chrome

%description
BMPx is the follow-up of the BMP project with a codebase rewritten
from scratch and aims to maintain a stable audio player foundation,
and to provide a player with a consistent and easy to understand usage
experience.

%description -l pl.UTF-8
BMPx jest następcą projektu BMP z przepisanym od zera kodem i skupia
się na utrzymaniu stabilnej podstawy odtwarzacza dźwięku, aby
udostępnić odtwarzacz ze spójną i łatwą do zrozumienia obsługą.

%package devel
Summary:	Header files for BMPx media player
Summary(pl.UTF-8):	Pliki nagłówkowe odtwarzacza multimedialnego BMPx
Group:		X11/Development/Libraries
Requires:	dbus-glib-devel >= 0.62
Obsoletes:	libchroma-devel
Obsoletes:	libhrel-devel

%description devel
Header files required for compiling BMPx media player plugins.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do kompilowania wtyczek odtwarzacza
multimedialnego BMPx.

%package -n mozilla-firefox-plugin-bmpx
Summary:	BMPx plugin for Mozilla Firefox
Summary(pl.UTF-8):	Wtyczka BMPx dla Mozilli Firefox
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	mozilla-firefox

%description -n mozilla-firefox-plugin-bmpx
This plugin registers the lastfm:// protocol to BMPx.

%description -n mozilla-firefox-plugin-bmpx -l pl.UTF-8
Ta wtyczka rejestruje protokół lastfm:// do BMPx.

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
	--enable-gamin \
	--enable-libnotify \
	--enable-mp4v2 \
	%{?with_ofa:--enable-ofa} \
	%{?with_sid:--enable-sid} \
	--enable-shared \
	%{?with_gaim:--enable-gaim} \
	--with-dbus-services-dir=%{_datadir}/dbus-1/services
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_chromedir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

unzip xpi/bmp.xpi -d $RPM_BUILD_ROOT%{_firefoxdir}
sed -e 's@chrome/bmp\.jar@bmp\.jar@' $RPM_BUILD_ROOT%{_firefoxdir}/chrome.manifest \
	> $RPM_BUILD_ROOT%{_chromedir}/bmp.manifest

rm -f $RPM_BUILD_ROOT%{_firefoxdir}/{install.rdf,chrome.manifest}
rm -f $RPM_BUILD_ROOT%{_datadir}/bmpx/data/GPL.txt
rm -f $RPM_BUILD_ROOT%{_libdir}/bmpx/plugins/{taglib,vfs/container,vfs/transport}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/th_TH

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor

%banner %{name} -e << EOF
Remember to install appropriate GStreamer plugins for files
you want to play:
- gstreamer-cdparanoia (for Audio-CD)
- gstreamer-flac (for FLAC)
- gstreamer-mad (for MP3s)
- gstreamer-vorbis (for Ogg Vorbis)
EOF

%postun
%update_desktop_database_postun
%update_mime_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/beep-media-player-2
%attr(755,root,root) %{_bindir}/bmp-enqueue-files-2.0 
%attr(755,root,root) %{_bindir}/bmp-enqueue-uris-2.0
%attr(755,root,root) %{_bindir}/bmp-play-files-2.0
%attr(755,root,root) %{_bindir}/bmp-play-lastfm-2.0
%attr(755,root,root) %{_libexecdir}/beep-media-player-2-bin
%attr(755,root,root) %{_libexecdir}/beep-media-player-2-sentinel

%dir %{_libdir}/bmpx
%dir %{_libdir}/bmpx/plugins
%dir %{_libdir}/bmpx/plugins/taglib
%dir %{_libdir}/bmpx/plugins/vfs
%dir %{_libdir}/bmpx/plugins/vfs/container
%dir %{_libdir}/bmpx/plugins/vfs/transport
%attr(755,root,root) %{_libdir}/bmpx/plugins/taglib/*.so*
%attr(755,root,root) %{_libdir}/bmpx/plugins/vfs/container/*.so*
%attr(755,root,root) %{_libdir}/bmpx/plugins/vfs/transport/*.so*

%{_datadir}/bmpx
%{_datadir}/dbus-1/services/*.service
%{_mandir}/man*/*
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png

%files devel
%defattr(644,root,root,755)
%{_includedir}/bmp-2.0
%{_pkgconfigdir}/*.pc

%files -n mozilla-firefox-plugin-bmpx
%defattr(644,root,root,755)
%{_chromedir}/bmp.jar
%{_chromedir}/bmp.manifest
