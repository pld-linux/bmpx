#
# Conditional build:
%bcond_with	gstreamer	# build with GStreamer support (instead of XINE)
#
Summary:	Sound player with the WinAmp GUI, for Unix-based systems for GTK+2
Summary(pl):	Odtwarzacz d¼wiêku z interfejsem WinAmpa dla GTK+2
Name:		bmpx
Version:	0.11.5.1
Release:	0.1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://download.berlios.de/bmpx/%{name}-%{version}.tar.gz
# Source0-md5:	f0b89bb96fd8b14cfd805f4a726b4f16
Source1:	mp3license
URL:		http://bmpx.berlios.de/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	curl-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	esound-devel >= 0.2.8
BuildRequires:	fam-devel
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	taglib-devel
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= 0.9.1
%else
BuildRequires:	xine-lib-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BMPx is the follow-up of the BMP project with a codebase rewritten
from scratch and aims to maintain a stable audio player foundation,
and to provide a player with a consistent and easy to understand usage
experience.

%description -l pl
BMPx jest nastêpc± projektu BMP z przepisanym od zera kodem i skupia
siê na utrzymaniu stabilnej podstawy odtwarzacza audio, aby udostêpniæ
odtwarzacz ze spójn± i ³atw± do zrozumienia obs³ug±.

%prep
%setup -q

%build
rm -rf autom4te.cache
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%if %{with gstreamer}
	--enable-gst \
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
%attr(755,root,root) %{_bindir}/bmp*
%{_mandir}/man*/*
%{_desktopdir}/*
%{_datadir}/bmpx
%{_datadir}/bmp-remote
%{_pixmapsdir}/*
%attr(755,root,root) %{_libdir}/libskinned.so.*
