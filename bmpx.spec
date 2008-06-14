#
# Conditional build:
%bcond_without	sid	# build without sid support
#
Summary:	Sound player with the WinAmp GUI, for Unix-based systems for GTK+
Summary(pl.UTF-8):	Odtwarzacz dźwięku z interfejsem WinAmpa dla GTK+
Name:		bmpx
Version:	0.40.14
Release:	1
License:	GPL v2
Group:		X11/Applications/Sound
Source0:	http://files.backtrace.info/releases/0.40/%{name}-%{version}.tar.bz2
# Source0-md5:	c741e05a82a82b14b6775d44a7c93c15
Patch0:		%{name}-lib64.patch
Patch1:		%{name}-libsoup24.patch
Patch2:		%{name}-invalid-conversion.patch
URL:		http://bmpx.backtrace.info/
BuildRequires:	alsa-lib-devel >= 1.0.9
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.8
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	cairomm-devel >= 0.6.0
BuildRequires:	cdparanoia-III-devel
BuildRequires:	dbus-glib-devel >= 0.62
BuildRequires:	gcc-c++ >= 5:4.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.10
BuildRequires:	gtkmm-devel >= 2.10.0
BuildRequires:	hal-devel >= 0.5.7.1
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libglademm-devel >= 2.6.0
BuildRequires:	libmodplug-devel >= 0.7
BuildRequires:	libofa-devel >= 0.9.3
BuildRequires:	librsvg-devel >= 1:2.14.0
BuildRequires:	libsexymm-devel >= 0.1.9
%{?with_sid:BuildRequires:	libsidplay-devel}
BuildRequires:	libsigc++-devel >= 2.0.0
BuildRequires:	libsoup-devel >= 2.4.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel >= 3.3.11
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	taglib-devel >= 1.4-2
BuildRequires:	unzip
BuildRequires:	xorg-lib-libSM-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2 >= 2:2.10.0
Requires(post,postun):	hicolor-icon-theme
Requires:	gstreamer-audiosink
Suggests:	gstreamer-aac
Suggests:	gstreamer-audio-formats >= 0.10.3
Suggests:	gstreamer-cdparanoia
Suggests:	gstreamer-ffmpeg
Suggests:	gstreamer-flac
Suggests:	gstreamer-mad
Suggests:	gstreamer-mms
Suggests:	gstreamer-musepack
Suggests:	gstreamer-plugins-bad
Suggests:	gstreamer-sid
Suggests:	gstreamer-vorbis
Obsoletes:	bmpx-curses
Obsoletes:	bmpx-libs
Obsoletes:	bmpx-plugin-container
Obsoletes:	bmpx-plugin-flow
Obsoletes:	bmpx-plugin-transport
Obsoletes:	bmpx-plugins-base
Obsoletes:	bmpx-remote
Obsoletes:	bmpx-remote-gtk
Obsoletes:	bmpx-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_datadir}/mozilla-firefox
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
Requires:	mozilla-firefox >= 2.0.0.1-2

%description -n mozilla-firefox-plugin-bmpx
This plugin registers the lastfm:// protocol to BMPx.

%description -n mozilla-firefox-plugin-bmpx -l pl.UTF-8
Ta wtyczka rejestruje protokół lastfm:// do BMPx.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-hal \
	--enable-modplug \
	%{?with_sid:--enable-sid} \
	--with-dbus-services-dir=%{_datadir}/dbus-1/services
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_chromedir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

unzip -q -o xpi/bmp.xpi -d $RPM_BUILD_ROOT%{_firefoxdir}
sed -e 's@chrome/bmp\.jar@bmp\.jar@' $RPM_BUILD_ROOT%{_firefoxdir}/chrome.manifest \
	> $RPM_BUILD_ROOT%{_chromedir}/bmp.manifest

rm -f $RPM_BUILD_ROOT%{_firefoxdir}/{install.rdf,chrome.manifest}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/bmpx/plugins/{taglib,vfs/container,vfs/transport}/*.la
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{th_TH,th}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/beep-media-player-2
%attr(755,root,root) %{_bindir}/bmp-play-files-2.0
%attr(755,root,root) %{_bindir}/bmp-play-uris-2.0
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
%{_docdir}/bmpx
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
