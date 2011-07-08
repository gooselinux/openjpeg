# reset patch fuzz, rebasing patches will require delicate surgery -- Rex
%global _default_patch_fuzz 2

Name:    openjpeg
Version: 1.3
Release: 7%{?dist}
Summary: OpenJPEG command line tools

Group:     Applications/Multimedia
License:   BSD
URL:       http://www.openjpeg.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake
BuildRequires: libtiff-devel

Requires: %{name}-libs = %{version}-%{release}

Source0: http://www.openjpeg.org/openjpeg_v1_3.tar.gz

Patch1: openjpeg-20070717svn-codec-libtiff.patch
Patch4: openjpeg-svn480-cmake.patch
Patch5: openjpeg-svn480-use-stdbool.patch
Patch6: openjpeg-1.3-tcd_init_encode-alloc-fix.patch
Patch7: openjpeg-1.3-reverse-bogus-aligned-malloc.patch
Patch44: openjpeg-svn468-mj2-noscroll.patch
Patch21: openjpeg-20070717svn-mqc-optimize.patch
Patch22: openjpeg-20070821svn-t1-remove-macro.patch
Patch23: openjpeg-20070719svn-t1-x86_64-flags-branchless.patch
Patch24: openjpeg-20070719svn-t1-t1_dec_sigpass_step-optimize.patch
Patch25: openjpeg-20070821svn-t1-flags-stride.patch
Patch26: openjpeg-20070821svn-t1-updateflags-x86_64.patch
Patch27: openjpeg-svn470-t1-flags-mmx.patch
Patch28: openjpeg-20070719svn-mqc-more-optimize.patch
Patch29: openjpeg-svn501-image-create0.patch
Patch30: openjpeg-svn505-error-check.patch

## upstreamable patches
# libopenjpeg has undefined references, http://bugzilla.redhat.com/467661
Patch50: openjpeg-1.3-libm.patch

%description
OpenJPEG is an open-source JPEG 2000 codec written in C language. It has been
developed in order to promote the use of JPEG 2000, the new still-image
compression standard from the Joint Photographic Experts Group (JPEG).

%package libs
Summary: JPEG 2000 codec library
Group:   System Environment/Libraries

%description libs
The openjpeg-libs package contains runtime libraries for applications that use
OpenJPEG.

%package  devel
Summary:  Development files for openjpeg
Group:    Development/Libraries
Requires: openjpeg-libs = %{version}-%{release}

%description devel
The openjpeg-devel package contains libraries and header files for
developing applications that use OpenJPEG.

%prep
%setup -q -n OpenJPEG_v1_3

# Windows stuff, delete it, it slows down patch making
rm -rf jp3d
# Make sure we use system libraries
rm -rf libs

%patch1 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch44 -p1
%patch22 -p1
%patch23 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch24 -p1
%patch21 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch50 -p1 -b .libm

%build
mkdir build
pushd build
%cmake .. -DBUILD_EXAMPLES:BOOL=ON
make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}
pushd build
make install DESTDIR="%{buildroot}"
popd

# HACK: until pkg-config support lands, temporarily provide
# openjpeg.h header in legacy location
ln -s openjpeg/openjpeg.h %{buildroot}%{_includedir}/openjpeg.h


%check
# mostly pointless without test images, but it's a start -- Rex
make test -C build

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog license.txt
%{_bindir}/extract_j2k_from_mj2
%{_bindir}/frames_to_mj2
%{_bindir}/image_to_j2k
%{_bindir}/j2k_to_image
%{_bindir}/mj2_to_frames
%{_bindir}/wrap_j2k_in_mj2

%files libs
%defattr(-,root,root,-)
%{_libdir}/libopenjpeg.so.2*

%files devel
%defattr(-,root,root,-)
%{_includedir}/openjpeg.h
%{_includedir}/openjpeg/
%{_libdir}/libopenjpeg.so

%changelog
* Wed Jul  7 2010 Tom Lane <tgl@redhat.com> 1.3-7
- Apply two upstream fixes for crasher bugs
Resolves: #609389
- Fix FTBFS: ImplicitDSOLinking (see Fedora bug 564783)

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.3-6.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.3-5
- libopenjpeg has undefined references (#467661)
- openjpeg.h is installed in a directory different from upstream's default (#484887)
- drop -O3 (#504663)
- add %%check section
- %%files: track libopenjpeg somajor (2)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 07 2008 Rex Dieter <rdieter@fedoraproject.org> 1.3-3
- FTBFS (#464949)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-2
- Autorebuild for GCC 4.3

* Thu Dec 27 2007 Callum Lerwick <seg@haxxed.com> 1.3-1
- New upstream release.

* Tue Dec 11 2007 Callum Lerwick <seg@haxxed.com> 1.2-4.20071211svn484
- New snapshot. Fixes bz420811.

* Wed Nov 14 2007 Callum Lerwick <seg@haxxed.com> 1.2-3.20071114svn480
- Build using cmake.
- New snapshot.

* Thu Aug 09 2007 Callum Lerwick <seg@haxxed.com> 1.2-2.20070808svn
- Put binaries in main package, move libraries to -libs subpackage.

* Sun Jun 10 2007 Callum Lerwick <seg@haxxed.com> 1.2-1
- Build the mj2 tools as well.
- New upstream version, ABI has broken, upstream has bumped soname.

* Fri Mar 30 2007 Callum Lerwick <seg@haxxed.com> 1.1.1-3
- Build and package the command line tools.

* Fri Mar 16 2007 Callum Lerwick <seg@haxxed.com> 1.1.1-2
- Link with libm, fixes building on ppc. i386 and x86_64 are magical.

* Fri Feb 23 2007 Callum Lerwick <seg@haxxed.com> 1.1.1-1
- New upstream version, which has the SL patches merged.

* Sat Feb 17 2007 Callum Lerwick <seg@haxxed.com> 1.1-2
- Move header to a subdirectory.
- Fix makefile patch to preserve timestamps during install.

* Sun Feb 04 2007 Callum Lerwick <seg@haxxed.com> 1.1-1
- Initial packaging.
