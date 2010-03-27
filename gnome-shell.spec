Name:           gnome-shell
Version:        2.29.1
Release:        4
Summary:        Window management and application launching for GNOME

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://live.gnome.org/GnomeShell
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gnome-shell/2.27/%{name}-%{version}.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Patch0: 0001-build-Link-against-lm.patch

%define clutter_version 1.2.2
%define gobject_introspection_version 0.6.9
%define mutter_version 2.29.1
%define gjs_version 0.6

BuildRequires:  clutter-devel >= %{clutter_version}
BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gir-repository-devel
BuildRequires:  gjs-devel >= %{gjs_version}
BuildRequires:  glib2-devel
BuildRequires:  gnome-desktop-devel
BuildRequires:  gnome-menus-devel
BuildRequires:  gobject-introspection >= %{gobject_introspection_version}
# for screencast recorder functionality
BuildRequires:  gstreamer-devel
BuildRequires:  gtk2-devel
BuildRequires:  intltool
# used in unused BigThemeImage
BuildRequires:  librsvg2-devel
BuildRequires:  mutter-devel >= %{mutter_version}

# User interface to switch to GNOME Shell
Requires:       desktop-effects
# For %pre/%post usage of gconftool-2
Requires:       GConf2
# wrapper script uses to restart old GNOME session if run --replace
# from the command line
Requires:       gobject-introspection >= %{gobject_introspection_version}
Requires:       gnome-python2-gconf
Requires:       pygobject2
# wrapper script uses to figure out available GLX capabilities
Requires:       glx-utils
# needed for loading SVG's via gdk-pixbuf
Requires:       librsvg2
# needed as it is now split from Clutter
Requires:       json-glib
Requires:       mutter >= %{mutter_version}
Requires:       gjs >= %{gjs_version}
# These are needed to run gnome-shell nested Xephyr mode, but that's a
# developer-only thing and unlikely to be interesting for a normal user
#Requires:       xorg-x11-server-Xephyr
#Requires:       xorg-x11-xauth

BuildRequires: gnome-common
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: intltool

%description
GNOME Shell provides core user interface functions for the GNOME 3 desktop,
like switching to windows and launching applications. GNOME Shell takes
advantage of the capabilities of modern graphics hardware and introduces
innovative user interface concepts to provide a visually attractive and
easy to use experience.

%prep
%setup -q
%patch0 -p1

%build
./autogen.sh
%configure

# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make V=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

rm -rf %{buildroot}/%{_libdir}/mutter/plugins/*.la

desktop-file-validate %{buildroot}%{_datadir}/applications/gnome-shell.desktop

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/gnome-shell
%{_datadir}/applications/gnome-shell.desktop
%{_datadir}/gnome-shell/
%{_mandir}/*
%{_libdir}/gnome-shell/
%{_libdir}/mutter/plugins/libgnome-shell.so
%{_sysconfdir}/gconf/schemas/gnome-shell.schemas

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/gconf/schemas/gnome-shell.schemas \
    > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/gconf/schemas/gnome-shell.schemas \
    > /dev/null || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
    %{_sysconfdir}/gconf/schemas/gnome-shell.schemas \
  > /dev/null || :

%changelog
* Sat Mar 27 2010 Colin Walters <walters@verbum.org> - 2.29.1-4
- Add an explicit Requires: on gjs.  Should resolve bug #577460

* Fri Mar 26 2010 Colin Walters <walters@verbum.org> - 2.29.1-3
- Add manpage to files
- Specify V=1 for build, readd smp_mflags since parallel is fixed upstream

* Thu Mar 25 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.29.1-2
- Bumped for new version of mutter and clutter
- Added version requirement to gjs-devel because of dependency of build

* Wed Mar 24 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.29.1-1
- Update to latest version 2.29.1

* Sun Feb 21 2010 Bastien Nocera <bnocera@redhat.com> 2.28.1-0.2.20100128git
- Require json-glib
- Rebuild for new clutter with json split out
- Fix deprecation in COGL

* Thu Jan 28 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.28.1-0.1.20100128git
- New git snapshot
- Fixed Version for alphatag use

* Fri Jan 15 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20101015git-1
- Added dependency on a git build of gobject-introspect to solve some breakage
- Also went ahead and made a new git tarball

* Tue Jan 12 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20100112git-1
- New git snapshot

* Tue Dec 07 2009 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20091206git-5
- Added libtool, glib-gettext for the libtoolize dep of git snapshot

* Mon Dec 07 2009 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20091206git-4
- Added gnome-common needed by autogen.sh in git snapshot build

* Sun Dec 06 2009 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20091206git-3
- Added the autotools needed to build the git snapshot to the build requires

* Sun Dec 06 2009 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20091206git-2
- Fixed the setup naming issue with the git snapshot directory naming

* Sun Dec 06 2009 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20091206git-1
- Update to git snapshot on 20091206

* Wed Oct  7 2009 Owen Taylor <otaylor@redhat.com> - 2.28.0-2
- Update to 2.28.0

* Tue Sep 15 2009 Owen Taylor <otaylor@redhat.com> - 2.27.3-1
- Update to 2.27.3

* Fri Sep  4 2009 Owen Taylor <otaylor@redhat.com> - 2.27.2-2
- Test for gobject-introspection version should be >= not >

* Fri Sep  4 2009 Owen Taylor <otaylor@redhat.com> - 2.27.2-1
- Update to 2.27.2
- Add an explicit dep on gobject-introspection 0.6.5 which is required 
  for the new version

* Sat Aug 29 2009 Owen Taylor <otaylor@redhat.com> - 2.27.1-4
- Fix GConf %%preun script to properly be for package removal

* Fri Aug 28 2009 Owen Taylor <otaylor@redhat.com> - 2.27.1-3
- Replace libgnomeui with gnome-desktop in BuildRequires

* Fri Aug 28 2009 Owen Taylor <otaylor@redhat.com> - 2.27.1-2
- BuildRequire intltool
- Add find_lang

* Fri Aug 28 2009 Owen Taylor <otaylor@redhat.com> - 2.27.1-1
- Update to 2.27.1
- Update Requires, add desktop-effects

* Wed Aug 12 2009 Owen Taylor <otaylor@redhat.com> - 2.27.0-4
- Add an explicit dependency on GConf2 for pre/post

* Tue Aug 11 2009 Owen Taylor <otaylor@redhat.com> - 2.27.0-3
- Add missing BuildRequires on gir-repository-devel

* Tue Aug 11 2009 Owen Taylor <otaylor@redhat.com> - 2.27.0-2
- Temporarily use a non-parallel-build until gnome-shell is fixed

* Mon Aug 10 2009 Owen Taylor <otaylor@redhat.com> - 2.27.0-1
- Initial version
