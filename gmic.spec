%global gimpplugindir %{_libdir}/gimp/2.0/plug-ins
%global soname %(c=%{version}; echo ${c//./})
%global basoname %(c=%{soname}; echo ${c:0:1})

%global debug_package %{nil}


# We have problems compiling zart in gmic 2.7.5
# https://github.com/c-koi/zart/issues/13
%bcond_with zart

# Conditional system cimg
%bcond_with system_cimg

# Only for test usage
%global gmic_commit 71e0f9cfd4c63e545b9a7a3f0515c33f93e2deae
%global shortcommit0 %(c=%{gmic_commit}; echo ${c:0:7})

%global zart_commit 099554f8bf26c6161cd8c0b7df3d1aedad27e8ec 
%global shortcommit1 %(c=%{zart_commit}; echo ${c:0:7})

%global gmic_qt_commit 168e4cc8d429c3ba4069f242090ac36ec94dfc33
%global shortcommit2 %(c=%{gmic_qt_commit}; echo ${c:0:7})

%global gmic_community_commit d77951f85ed6286a490a16fa4695426a3ed11f8e
%global shortcommit3 %(c=%{gmic_community_commit}; echo ${c:0:7})


Summary: GREYC's Magic for Image Computing
Name: gmic
Version: 2.8.3
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
Source4: https://raw.githubusercontent.com/dtschump/CImg/12f1fac5dc1221eca3c0ecdca7bd77da7392ddbb/CImg.h
Patch0: zart-opencv4.patch
Patch1: cmake_fix.patch
License: (CeCILL or CeCILL-C) and GPLv3+
Url: http://gmic.eu/
%if %{with system_cimg}
BuildRequires: CImg-devel 
%endif
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libtiff-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: fftw-devel
BuildRequires: OpenEXR-devel
BuildRequires: zlib-devel
BuildRequires: gimp-devel-tools
BuildRequires: hdf5-devel
BuildRequires: opencv-devel >= 4.2.0
BuildRequires: opencv-xfeatures2d-devel >= 4.2.0
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
%patch0 -p1
%patch1 -p1

# fixes
dos2unix src/Makefile


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

%build

pushd src

ln -fs ../gmic-community/libcgmic/gmic_libc.cpp .
ln -fs ../gmic-community/libcgmic/gmic_libc.h .
ln -fs ../gmic-community/libcgmic/use_libcgmic.c .
popd

# Build gmic
# We are using cmake, reduce build time and resources
mkdir -p build
pushd build
cmake \
		-DCMAKE_INSTALL_PREFIX=/usr \
		-DCMAKE_INSTALL_LIBDIR=%{_libdir} \
		-DCMAKE_VERBOSE_MAKEFILE:BOOL=OFF \
		-DENABLE_CCACHE=OFF \
		-DCMAKE_BUILD_TYPE=Release \
		-DBUILD_LIB=ON \
		-DBUILD_LIB_STATIC=OFF \
		-DBUILD_CLI=ON \
		-DBUILD_MAN=ON \
		-DBUILD_BASH_COMPLETION=ON \
		-DCUSTOM_CFLAGS=ON \
		-DENABLE_CURL=ON \
		-DENABLE_X=ON \
		-DENABLE_FFMPEG=OFF \
		-DENABLE_FFTW=ON \
		-DENABLE_GRAPHICSMAGICK=ON \
		-DENABLE_JPEG=ON \
		-DENABLE_OPENCV=ON \
		-DENABLE_OPENEXR=ON \
		-DENABLE_OPENMP=OFF \
		-DENABLE_PNG=ON \
		-DENABLE_TIFF=ON \
		-DENABLE_ZLIB=ON \
		-DENABLE_DYNAMIC_LINKING=ON ..

%make_build VERBOSE=0 NOSTRIP=1 -j1
popd
echo 'DONE MAKE'

# Create link for zart dynamic linking
ln -s ../build/libgmic.so src/libgmic.so 

mv -f %{S:4} src/CImg.h
	
%if %{with system_cimg}
# We want to build against the system installed CImg package.
# G'MIC provides no way todo this, so we just copy the file
# over what's there already
mv src/CImg.h src/CImg.h.bak
cp /usr/include/CImg.h src/CImg.h
%endif

  pushd gmic-qt
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on HOST=none
  %make_build VERBOSE=0
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on HOST=gimp
  %make_build VERBOSE=0
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on HOST=krita
  %make_build VERBOSE=0
  popd

%if !%{with zart}
  pushd zart
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src zart.pro 
  %make_build VERBOSE=0
  popd
%endif

# build libc
pushd src  
%make_build libc NOSTRIP=1
popd

%install

pushd build
%make_install
popd


pushd src
VERSION0=$(grep 'gmic_version\ ' gmic.h | tail -c4 | head -c3)
VERSION1=$(grep 'gmic_version\ ' gmic.h | tail -c4 | head -c1)
VERSION2=$(grep 'gmic_version\ ' gmic.h | tail -c3 | head -c1)
VERSION3=$(grep 'gmic_version\ ' gmic.h | tail -c2 | head -c1)

# Soname of cmake? why so.1?
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

# symlinks for compatibility for the library
ln -sf libgmic.so.${VERSION1} $RPM_BUILD_ROOT/%{_libdir}/libgmic.so
ln -sf libgmic.so.${VERSION1} $RPM_BUILD_ROOT/%{_libdir}/libgmic.so.${VERSION0}
ln -sf libgmic.so.${VERSION1} $RPM_BUILD_ROOT/%{_libdir}/libgmic.so.1
ln -sf libgmic.so.${VERSION1} $RPM_BUILD_ROOT/%{_libdir}/libgmic.so.%{version}

ln -sf libcgmic.so.${VERSION1} $RPM_BUILD_ROOT/%{_libdir}/libcgmic.so
ln -sf libcgmic.so.${VERSION1} $RPM_BUILD_ROOT/%{_libdir}/libcgmic.so.${VERSION0}
ln -sf libcgmic.so.${VERSION1} $RPM_BUILD_ROOT/%{_libdir}/libcgmic.so.1
ln -sf libcgmic.so.${VERSION1} $RPM_BUILD_ROOT/%{_libdir}/libcgmic.so.%{version}


pushd build/resources/
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d/
cp -f gmic_bashcompletion.sh  %{buildroot}/%{_sysconfdir}/bash_completion.d/gmic
popd
 
# Sourced files shouldn't be executable
chmod -x %{buildroot}/%{_sysconfdir}/bash_completion.d/gmic
 

# COPYING fix
mv $PWD/gmic-community/libcgmic/COPYING COPYING-libcgmic 
mv $PWD/gmic-qt/COPYING COPYING-gmic-qt 

# cmake fix, using the correct soname for the release
sed -i "s|libgmic.so.1|libgmic.so.${VERSION1}|g" $RPM_BUILD_ROOT/%{_libdir}/cmake/gmic/GmicTargets-release.cmake

%ldconfig_scriptlets

%files
%doc README
%license COPYING COPYING-gmic-qt COPYING-libcgmic
%{_bindir}/gmic
%{_bindir}/gmic_qt
%if !%{with zart}
%{_bindir}/zart
%endif
%{_sysconfdir}/bash_completion.d/gmic
%{_libdir}/libgmic.so.*
%{_libdir}/libcgmic.so.*
%{_libdir}/cmake/gmic/*.cmake
%{_mandir}/man1/%{name}.1.gz

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
