%global gimpplugindir %{_libdir}/gimp/2.0/plug-ins

%global use_system_cimg 0

%global zart_commit 51f9d2d3ab749c48ecfe0f0fcfe2a41d97b3a6f0
%global shortcommit1 %(c=%{zart_commit}; echo ${c:0:7})

%global gmic_qt_commit df21660c26dafa6254f5cdab75fc735d994104ce
%global shortcommit2 %(c=%{gmic_qt_commit}; echo ${c:0:7})

%global gmic_community_commit cee13cf2f76baa0bc2ca9f90ff21375b311c7792
%global shortcommit3 %(c=%{gmic_community_commit}; echo ${c:0:7})


Summary: GREYC's Magic for Image Computing
Name: gmic
Version: 2.6.2
Release: 7%{?dist}
Source0: https://gmic.eu/files/source/%{name}_%{version}.tar.gz 
# GIT archive snapshot of https://github.com/c-koi/zart
Source1: https://github.com/c-koi/zart/archive/%{zart_commit}.tar.gz#/zart-%{shortcommit1}.tar.gz
# GIT archive snapshot of https://github.com/c-koi/gmic-qt
Source2: https://github.com/c-koi/gmic-qt/archive/%{gmic_qt_commit}.tar.gz#/gmic-qt-%{shortcommit2}.tar.gz
# GIT archive snapshot of https://github.com/dtschump/gmic-community
Source3: https://github.com/dtschump/gmic-community/archive/%{gmic_community_commit}.tar.gz#/gmic-community-%{shortcommit3}.tar.gz
Patch0: opencv_4.patch
License: (CeCILL or CeCILL-C) and GPLv3+
Url: http://gmic.eu/
%if %{use_system_cimg}
BuildRequires: CImg-devel == 1:%{version}
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
BuildRequires: opencv-devel
BuildRequires: opencv-xfeatures2d-devel
BuildRequires: GraphicsMagick-c++-devel
BuildRequires: ilmbase-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: libcurl-devel
BuildRequires: gcc-c++
BuildRequires: gimp-devel-tools
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
%setup -n %{name}-%{version} 

%if 0%{?fedora} >= 32
# opencv 4
%patch0 -p1 
%endif

# fix overlinking
%if 0%{?fedora} >= 32
sed -e 's/pkg-config opencv --libs ||//' -e 's/-lopencv_highgui/-lopencv_videoio/' \
      -e 's/pkg-config opencv/pkg-config opencv4/' -i src/Makefile   
%endif

%build
  make -C src cli lib libc WGET=/bin/true LIBS=${LDFLAGS}

  pushd gmic-qt
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on HOST=none
  make
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on HOST=gimp
  make
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on HOST=krita
  make  
  popd

  pushd zart
  %{qmake_qt5} CONFIG+=release GMIC_PATH=../src GMIC_DYNAMIC_LINKING=on QMAKE_CXXFLAGS+=" -DOPENCV2_HEADERS"
  make
  popd


%if %{use_system_cimg}
# We want to build against the system installed CImg package.
# G'MIC provides no way todo this, so we just copy the file
# over what's there already
mv CImg.h CImg.h.bak
cp /usr/include/CImg.h CImg.h
%endif


%install

pushd src
make DESTDIR=%{buildroot} install
rm -r %{buildroot}/usr/{bin/zart,lib64/gimp,bin/gmic_krita_qt}

install -Dm755 ../zart/zart -t %{buildroot}/usr/bin

install -dm 755 %{buildroot}/%{gimpplugindir}/
install -Dm644 ../gmic-qt/gmic_gimp_qt %{buildroot}/%{gimpplugindir}/
install -Dm644 ../resources/gmic_cluts.gmz %{buildroot}/%{gimpplugindir}/

install -Dm644 ../gmic-qt/gmic_krita_qt -t %{buildroot}/usr/bin/

# Makefile is not multilib aware
%ifarch x86_64
mv %{buildroot}/%{_prefix}/lib/* %{buildroot}/%{_libdir}/
%endif

mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d/
cp -f %{buildroot}/%{_datadir}/bash-completion/completions/gmic %{buildroot}/%{_sysconfdir}/bash_completion.d/
rm -rf %{buildroot}/%{_datadir}/bash-completion/completions
 
# Sourced files shouldn't be executable
chmod -x %{buildroot}/%{_sysconfdir}/bash_completion.d/gmic

%ldconfig_scriptlets

%files
%doc README
%license COPYING 
%{_bindir}/gmic
%{_bindir}/gmic_qt
%{_bindir}/zart
%{_sysconfdir}/bash_completion.d/gmic
%{_libdir}/libgmic.so.*
%{_libdir}/libcgmic.so.*
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/fr/man1/%{name}.1.gz

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
