#Global macro or variable
%define atk_version 2.15.1
%define glib2_version 2.49.4
%define cairo_version 1.14.0
%define pango_version 1.41.0
%define gdk_pixbuf_version 2.30.0
%define epoxy_version 1.4
%define wayland_version 1.9.91
%define wayland_protocols_version 1.12
%define bin_version 3.0.0
%define enable_immodules_package 0
%global __provides_exclude_from %{_libdir}/gtk-3.0

#Basic Information
Name:    gtk3
Version: 3.24.30
Release: 3
Summary: GTK+ graphical user interface library
License: LGPLv2+
URL:     http://www.gtk.org
Source0: http://download.gnome.org/sources/gtk+/3.24/gtk+-%{version}.tar.xz

#Dependency
BuildRequires: pkgconfig(atk) >= %{atk_version} pkgconfig(atk-bridge-2.0)
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version} pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(cairo) >= %{cairo_version} pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires: pkgconfig(pango) >= %{pango_version} pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires: pkgconfig(xi) pkgconfig(xrandr) pkgconfig(xinerama) pkgconfig(xcomposite) pkgconfig(xdamage)
BuildRequires: pkgconfig(xkbcommon) pkgconfig(epoxy) >= %{epoxy_version}
BuildRequires: wayland-devel >= %{wayland_version} wayland-protocols-devel >= %{wayland_protocols_version}
BuildRequires: pkgconfig(colord) pkgconfig(json-glib-1.0) pkgconfig(rest-0.7)
BuildRequires: gettext gtk-doc libtool desktop-file-utils libXcursor-devel
%if 0%{?openEuler}
BuildRequires: cups-devel
%endif

Requires:      adwaita-icon-theme hicolor-icon-theme
Requires:      atk >= %{atk_version} glib2 >= %{glib2_version} pango >= %{pango_version}
Requires:      cairo >= %{cairo_version} cairo-gobject >= %{cairo_version}
Requires:      libepoxy >= %{epoxy_version}
Requires:      libwayland-client >= %{wayland_version} libwayland-cursor >= %{wayland_version}
Requires:      gdk-pixbuf2-modules libXrandr
Recommends:    dconf

Obsoletes:     adwaita-gtk3-theme < 3.13.3
Provides:      adwaita-gtk3-theme = %{version}-%{release}
Conflicts:     gtk2 < 2.24.29

Obsoletes:     gtk3-engines <= 2.91.5-5.fc15
Obsoletes:     gtk-solidity-engine < 0.4.1-9
Obsoletes:     oxygen-gtk3 < 2:1.4.1

%description
GTK+ is an object-oriented widget toolkit written in the programming language C;
it has a C-based object-oriented architecture that allows for maximum
flexibility. The GTK+ library contains a set of graphical control elements
(widgets)for creating graphical user interfaces. This package contains version 3
of GTK+.

%if 0%{?enable_immodules_package}
%package       immodules
Summary:       Input methods for GTK+
Requires:      gtk3 = %{version}-%{release}
Requires:      gtk2-immodules

%description   immodules
The gtk3-immodules package contains standalone input methods that
are shipped as part of GTK+ 3.
%endif

%package       immodule-xim
Summary:       XIM support for GTK+
Requires:      gtk3 = %{version}-%{release}

%description   immodule-xim
The gtk3-immodule-xim package contains XIM support for GTK+ 3.

%package       -n gtk-update-icon-cache
Summary:       Icon theme caching utility
Obsoletes:     gtk-update-icon-cache < %{version}-%{release}

%description   -n gtk-update-icon-cache
GTK+ can use the cache files created by gtk-update-icon-cache to avoid alot of system call and disk seek overhead when the application starts.Since the format of the cache files allows them to be mmap()ed shared between multiple applications,the overall memory consumption is reduced as well.

%package       devel
Summary:       Development files for gtk+3
Requires:      gtk3 = %{version}-%{release}

Obsoletes:     gtk3-tests < %{version}-%{release}
Provides:      gtk3-tests = %{version}-%{release}
Obsoletes:     gtk3-engines-devel <= 2.91.5-5

%description   devel
This package contains the libraries, header files other development files for
GTK+ 3.

%package       help
Summary:       Documents for gtk3
Requires:      gtk3 = %{version}-%{release}

Obsoletes:     gtk3-devel-docs < %{version}-%{release}
Provides:      gtk3-devel-docs = %{version}-%{release}

%description   help
This package contains man pages and other related documents for gtk3.

#Build sections
%prep
%autosetup -n gtk+-%{version} -p1

%build
export CFLAGS='-fno-strict-aliasing %optflags'
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
%configure $CONFIGFLAGS \
        --enable-xkb \
        --enable-xinerama \
        --enable-xrandr \
        --enable-xfixes \
        --enable-xcomposite \
        --enable-xdamage \
        --enable-x11-backend \
        --enable-wayland-backend \
        --enable-broadway-backend \
        --enable-colord \
        --enable-installed-tests \
        --with-included-immodules=wayland \
	%if !0%{?openEuler}
	--disable-cups
	%endif
)

# fight unused direct deps
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}

%install
%make_install RUN_QUERY_IMMODULES_TEST=false

%find_lang gtk30
%find_lang gtk30-properties

(cd $RPM_BUILD_ROOT%{_bindir}
mv gtk-query-immodules-3.0 gtk-query-immodules-3.0-64
)

echo ".so man1/gtk-query-immodules-3.0.1" > $RPM_BUILD_ROOT%{_mandir}/man1/gtk-query-immodules-3.0-64.1

# rm unpackaged files
find $RPM_BUILD_ROOT -name '*.la' -delete

touch $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/immodules.cache

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-3.0
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/modules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/immodules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/theming-engines

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%transfiletriggerin -- %{_libdir}/gtk-3.0/3.0.0/immodules
gtk-query-immodules-3.0-64 --update-cache &>/dev/null || :

%transfiletriggerpostun -- %{_libdir}/gtk-3.0/3.0.0/immodules
gtk-query-immodules-3.0-64 --update-cache &>/dev/null || :

#Install and uninstall scripts
%pre

%preun

%post

%postun

#Files list
%files -f gtk30.lang
%license COPYING
%{_bindir}/broadwayd
%{_bindir}/gtk-launch
%{_bindir}/gtk-query-immodules-3.0*
%{_libdir}/libgtk-3.so.*
%{_libdir}/libgdk-3.so.*
%{_libdir}/libgailutil-3.so.*
%dir %{_libdir}/gtk-3.0
%dir %{_libdir}/gtk-3.0/%{bin_version}
%dir %{_datadir}/gtk-3.0
%{_libdir}/gtk-3.0/%{bin_version}/theming-engines
%dir %{_libdir}/gtk-3.0/%{bin_version}/immodules
%{_libdir}/gtk-3.0/%{bin_version}/printbackends
%{_libdir}/gtk-3.0/modules
%{_libdir}/gtk-3.0/immodules
%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_libdir}/girepository-1.0
%ghost %{_libdir}/gtk-3.0/%{bin_version}/immodules.cache
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.Debug.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.EmojiChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.exampleapp.gschema.xml
%if ! 0%{?enable_immodules_package}
%exclude %{_libdir}/gtk-3.0/%{bin_version}/immodules/*
%exclude %{_sysconfdir}/gtk-3.0/im-multipress.conf
%endif

%files -n gtk-update-icon-cache
%license COPYING
%{_bindir}/gtk-update-icon-cache

%if 0%{?enable_immodules_package}
%files immodules
%config(noreplace) %{_sysconfdir}/gtk-3.0/im-multipress.conf
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-am-et.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-broadway.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-cedilla.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-cyrillic-translit.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-inuktitut.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ipa.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-multipress.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-thai.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ti-er.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ti-et.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-viqr.so
%endif

%files immodule-xim
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-xim.so

%files devel -f gtk30-properties.lang
%{_libdir}/lib*.so
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_bindir}/gtk3-demo
%{_bindir}/gtk3-icon-browser
%{_bindir}/gtk-builder-tool
%{_bindir}/gtk-encode-symbolic-svg
%{_bindir}/gtk-query-settings
%{_datadir}/gtk-3.0/valgrind/gtk.supp
%{_datadir}/applications/gtk3-demo.desktop
%{_datadir}/applications/gtk3-icon-browser.desktop
%{_datadir}/applications/gtk3-widget-factory.desktop
%{_datadir}/icons/hicolor/*/apps/gtk3-demo.png
%{_datadir}/icons/hicolor/*/apps/gtk3-demo-symbolic.symbolic.png
%{_datadir}/icons/hicolor/*/apps/gtk3-widget-factory.png
%{_datadir}/icons/hicolor/*/apps/gtk3-widget-factory-symbolic.symbolic.png
%{_bindir}/gtk3-demo-application
%{_bindir}/gtk3-widget-factory
%{_datadir}/gettext/
%{_datadir}/gtk-3.0/gtkbuilder.rng
%{_datadir}/gir-1.0
%{_datadir}/glib-2.0/schemas/org.gtk.Demo.gschema.xml
%{_libexecdir}/installed-tests/gtk+
%{_datadir}/installed-tests

%files help
%doc AUTHORS NEWS README
%{_datadir}/gtk-doc
%{_mandir}/man1/broadwayd.1*
%{_mandir}/man1/gtk-builder-tool.1*
%{_mandir}/man1/gtk-encode-symbolic-svg.1*
%{_mandir}/man1/gtk-launch.1*
%{_mandir}/man1/gtk-query-immodules-3.0*
%{_mandir}/man1/gtk-query-settings.1*
%{_mandir}/man1/gtk-update-icon-cache.1*
%{_mandir}/man1/gtk3-demo.1*
%{_mandir}/man1/gtk3-demo-application.1*
%{_mandir}/man1/gtk3-icon-browser.1*
%{_mandir}/man1/gtk3-widget-factory.1*

%changelog
* Tue Mar 08 2022 Wenlong Ding <wenlong.ding@turbolinux.com.cn> - 3.24.30-3
- Remove 'Provides: gtk-update-icon-cache' from gtk3 package

* Fri Jan 14 2022 wangkerong <wangkerong@huawei.com> - 3.24.30-2
- Other distros disable cups

* Tue Dec 14 2021 liuyumeng <liuyumeng5@huawei.com> - 3.24.30-1
- update to gtk3-3.24.30-1

* Wed Nov 03 2021 liuyumeng <liuyumeng5@huawei.com> - 3.24.29-3
- Split the update-icon-cache sub-package from the main package

* Wed Jun 23 2021 chenbo pan <panchenbo@uniontech.com> - 3.24.29-2
- Fix virt-manager 'NoneType' object has no attribute 'conn' error

* Wed May 19 2021 weijin deng <weijin.deng@turbolinux.com.cn> - 3.24.29-1
- Upgrade to 3.24.29
- Update Version
- Delete '^' char

* Wed Dec 23 2020 huanghaitao <huanghaitao8@huawei.com> - 3.24.22-1
- update gtk3.24.22

* Thu Jul 23 2020 hanhui <hanhui15@huawei.com> - 3.24.21-1
- update gtk3.24.21

* Tue Jun 23 2020 hanhui <hanhui15@huawei.com> - 3.24.20-1
- update gtk3.24.20

* Sat Mar 14 2020 songnannan <songnannan2@huawei.com> - 3.24.1-3
- disable package

* Wed Sep 18 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.24.1-2
- Package init

