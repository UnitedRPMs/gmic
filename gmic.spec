#
# spec file for package gmic
#
# Copyright (c) 2021 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#

%global gimpplugindir %{_libdir}/gimp/2.0/plug-ins
%global soname %(c=%{version}; echo ${c//./})
%global basoname %(c=%{soname}; echo ${c:0:1})

%global debug_package %{nil}
%global _lto_cflags %{nil}
%define _legacy_common_support 1


# We have problems compiling zart in gmic 2.7.5
# https://github.com/c-koi/zart/issues/13
%bcond_with zart

# Conditional system cimg
%bcond_with system_cimg


# Only for test usage
%global gmic_commit 6be0a89816e35ecb169afe739c2f35d1dc94defd
%global shortcommit0 %(c=%{gmic_commit}; echo ${c:0:7})

%global zart_commit 939cf381c5871e506aabd066037acf2b55143c1d
%global shortcommit1 %(c=%{zart_commit}; echo ${c:0:7})

%global gmic_qt_commit 1c181e0e903760ba6e82cfdc754e1586854bd6ac
%global shortcommit2 %(c=%{gmic_qt_commit}; echo ${c:0:7})

%global gmic_community_commit 03869cb264cfbb5cc1cf5d7cde55f2fe0dbb99cd
%global shortcommit3 %(c=%{gmic_community_commit}; echo ${c:0:7})


Summary: GREYC's Magic for Image Computing
Name: gmic
Version: 2.9.9
Release: 7%{?dist}
Source0: https://github.com/dtschump/gmic/archive/%{gmic_commit}.tar.gz#/gmic-%{shortcommit0}.tar.gz 
#Source0: https://github.com/dtschump/gmic/archive/v.%{version}.tar.gz
# GIT archive snapshot of https://github.com/c-koi/zart
Source1: https://github.com/c-koi/zart/archive/%{zart_commit}.tar.gz#/zart-%{shortcommit1}.tar.gz
# GIT archive snapshot of https://github.com/c-koi/gmic-qt
Source2: https://github.com/c-koi/gmic-qt/archive/%{gmic_qt_commit}.tar.gz#/gmic-qt-%{shortcommit2}.tar.gz
# GIT archive snapshot of https://github.com/dtschump/gmic-community
Source3: https://github.com/dtschump/gmic-community/archive/%{gmic_community_commit}.tar.gz#/gmic-community-%{shortcommit3}.tar.gz
# CImg.h header same version to gmic
# https://github.com/dtschump/CImg
Source4: https://raw.githubusercontent.com/dtschump/CImg/b33dcc8f9f1acf1f276ded92c04f8231f6c23fcd/CImg.h
Patch:	gmic-2.9.1-optflags.patch
Patch1: gmic-openexr3.patch
#Patch1: file.patch
Patch2: cimg_OpenEXR.patch
License: (CeCILL or CeCILL-C) and GPLv3+
Url: http://gmic.eu/
%if %{with system_cimg}
BuildRequires: CImg-devel 
%endif
BuildRequires: libX11-devel
BuildRequires: libXext-devel
#BuildRequires: libtiff-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: fftw-devel
BuildRequires: zlib-devel
BuildRequires: gimp-devel-tools
BuildRequires: hdf5-devel
BuildRequires: opencv-devel >= 4.5.2
BuildRequires: opencv-xfeatures2d-devel >= 4.5.2
BuildRequires: GraphicsMagick-c++-devel
BuildRequires: ilmbase-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: libcurl-devel
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gimp-devel-tools
BuildRequires: bash-completion
BuildRequires: libxkbcommon-devel
BuildRequires: wget
BuildRequires: dos2unix
%if 0%{?fedora} <= 34
BuildRequires:  OpenEXR-devel
%else
BuildRequires:  openexr-devel
BuildRequires:  imath-devel
%endif
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5Xml)

BuildRequires:  pkgconfig(GraphicsMagick++)
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(gimp-2.0)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(zlib)


# The C library binding was mistakenly put in a -static
# package despite being a shared library
Obsoletes: gmic-static <= 2.1.8

%description
G'MIC is an open and full-featured framework for image processing, providing
several different user interfaces to convert/manipulate/filter/visualize
generic image datasets, from 1d scalar signals to 3d+t sequences of
multi-spectral volumetric images.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Development files for G'MIC

%package gimp
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: G'MIC plugin for GIMP

%description devel
G'MIC is an open and full-featured framework for image processing, providing
several different user interfaces to convert/manipulate/filter/visualize
generic image datasets, from 1d scalar signals to 3d+t sequences of
multi-spectral volumetric images.

Provides files for building applications against the G'MIC API

%description gimp
G'MIC is an open and full-featured framework for image processing, providing
several different user interfaces to convert/manipulate/filter/visualize
generic image datasets, from 1d scalar signals to 3d+t sequences of
multi-spectral volumetric images.

Provides a plugin for using G'MIC from GIMP

%package krita
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: G'MIC plugin for krita

%description krita
Krita plugin for the G'MIC image processing framework

%prep
%setup -n gmic-%{gmic_commit} -a 1 -a 2 -a 3 
# We are using commits updated...
rm -rf zart gmic-qt gmic-community
mv -f zart-%{zart_commit} zart 
mv -f gmic-qt-%{gmic_qt_commit} gmic-qt
mv -f gmic-community-%{gmic_community_commit} gmic-community

#patches
%patch -p1
%if 0%{?fedora} >= 35
%patch1 -p1
%endif
%patch2 -p1 -d %{_sourcedir}

# fixes
dos2unix src/Makefile

# fix libdir
sed 's|\$(USR)/\$(LIB)/|$(USR)/%_lib/|' src/Makefile
# fix libcgmic path
sed 's| \.\.\/\(\.\.\/gmic-community/libcgmic\)| \1|' src/Makefile
#%ifnarch %ix86 x86_64
#sed 's|-mtune=generic||' src/Makefile
#%endif


#-------- opencv 4 fix--------
# for zart
sed -e 's|opencv|opencv4|' -i zart/zart.pro
rm -f zart/.qmake.stash


# fix overlinking
sed -e 's/pkg-config opencv --libs ||//' -e 's/-lopencv_highgui/-lopencv_videoio/' \
      -e 's/pkg-config opencv/pkg-config opencv4/' -i src/Makefile   
#------------------------------

# qmake fix
sed -i 's|QMAKE = qmake|QMAKE = qmake-qt5|g' src/Makefile

# remove stash-file (thanks Wolfgang Lieff <Wolfgang.Lieff@airborneresearch.org.au>)
rm -f zart/.qmake.stash

%build


pushd src

ln -fs ../gmic-community/libcgmic/gmic_libc.cpp .
ln -fs ../gmic-community/libcgmic/gmic_libc.h .
ln -fs ../gmic-community/libcgmic/use_libcgmic.c .

%if %{with system_cimg}
# We want to build against the system installed CImg package.
# G'MIC provides no way todo this, so we just copy the file
# over what's there already
#mv CImg.h CImg.h.bak
cp -f /usr/include/CImg.h CImg.h
%if 0%{?fedora} >= 35
sed 's|"ImfRgbaFile.h"|"OpenEXR/ImfRgbaFile.h"|' CImg.h
%endif
echo 'CImg from System'
%else
mv -f %{S:4} .
echo 'CImg from URL'
%endif

export CC=gcc
export CXX=g++
make LIB=lib64 OPT_CFLAGS="-O2 -fPIC -fno-fast-math" cli lib libc 
popd

echo 'DONE MAKE'
	export CCACHE_DISABLE=1
	export CC=gcc
        export CXX=g++
  pushd gmic-qt
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on HOST=none
  %make_build VERBOSE=0
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on HOST=gimp
  %make_build VERBOSE=0
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on HOST=krita
  %make_build VERBOSE=0
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on HOST=digikam
  %make_build VERBOSE=0
  popd

%if !%{with zart}
  pushd zart
  unset CXXFLAGS 
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src zart.pro 
  %make_build VERBOSE=0
  popd
%endif

# build libc
pushd src  
export CC=gcc
export CXX=g++
%make_build libc NOSTRIP=1
popd

%install

%make_install -C src LIB=lib64 USR="/usr"


pushd src
VERSION0=$(grep 'gmic_version\ ' gmic.h | tail -c4 | head -c3)
VERSION1=$(grep 'gmic_version\ ' gmic.h | tail -c4 | head -c1)
VERSION2=$(grep 'gmic_version\ ' gmic.h | tail -c3 | head -c1)
VERSION3=$(grep 'gmic_version\ ' gmic.h | tail -c2 | head -c1)

# symlink
cp -f libgmic.so %{buildroot}/%{_libdir}/libgmic.so.${VERSION1}
cp -f libcgmic.so %{buildroot}/%{_libdir}/libcgmic.so.${VERSION1}

# install libc
#cp -f libcgmic.so %{buildroot}/%{_libdir}/libcgmic.so.${VERSION0}
cp -f gmic_libc*.h %{buildroot}/%{_includedir}/
popd


# install gmic qt for gimp and krita
pushd gmic-qt

%if !%{with zart}
install -Dm755 ../zart/zart -t %{buildroot}/usr/bin
%endif

install -dm 755 %{buildroot}/%{gimpplugindir}/
install -Dm755 gmic_gimp_qt %{buildroot}/%{gimpplugindir}/
install -Dm644 ../resources/gmic_cluts.gmz %{buildroot}/%{gimpplugindir}/

install -Dm755 gmic_qt %{buildroot}/usr/bin/
install -Dm755 gmic_krita_qt %{buildroot}/usr/bin/
popd

if [ -f %{_target_platform}/resources/gmic_bashcompletion.sh ]; then 
pushd %{_target_platform}/resources/
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d/
cp -f gmic_bashcompletion.sh  %{buildroot}/%{_sysconfdir}/bash_completion.d/gmic
popd
# Sourced files shouldn't be executable
chmod -x %{buildroot}/%{_sysconfdir}/bash_completion.d/gmic
fi

 

# COPYING fix
mv $PWD/gmic-community/libcgmic/COPYING COPYING-libcgmic 
mv $PWD/gmic-qt/COPYING COPYING-gmic-qt 

# cmake fix, using the correct soname for the release
#sed -i "s|libgmic.so.1|libgmic.so.${VERSION1}|g" $RPM_BUILD_ROOT/%{_libdir}/cmake/gmic/GmicTargets-release.cmake

%ldconfig_scriptlets

%files
%doc README
%license COPYING COPYING-gmic-qt COPYING-libcgmic
%{_bindir}/gmic
%{_bindir}/gmic_qt
%if !%{with zart}
%{_bindir}/zart
%endif
%{_libdir}/libgmic.so.*
%{_libdir}/libcgmic.so.*
#{_mandir}/man1/%{name}.1.gz
#{_datadir}/bash-completion/completions/gmic
%{_datadir}/applications/gmic_qt.desktop
%{_datadir}/applications/zart.desktop
%{_datadir}/icons/hicolor/48x48/apps/gmic_qt.png
%{_datadir}/icons/hicolor/48x48/apps/zart.png
%{_datadir}/icons/hicolor/scalable/apps/gmic_qt.svg
%{_datadir}/icons/hicolor/scalable/apps/zart.svg


%files devel
%{_prefix}/include/gmic.h
%{_prefix}/include/gmic_libc.h
%{_libdir}/libgmic.so
%{_libdir}/libcgmic.so

%files gimp
%{gimpplugindir}/gmic_gimp_qt
%{gimpplugindir}/gmic_cluts.gmz

%files krita
%{_bindir}/gmic_krita_qt

%changelog

* Fri Sep 10 2021 - David Va <davidva AT tuta DOT io> 2.9.9-7
- Updated to 2.9.9

* Sun Aug 01 2021 - David Va <davidva AT tuta DOT io> 2.9.8-7
- Updated to 2.9.8

* Sat Apr 17 2021 - David Va <davidva AT tuta DOT io> 2.9.7-7
- Updated to 2.9.7

* Mon Feb 15 2021 - David Va <davidva AT tuta DOT io> 2.9.6-7
- Updated to 2.9.6

* Sat Dec 05 2020 - David Va <davidva AT tuta DOT io> 2.9.4-7
- Updated to 2.9.4

* Wed Nov 18 2020 - David Va <davidva AT tuta DOT io> 2.9.3-7
- Updated to 2.9.3

* Thu Nov 05 2020 - David Va <davidva AT tuta DOT io> 2.9.2-8
- Rebuilt for opencv

* Mon Sep 14 2020 - David Va <davidva AT tuta DOT io> 2.9.2-7
- Updated to 2.9.2

* Tue Aug 11 2020 - David Va <davidva AT tuta DOT io> 2.9.1-8
- Rebuilt for opencv

* Thu Jun 11 2020 - David Va <davidva AT tuta DOT io> 2.9.1-7
- Updated to 2.9.1

* Mon Apr 27 2020 - David Va <davidva AT tuta DOT io> 2.9.0-8
- Rebuilt for opencv

* Tue Mar 31 2020 - David Va <davidva AT tuta DOT io> 2.9.0-7
- Updated to 2.9.0

* Tue Feb 11 2020 - David Va <davidva AT tuta DOT io> 2.8.4-7
- Updated to 2.8.4

* Sat Jan 25 2020 - David Va <davidva AT tuta DOT io> 2.8.3-7
- Updated to 2.8.3-7

* Thu Jan 16 2020 - David Va <davidva AT tuta DOT io> 2.8.2-7
- Updated to 2.8.2-7

* Sun Dec 29 2019 - David Va <davidva AT tuta DOT io> 2.8.1-8
- Rebuilt for opencv

* Fri Dec 20 2019 - David Va <davidva AT tuta DOT io> 2.8.1-7
- Updated to 2.8.1

* Fri Dec 13 2019 - David Va <davidva AT tuta DOT io> 2.8.0-7
- Updated to 2.8.0

* Sat Oct 26 2019 - David Va <davidva AT tuta DOT io> 2.7.5-7
- Updated to 2.7.5

* Mon Oct 21 2019 - David Va <davidva AT tuta DOT io> 2.7.4-7
- Updated to 2.7.4

* Tue Oct 08 2019 - David Va <davidva AT tuta DOT io> 2.7.3-7
- Updated to 2.7.3

* Fri Oct 04 2019 - David Va <davidva AT tuta DOT io> 2.7.2-7
- Updated to 2.7.2

* Tue Sep 03 2019 - David Va <davidva AT tuta DOT io> 2.7.1-7
- Updated to 2.7.1

* Thu Aug 22 2019 - David Va <davidva AT tuta DOT io> 2.7.0-8
- Updated to 2.7.0
- Changed to Cmake because reduce build time and resources

* Sat Aug 03 2019 - David Va <davidva AT tuta DOT io> 2.6.5-8
- Rebuilt for opencv

* Tue Jun 11 2019 - David Va <davidva AT tuta DOT io> 2.6.5-7
- Updated to 2.6.5

* Fri May 24 2019 - David Va <davidva AT tuta DOT io> 2.6.2-8
- Rebuilt for opencv

* Thu May 16 2019 - David Va <davidva AT tuta DOT io> 2.6.2-7
- Updated to 2.6.2-7

* Wed May 01 2019 - David Va <davidva AT tuta DOT io> 2.6.1-7
- Updated to 2.6.1-7

* Thu Apr 18 2019 josef radinger <cheese@nosuchhost.net> - 2.5.7-1
- bump version

* Thu Apr 11 2019 Richard Shaw <hobbes1069@gmail.com> - 2.5.6-2
- Rebuild for OpenEXR/Ilmbase 2.3.0.
- Move licences files to %%license.

* Mon Apr 08 2019 josef radinger <cheese@nosuchhost.net> - 2.5.6-1
- bump version

* Sat Mar 30 2019 josef radinger <cheese@nosuchhost.net> - 2.5.5-1
- bump version

* Sun Mar 24 2019 josef radinger <cheese@nosuchhost.net> - 2.5.4-1
- bump version

* Mon Mar 18 2019 Orion Poplawski <orion@nwra.com> - 2.5.3-2
- Rebuild for hdf5 1.10.5

* Sun Mar 17 2019 josef radinger <cheese@nosuchhost.net> - 2.5.3-1
- bump version
- use gmic_cluts.gmz instead of gmic_film_cluts.gmz

* Sat Mar 16 2019 josef radinger <cheese@nosuchhost.net> - 2.5.2-1
- bump version

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 josef radinger <cheese@nosuchhost.net> - 2.4.5-1
- bump version
- create %%{_sysconfdir}/bash_completion.d and move the file

* Tue Oct 16 2018 Daniel P. Berrangé <berrange@redhat.com> - 2.4.0-1
- Update to 2.4.0 release

* Tue Sep  4 2018 Daniel P. Berrangé <berrange@redhat.com> - 2.3.6-1
- Update to 2.3.6 release
- Drop BuildRoot and Group tags
- Use system CImg
- Update URL tag

* Mon Jul 23 2018 Daniel P. Berrangé <berrange@redhat.com> - 2.3.3-1
- Updated to latest release / snapshots
- Add BR on gcc-c++

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 05 2018 Adam Williamson <awilliam@redhat.com> - 2.2.0-2
- Rebuild for opencv soname bump

* Thu Feb 22 2018 Daniel P. Berrange <berrange@redhat.com> - 2.2.0-1
- Update to new 2.2.0 upstream release
- Some parts now licensed under choice of CeCILL or CeCILL-C

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Daniel P. Berrange <berrange@redhat.com> - 2.1.8-1
- Update to new 2.1.8 upstream release
- Remove bogus -static sub-RPM which contained shared libs

* Thu Jan 04 2018 josef radinger <cheese@nosuchhost.net> - 1.7.2-6
- Rebuilt for libopencv

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar  2 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuild due to opencv soname change

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jun 4 2016 josef radinger <cheese@nosuchhost.net> - 1.7.2-1
- bump version

* Sun May 8 2016 josef radinger <cheese@nosuchhost.net> - 1.7.1-2
- rebuild for rawhide

* Fri Apr 29 2016 josef radinger <cheese@nosuchhost.net> - 1.7.1-1
- bump version
- update Patch1
- fix link on libgmic
- remove smp_mflags (because of compile-errors)
- split a *-static package

* Fri Feb 5 2016 josef radinger <cheese@nosuchhost.net> - 1.6.9-1
- bump version
- update Patch1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 7 2015 josef radinger <cheese@nosuchhost.net> - 1.6.8-1
- bump version

* Sat Oct 24 2015 josef radinger <cheese@nosuchhost.net> - 1.6.7-1
- bump version
- new downloadurl

* Tue Oct 13 2015 josef radinger <cheese@nosuchhost.net> - 1.6.6.1-1
- bump version

* Tue Jun 23 2015 Daniel P. Berrange <berrange@redhat.com> - 1.6.5.0-1
- Update to 1.6.5.0 release
- Enable zart binary build

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Daniel P. Berrange <berrange@redhat.com> - 1.6.2.0-1
- Update to 1.6.2.0 release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.6.1.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Mar 20 2015 Daniel P. Berrange <berrange@redhat.com> - 1.6.1.0-1
- Update to 1.6.1.0 release

* Fri Feb  6 2015 Daniel P. Berrange <berrange@redhat.com> - 1.6.0.4-1
- Update to 1.6.0.4 release

* Fri Dec 19 2014 Daniel P. Berrange <berrange@redhat.com> - 1.6.0.3-1
- Update to 1.6.0.3 release

* Wed Nov 26 2014 Rex Dieter <rdieter@fedoraproject.org> 1.6.0.1-2
- rebuild (openexr), s|qt-devel|qt4-devel|, tighten subpkg deps

* Fri Oct  3 2014 Daniel P. Berrange <berrange@redhat.com> - 1.6.0.1-1
- Update to 1.6.0.1 release

* Mon Aug 25 2014 Daniel P. Berrange <berrange@redhat.com> - 1.6.0.0-1
- Update to 1.6.0.0 release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Daniel P. Berrange <berrange@redhat.com> - 1.5.9.4-1
- Initial Fedora package after review (rhbz #1061801)
