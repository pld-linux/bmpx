#
# Conditional build:
%bcond_with	gstreamer	# build with GStreamer support (instead of XINE)
#
Summary:	Sound player with the WinAmp GUI, for Unix-based systems for GTK+
Summary(pl):	Odtwarzacz d¼wiêku z interfejsem WinAmpa dla GTK+
Name:		bmpx
Version:	0.12.1
Release:	1
License:	GPL v2
Group:		X11/Applications/Sound
Source0:	http://download.berlios.de/bmpx/%{name}-%{version}.tar.gz
# Source0-md5:	40965fe0e9707a49a773c91eff777fb2
Source1:	mp3license
Patch0:		%{name}-embedded-images.patch
Patch1:		%{name}-desktop.patch
URL:		http://bmpx.berlios.de/
BuildRequires:	autoconf
BuildRequires:	automake
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
# there is no gstreamer 0.9.x in PLD cvs yet!
BuildRequires:	gstreamer-devel >= 0.9.1
%else
BuildRequires:	xine-lib-devel
%endif
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	%{name}-plugin-flow = %{epoch}:%{version}-%{release}
Requires:	%{name}-plugin-container = %{epoch}:%{version}-%{release}
Requires:	%{name}-plugin-transport = %{epoch}:%{version}-%{release}
%if %{with gstreamer}
Requires:	gstreamer-audio-effects
Requires:	gstreamer-audio-formats
Requires:	gstreamer-audiosink
%else
Requires:	xine-plugin-audio
%endif
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
Summary:	BMPx player library
Summary(pl):	Biblioteka odtwarzacza BMPx
Group:		X11/Development/Libraries

%description libs
BMPx player library.

%description libs -l pl
Biblioteka odtwarzacza BMPx.

%package devel
Summary:	Header files for BMPx media player
Summary(pl):	Pliki nag³ówkowe odtwarzacza multimedialnego BMPx
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files required for compiling BMPx media player plugins.

%description devel -l pl
Pliki nag³ówkowe potrzebne do kompilowania wtyczek odtwarzacza
multimedialnego BMPx.

%package static
Summary:	Static BMPx library
Summary(pl):	Statyczna biblioteka BMPx
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static BMPx library.

%description static -l pl
Statyczna biblioteka BMPx.

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

%package remote-curses
Summary:	BMPx python status watcher
Summary(pl):	Obserwator statusu BMPx w pythonie
Group:		X11/Applications/Sound
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description remote-curses
BMPx python status watcher (CLI interface).

%description remote-curses -l pl
Obserwator statusu BMPx w pythonie (interfejs CLI).

%package remote-gtk
Summary:	BMPx python status watcher
Summary(pl):	Obserwator statusu BMPx w pythonie
Group:		X11/Applications/Sound
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python-pygtk-glade

%description remote-gtk
BMPx python status watcher (GTK+ interface).

%description remote-gtk -l pl
Obserwator statusu BMPx w pythonie (interfejs GTK+).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
	--enable-static
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

rm -f $RPM_BUILD_ROOT%{_libdir}/bmpx/plugins/*/*.{a,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:

%if %{with gstreamer}
%banner %{name} -e << EOF
Remember to install appropriate GStreamer plugins for files
you want to play:
- gstreamer-flac (for FLAC)
- gstreamer-mad (for MP3s)
- gstreamer-vorbis (for Ogg Vorbis)
EOF
%else
%banner %{name} -e << EOF
Remember to install appropriate xine-decode plugins for files
you want to play:
- xine-decode-flac (for FLAC)
- xine-decode-ogg (for Ogg Vorbis)
EOF
%endif

%postun
if [ $1 = 0 ]; then
    umask 022
    [ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/bmpx
%attr(755,root,root) %{_bindir}/bmp-dbus-*
%dir %{_libdir}/bmpx
%dir %{_libdir}/bmpx/plugins
%{_mandir}/man*/*
%{_datadir}/bmpx
%{_desktopdir}/*
%{_pixmapsdir}/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libskinned.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libskinned.so
%{_libdir}/libskinned.la
%{_includedir}/bmpx

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

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

%files remote-curses
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bmpty

%files remote-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bmp-remote-pygtk
%{_datadir}/bmp-remote
