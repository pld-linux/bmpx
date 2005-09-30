#
Summary:	Sound player with the WinAmp GUI, for Unix-based systems for GTK+2
Summary(pl):	Odtwarzacz d¼wiêku z interfejsem WinAmpa dla GTK+2
Name:		bmpx
Version:	0.11.5
Release:	0.1
Epoch:		1
License:	GPL
Group:		Applications/Sound
Source0:	http://download.berlios.de/bmpx/%{name}-%{version}.tar.gz
# Source0-md5:	b70f812629eb28db0b55f897f2353a5d
Source1:	mp3license
URL:		http://www.sosdg.org/~larne/w/BMP_Homepage
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	curl-devel
BuildRequires:	esound-devel >= 0.2.8
BuildRequires:	fam-devel
BuildRequires:  GConf2-devel >= 2.4.0
BuildRequires:  gnome-vfs2-devel >= 2.4.0
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	home-etc-devel
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	libglade2-devel >= 2.5.1
BuildRequires:	pkgconfig
BuildRequires:	taglib-devel
BuildRequires:	xine-lib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BMPx is a media player based on XMMS (http://www.xmms.org/). The
primary goals of this fork are UI enhancements with latest technology
(GTK+2, Pango), and usability while maintaining the skinned UI.

%description -l pl
BMPx to odtwarzacz mediów oparty na XMMS-ie (http://www.xmms.org/).
G³ówne cele tego odga³êzienia to rozszerzenie interfejsu u¿ytkownika o
najnowsze technologie (GTK+2, Pango) i ergonomia interfejsu
obs³uguj±cego skórki.

%prep
%setup -q

%build
rm -rf autom4te.cache
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%ifarch %{ix86}
%ifnarch i386 i486
	--enable-simd \
%endif
%else
	--disable-simd \
%endif
	--enable-gnome-vfs \
	--enable-gconf \
	--enable-shared
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:

%postun
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bmp*
%{_mandir}/man*/*
%{_desktopdir}/*
%{_datadir}/bmpx
%{_datadir}/bmp-remote
%{_iconsdir}/*/*/*/*
