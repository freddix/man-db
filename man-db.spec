# based on PLD Linux spec git://git.pld-linux.org/packages/.git
Summary:	Tools for searching and reading man pages
Name:		man-db
Version:	2.7.1
Release:	1
License:	GPL v2+ and GPL v3+
Group:		Base
URL:		http://www.nongnu.org/man-db/
Source0:	http://download.savannah.gnu.org/releases/man-db/%{name}-%{version}.tar.xz
# Source0-md5:	88d32360e2ed18e05de9b528ad336fd8
Source1:	%{name}.service
Source2:	%{name}.timer
# use old format of nroff output - from Fedora
Patch0:		%{name}-nroff.patch
BuildRequires:	gdbm-devel
BuildRequires:	gettext
BuildRequires:	groff
BuildRequires:	less
BuildRequires:	libpipeline-devel
BuildRequires:	zlib-devel
Requires:	coreutils
Requires:	grep
Requires:	groff
Requires:	gzip
Requires:	less
Provides:	man-pages-reader = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cache	/var/cache/man

%description
The man-db package includes five tools for browsing man-pages: man,
whatis, apropos, manpath and lexgrog. man preformats and displays
manual pages. whatis searches the manual page names. apropos searches
the manual page names and descriptions. manpath determines search path
for manual pages. lexgrog directly reads header information in manual
pages.

%prep
%setup -q
%patch0 -p1

%{__sed} -i 's/man\ root/root\ root/' init/systemd/man-db.conf

%build
%configure\
	--disable-setuid	\
	--disable-silent-rules	\
	--with-browser=elinks	\
	--with-sections="1 1p 8 2 3 3p 4 5 6 7 9 0p n l p o 1x 2x 3x 4x 5x 6x 7x 8x"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# move the documentation to relevant place
mv $RPM_BUILD_ROOT%{_datadir}/doc/man-db/* ./

# remove libtool archives
%{__rm} $RPM_BUILD_ROOT%{_libdir}/man-db/*.la

# install cache directory
install -d $RPM_BUILD_ROOT%{cache}

# install systemd service and timer files
install -d $RPM_BUILD_ROOT%{systemdunitdir}/timers.target.wants
install %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}
ln -s ../man-db.timer $RPM_BUILD_ROOT%{systemdunitdir}/timers.target.wants/man-db.timer

%find_lang %{name}
%find_lang %{name}-gnulib
cat %{name}-gnulib.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- %{name} < 2.7.0
umask 022
/usr/bin/mandb -c --quiet

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README man-db-manual.txt man-db-manual.ps docs/COPYING ChangeLog NEWS
%config(noreplace) %{_sysconfdir}/man_db.conf
%attr(755,root,root) %{_sbindir}/accessdb
%attr(755,root,root) %{_bindir}/man
%attr(755,root,root) %{_bindir}/whatis
%attr(755,root,root) %{_bindir}/apropos
%attr(755,root,root) %{_bindir}/manpath
%attr(755,root,root) %{_bindir}/lexgrog
%attr(755,root,root) %{_bindir}/catman
%attr(755,root,root) %{_bindir}/mandb
%dir %{_libdir}/man-db
%attr(755,root,root) %{_libdir}/man-db/globbing
%attr(755,root,root) %{_libdir}/man-db/manconv
%attr(755,root,root) %{_libdir}/man-db/zsoelim
%{_libdir}/man-db/*.so
%dir %{cache}
%{_mandir}/man1/apropos.1*
%{_mandir}/man1/lexgrog.1*
%{_mandir}/man1/man.1*
%{_mandir}/man1/manconv.1*
%{_mandir}/man1/manpath.1*
%{_mandir}/man1/whatis.1*
%{_mandir}/man5/manpath.5*
%{_mandir}/man8/accessdb.8*
%{_mandir}/man8/catman.8*
%{_mandir}/man8/mandb.8*
# systemd files
%{_prefix}/lib/tmpfiles.d/man-db.conf
%{systemdunitdir}/timers.target.wants/man-db.timer
%{systemdunitdir}/man-db.service
%{systemdunitdir}/man-db.timer

