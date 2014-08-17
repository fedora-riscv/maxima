
%if 0%{?rhel} && 0%{?rhel} < 7
%define desktop_vendor --vendor=fedora
%endif

Summary: Symbolic Computation Program
Name: 	 maxima
Version: 5.33.0

Release: 8%{?dist}
License: GPLv2
Group:	 Applications/Engineering 
URL: 	 http://maxima.sourceforge.net/
Source:	 http://downloads.sourceforge.net/sourceforge/maxima/maxima-%{version}%{?beta}.tar.gz
ExclusiveArch: %{arm} %{ix86} x86_64 ppc sparcv9

## upstreamable patches
# https://bugzilla.redhat.com/show_bug.cgi?id=837142
# https://sourceforge.net/tracker/?func=detail&aid=3539587&group_id=4933&atid=104933
Patch50: maxima-5.28.0-clisp-noreadline.patch

# Build the fasl while building the executable to avoid double initialization
Patch51: maxima-5.30.0-build-fasl.patch

## upstream patches

%define maxima_ver %{version}%{?beta}
%define emacs_sitelisp  %{_datadir}/emacs/site-lisp/
%define xemacs_sitelisp %{_datadir}/xemacs/site-packages/lisp/
%define texmf %{_datadir}/texmf

%ifarch %{ix86} x86_64
%define default_lisp sbcl 
%define _enable_sbcl --enable-sbcl
%if 0%{?fedora}
%define _enable_clisp --enable-clisp
%define _enable_gcl --enable-gcl
%define _enable_ecl --enable-ecl
%endif
%endif

%ifarch %{arm}
%define default_lisp sbcl
%define _enable_sbcl --enable-sbcl
#define _enable_gcl --enable-gcl
%define _enable_ecl --enable-ecl
%endif

%ifarch ppc
%define default_lisp sbcl
%define _enable_sbcl --enable-sbcl
%if 0%{?fedora}
# clisp: http://bugzilla.redhat.com/166347 (resolved) - clisp/ppc (still) awol.
#define _enable_clisp --enable-clisp
%define _enable_gcl --enable-gcl
%endif
%endif

%ifarch sparcv9
%define default_lisp sbcl
%define _enable_sbcl --enable-sbcl
%endif

%if "x%{?_enable_cmucl}" == "x%{nil}"
Obsoletes: %{name}-runtime-cmucl < %{version}-%{release}
%endif
%if "x%{?_enable_gcl}" == "x%{nil}"
Obsoletes: %{name}-runtime-gcl < %{version}-%{release}
%endif
%if "x%{?_enable_sbcl}" == "x%{nil}"
Obsoletes: %{name}-runtime-sbcl < %{version}-%{release}
%endif
%if "x%{?_enable_ecl}" == "x%{nil}"
Obsoletes: %{name}-runtime-ecl < %{version}-%{release}
%endif

Source1: maxima.png
Source2: xmaxima.desktop
Source6: maxima-modes.el

## Other maxima reference docs
Source10: http://starship.python.net/crew/mike/TixMaxima/macref.pdf
Source11: http://maxima.sourceforge.net/docs/maximabook/maximabook-19-Sept-2004.pdf

# Inhibit automatic compressing of info files. 
# Compressed info files break maxima's internal help.
%define __spec_install_post %{nil} 
# debuginfo.list ends up empty/blank anyway. disable
%define debug_package   %{nil}

# upstream langpack upgrades, +Provides too? -- Rex
Obsoletes: %{name}-lang-es < %{version}-%{release}
Obsoletes: %{name}-lang-es-utf8 < %{version}-%{release}
Obsoletes: %{name}-lang-pt < %{version}-%{release}
Obsoletes: %{name}-lang-pt-utf8 < %{version}-%{release}
Obsoletes: %{name}-lang-pt_BR < %{version}-%{release}
Obsoletes: %{name}-lang-pt_BR-utf8 < %{version}-%{release}

BuildRequires: desktop-file-utils
BuildRequires: time
%if 0%{?texinfo}
# texi2dvi
BuildRequires: texinfo-tex
BuildRequires: tex(latex)
%if 0%{?fedora} > 17
BuildRequires: tex(fullpage.sty)
%endif
%endif
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info
# /usr/bin/wish
BuildRequires: tk

Requires: %{name}-runtime%{?default_lisp:-%{default_lisp}} = %{version}-%{release}
Requires: gnuplot
Requires: rlwrap

%description
Maxima is a full symbolic computation program.  It is full featured
doing symbolic manipulation of polynomials, matrices, rational
functions, integration, Todd-coxeter, graphing, bigfloats.  It has a
symbolic debugger source level debugger for maxima code.  Maxima is
based on the original Macsyma developed at MIT in the 1970's.

%package gui
Summary: Tcl/Tk GUI interface for %{name}
Group:	 Applications/Engineering 
Requires: %{name} = %{version}-%{release} 
Obsoletes: %{name}-xmaxima < %{version}-%{release}
Requires: tk
Requires: xdg-utils
%description gui
Tcl/Tk GUI interface for %{name}

%package src 
Summary: %{name} lisp source code 
Group:   Applications/Engineering
Requires: %{name} = %{version}-%{release}
%description src 
%{name} lisp source code.

%if "x%{?_enable_clisp:1}" == "x1"
# to workaround mysterious(?) "cpio: MD5 sum mismatch" errors when installing this subpkg
%define __prelink_undo_cmd %{nil}
#define _with_clisp_runtime --with-clisp-runtime=%{_libdir}/clisp/base/lisp.run
%package runtime-clisp
Summary: Maxima compiled with clisp
Group:	 Applications/Engineering
BuildRequires: clisp-devel
Requires: clisp
Requires: %{name} = %{version}-%{release}
Obsoletes: maxima-exec-clisp < %{version}-%{release}
Provides: %{name}-runtime = %{version}-%{release}
%description runtime-clisp
Maxima compiled with Common Lisp (clisp) 
%endif

%if "x%{?_enable_cmucl:1}" == "x1"
%define _with_cmucl_runtime --with-cmucl-runtime=%{_prefix}/lib/cmucl/bin/lisp
%package runtime-cmucl
Summary: Maxima compiled with CMUCL
Group:	 Applications/Engineering 
BuildRequires: cmucl 
# needed dep somewhere around cmucl-20a -- Rex
Requires: cmucl
Requires:  %{name} = %{version}-%{release}
Obsoletes: maxima-exec-cmucl < %{version}-%{release}
Provides:  %{name}-runtime = %{version}-%{release}
%description runtime-cmucl
Maxima compiled with CMU Common Lisp (cmucl) 
%endif

%if "x%{?_enable_gcl:1}" == "x1"
%package runtime-gcl
Summary: Maxima compiled with GCL
Group:   Applications/Engineering
BuildRequires: gcl
Requires:  %{name} = %{version}-%{release}
Obsoletes: maxima-exec-gcl < %{version}-%{release}
Provides:  %{name}-runtime = %{version}-%{release}
%description runtime-gcl
Maxima compiled with Gnu Common Lisp (gcl)
%endif

%if "x%{?_enable_sbcl:1}" == "x1"
%package runtime-sbcl
Summary: Maxima compiled with SBCL 
Group:   Applications/Engineering
BuildRequires: sbcl
# requires the same sbcl it was built against
%global sbcl_vr %(sbcl --version 2>/dev/null | cut -d' ' -f2)
%if "x%{?sbcl_vr}" != "x%{nil}" 
Requires: sbcl = %{sbcl_vr}
%else
Requires: sbcl
%endif
Requires: %{name} = %{version}-%{release}
Obsoletes: maxima-exec-sbcl < %{version}-%{release}
Provides: %{name}-runtime = %{version}-%{release}
%description runtime-sbcl
Maxima compiled with Steel Bank Common Lisp (sbcl).
%endif

%if "x%{?_enable_ecl:1}" == "x1"
%package runtime-ecl
Summary: Maxima compiled with ECL 
Group:   Applications/Engineering
BuildRequires: ecl
# workaround missing requires in ecl pkg(?)
BuildRequires: libffi-devel
%global ecllib %(ecl -eval "(princ (SI:GET-LIBRARY-PATHNAME))" -eval "(quit)")
Requires: ecl
Requires: %{name} = %{version}-%{release}
Obsoletes: maxima-exec-ecl < %{version}-%{release}
Provides: %{name}-runtime = %{version}-%{release}
%description runtime-ecl
Maxima compiled with Embeddable Common-Lisp (ecl).
%endif

%prep
%setup -q  -n %{name}%{!?cvs:-%{version}%{?beta}}

%patch50 -p1 -b .clisp-noreadline
%patch51 -p1 -b .build-fasl

# Extra docs
install -p -m644 %{SOURCE10} .
install -D -p -m644 %{SOURCE11} doc/maximabook/maxima.pdf

sed -i -e 's|@ARCH@|%{_target_cpu}|' src/maxima.in

sed -i -e 's:/usr/local/info:/usr/share/info:' \
  interfaces/emacs/emaxima/maxima.el
sed -i -e \
  's/(defcustom\s+maxima-info-index-file\s+)(\S+)/$1\"maxima.info-16\"/' \
  interfaces/emacs/emaxima/maxima.el

# remove CVS crud
find -name CVS -type d | xargs --no-run-if-empty rm -rv


%build
%configure \
  %{?default_lisp:--with-default-lisp=%{default_lisp} } \
  %{?_enable_clisp} %{!?_enable_clisp: --disable-clisp } %{?_with_clisp_runtime} \
  %{?_enable_cmucl} %{!?_enable_cmucl: --disable-cmucl } %{?_with_cmucl_runtime} \
  %{?_enable_gcl}   %{!?_enable_gcl:   --disable-gcl } \
  %{?_enable_sbcl}  %{!?_enable_sbcl:  --disable-sbcl } \
  %{?_enable_ecl}   %{!?_enable_ecl:   --disable-ecl } \
  --enable-lang-es --enable-lang-es-utf8 \
  --enable-lang-pt --enable-lang-pt-utf8 \
  --enable-lang-pt_BR --enable-lang-pt_BR-utf8 

# help avoid (re)running makeinfo/tex
touch doc/info/maxima.info

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if "x%{?_enable_ecl:1}" == "x1"
install -D -m755 src/binary-ecl/maxima.fas $RPM_BUILD_ROOT%{ecllib}/maxima.fas
%endif

# app icon
install -p -D -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/maxima.png

desktop-file-install \
  --dir="$RPM_BUILD_ROOT%{_datadir}/applications" \
  %{?desktop_vendor} \
  %{SOURCE2} 

# (x)emacs
install -D -m644 -p %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/maxima/%{maxima_ver}/emacs/site_start.d/maxima-modes.el

for dir in %{emacs_sitelisp} %{xemacs_sitelisp} ; do
  install -d -m755 $RPM_BUILD_ROOT$dir/{,site-start.d}
  ln -s %{_datadir}/maxima/%{maxima_ver}/emacs $RPM_BUILD_ROOT$dir/maxima
  for file in $RPM_BUILD_ROOT%{_datadir}/maxima/%{maxima_ver}/emacs/*.el ; do
    touch `dirname $file`/`basename $file .el`.elc
  done
  ln -s %{_datadir}/maxima/%{maxima_ver}/emacs/site_start.d/maxima-modes.el $RPM_BUILD_ROOT$dir/site-start.d/
  touch $RPM_BUILD_ROOT$dir/site-start.d/maxima-modes.elc
done

# emaxima LaTeX style (%ghost)
install -d $RPM_BUILD_ROOT%{texmf}/tex/latex/
ln -sf  %{_datadir}/maxima/%{maxima_ver}/emacs \
        $RPM_BUILD_ROOT%{texmf}/tex/latex/emaxima

## unwanted/unpackaged files
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
# docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/maxima/%{maxima_ver}/doc/{contributors,implementation,misc,maximabook,EMaximaIntro.ps}

# _enable_gcl: debuginfo (sometimes?) fails to get auto-created, so we'll help out
touch debugfiles.list


%check
%ifnarch %{arm}
make -k check
%endif


%post
/sbin/install-info %{_infodir}/maxima.info %{_infodir}/dir ||:
[ -x /usr/bin/texhash ] && /usr/bin/texhash 2> /dev/null ||:

%postun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/maxima.info %{_infodir}/dir ||:
  [ -x /usr/bin/texhash ] && /usr/bin/texhash 2> /dev/null ||:
fi

%post gui
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun gui
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans gui
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%triggerin -- emacs-common
if [ -d %{emacs_sitelisp} ]; then
  rm -rf %{emacs_sitelisp}/maxima   
  ln -sf %{_datadir}/maxima/%{maxima_ver}/emacs  %{emacs_sitelisp}/maxima ||:
fi
ln -sf %{_datadir}/maxima/%{maxima_ver}/emacs/site_start.d/maxima-modes.el %{emacs_sitelisp}/site-start.d/ ||:

%triggerin -- xemacs-common
if [ -d %{xemacs_sitelisp} ]; then
  rm -rf %{xemacs_sitelisp}/maxima
  ln -sf %{_datadir}/maxima/%{maxima_ver}/emacs  %{xemacs_sitelisp}/maxima ||:
fi
ln -sf %{_datadir}/maxima/%{maxima_ver}/emacs/site_start.d/maxima-modes.el %{xemacs_sitelisp}/site-start.d/ ||:

%triggerun -- emacs-common
if [ $2 -eq 0 ]; then
 rm -f %{emacs_sitelisp}/maxima || :
 rm -f %{emacs_sitelisp}/site-start.d/maxima-modes.el* ||:
fi

%triggerun -- xemacs-common
if [ $2 -eq 0 ]; then
 rm -f %{xemacs_sitelisp}/maxima || :
 rm -f %{xemacs_sitelisp}/site-start.d/maxima-modes.el* ||:
fi

%triggerin -- tetex-latex,texlive-latex
if [ -d %{texmf}/tex/latex ]; then
  rm -rf %{texmf}/tex/latex/emaxima ||:
  ln -sf %{_datadir}/maxima/%{maxima_ver}/emacs %{texmf}/tex/latex/emaxima ||:
  %{_bindir}/texhash 2> /dev/null ||:
fi

%triggerun -- tetex-latex,texlive-latex
if [ $2 -eq 0 ]; then
  rm -f %{texmf}/tex/latex/emaxima ||:
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README README.lisps
%doc doc/misc/ doc/implementation/
%doc doc/maximabook/maxima.pdf
%{_bindir}/maxima
%{_bindir}/rmaxima
%dir %{_datadir}/maxima
%dir %{_datadir}/maxima/%{maxima_ver}
%{_datadir}/maxima/%{maxima_ver}/[a-c,f-r,t-w,y-z,A-Z]*
%{_datadir}/maxima/%{maxima_ver}/demo/
%dir %{_datadir}/maxima/%{maxima_ver}/doc/
%dir %{_datadir}/maxima/%{maxima_ver}/doc/html/
%{_datadir}/maxima/%{maxima_ver}/doc/html/figures/
%doc %lang(en) %{_datadir}/maxima/%{maxima_ver}/doc/html/*.h*
%doc %lang(en) %{_datadir}/maxima/%{maxima_ver}/doc/share/
%doc %lang(es) %{_datadir}/maxima/%{maxima_ver}/doc/html/es/
%doc %lang(es) %{_datadir}/maxima/%{maxima_ver}/doc/html/es.utf8/
%doc %lang(pt) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt/
%doc %lang(pt) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt.utf8/
%doc %lang(pt_BR) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt_BR/
%doc %lang(pt_BR) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt_BR.utf8/
%{_datadir}/maxima/%{maxima_ver}/share/
%dir %{_libdir}/maxima/
%dir %{_libdir}/maxima/%{maxima_ver}/
%{_libexecdir}/maxima
%{_infodir}/*maxima*
%lang(es) %{_infodir}/es*
%lang(pt) %{_infodir}/pt/
%lang(pt) %{_infodir}/pt.utf8/
%lang(pt_BR) %{_infodir}/pt_BR*
%{_mandir}/man1/maxima.*
%dir %{_datadir}/maxima/%{maxima_ver}/emacs
%{_datadir}/maxima/%{maxima_ver}/emacs/emaxima.*
%{_datadir}/maxima/%{maxima_ver}/emacs/imaxima.*
%{_datadir}/maxima/%{maxima_ver}/emacs/*.el
%ghost %{_datadir}/maxima/%{maxima_ver}/emacs/*.elc
%dir %{_datadir}/maxima/%{maxima_ver}/emacs/site_start.d/
%{_datadir}/maxima/%{maxima_ver}/emacs/site_start.d/*.el
%ghost %{emacs_sitelisp}
%ghost %{xemacs_sitelisp}
%ghost %{texmf}/tex/latex/emaxima

%files src
%defattr(-,root,root,-)
%{_datadir}/maxima/%{maxima_ver}/src/

%files gui
%defattr(-,root,root,-)
%{_bindir}/xmaxima
%{_datadir}/maxima/%{maxima_ver}/xmaxima/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*

%if "x%{?_enable_clisp:1}" == "x1"
%files runtime-clisp
%defattr(-,root,root,-)
%{_libdir}/maxima/%{maxima_ver}/binary-clisp
%endif

%if "x%{?_enable_cmucl:1}" == "x1"
%files runtime-cmucl
%defattr(-,root,root,-)
%{_libdir}/maxima/%{maxima_ver}/binary-cmucl
%endif

%if "x%{?_enable_gcl:1}" == "x1"
%files runtime-gcl
%defattr(-,root,root,-)
%{_libdir}/maxima/%{maxima_ver}/binary-gcl
%endif

%if "x%{?_enable_sbcl:1}" == "x1"
%files runtime-sbcl
%defattr(-,root,root,-)
%{_libdir}/maxima/%{maxima_ver}/binary-sbcl
%endif

%if "x%{?_enable_ecl:1}" == "x1"
%files runtime-ecl
%defattr(-,root,root,-)
%{_libdir}/maxima/%{version}/binary-ecl
%{ecllib}/maxima*.fas
%endif


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.33.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.33.0-7
- rebuild (sbcl)

* Thu Jun 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.33.0-6
- rebuild (sbcl), arm support/use-by-default sbcl (like other archs)

* Tue Jun 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.33.0-5
- (re)enable gcl support

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.33.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.33.0-3
- (re)enable ecl support

* Wed May 14 2014 Rex Dieter <rdieter@fedoraproject.org> 5.33.0-2
- rebuild (sbcl)
- disable gcl/ecl support (rawhide busted atm)

* Tue Apr 08 2014 Rex Dieter <rdieter@fedoraproject.org> 5.33.0-1
- 5.33.0

* Fri Mar 07 2014 Rex Dieter <rdieter@fedoraproject.org> 5.32.1-3
- rebuild (sbcl)

* Wed Jan 29 2014 Rex Dieter <rdieter@fedoraproject.org> 5.32.1-2
- rebuild (sbcl)

* Fri Jan 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.32.1-1
- 5.32.1

* Thu Dec 26 2013 Rex Dieter <rdieter@fedoraproject.org> 5.32.0-1
- 5.32.0

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> 5.31.3-3
- rebuild (sbcl)

* Fri Nov 01 2013 Rex Dieter <rdieter@fedoraproject.org> 5.31.3-2
- rebuild (sbcl)

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.31.3-1
- 5.31.3

* Sat Oct 05 2013 Rex Dieter <rdieter@fedoraproject.org> 5.31.2-1
- 5.31.2

* Mon Sep 30 2013 Rex Dieter <rdieter@fedoraproject.org> 5.31.1-2
- rebuild (sbcl)

* Fri Sep 27 2013 Rex Dieter <rdieter@fedoraproject.org> 5.31.1-1
- 5.31.1

* Sat Sep 07 2013 Rex Dieter <rdieter@fedoraproject.org> 5.31.0-1
- 5.31.0

* Sat Aug 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.30.0-8
- build for %%arm too (gcl/ecl support)

* Fri Aug 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.30.0-7
- rebuild (sbcl)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.30.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Jerry James <loganjerry@gmail.com> - 5.30.0-5
- rebuild (ecl)

* Tue Jun 04 2013 Rex Dieter <rdieter@fedoraproject.org> 5.30.0-4
- rebuild (sbcl)

* Sun Jun 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.30.0-3
- rebuild (sbcl)

* Mon Apr 29 2013 Rex Dieter <rdieter@fedoraproject.org> 5.30.0-2
- rebuild (sbcl)

* Sat Apr 06 2013 Rex Dieter <rdieter@fedoraproject.org> 5.30.0-1
- 5.3.30

* Wed Feb 27 2013 Rex Dieter <rdieter@fedoraproject.org> 5.29.1-6
- cleaner/simpler workaround to avoid (re)running makeinfo/tex

* Tue Feb 26 2013 Rex Dieter <rdieter@fedoraproject.org> 5.29.1-5
- avoid texinfo on f19+ (#913274)

* Wed Feb 20 2013 Rex Dieter <rdieter@fedoraproject.org> 5.29.1-4
- rebuild (sbcl)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.29.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.29.1-2
- rebuild (sbcl)

* Thu Dec 13 2012 Rex Dieter <rdieter@fedoraproject.org> 5.29.1-1
- maxima-5.29.1

* Sat Dec 08 2012 Rex Dieter <rdieter@fedoraproject.org> 5.29.0-3
- wxmaxima_compat patch

* Sat Dec 08 2012 Rex Dieter <rdieter@fedoraproject.org> 5.29.0-2
- rebuild (sbcl)

* Sat Dec 08 2012 Rex Dieter <rdieter@fedoraproject.org> 5.29.0-1
- maxima-5.29.0

* Fri Nov 02 2012 Rex Dieter <rdieter@fedoraproject.org> 5.28.0-3
- rebuild (sbcl)

* Sat Oct 27 2012 Rex Dieter <rdieter@fedoraproject.org> 5.28.0-2
- rebuild (sbcl)

* Fri Aug 17 2012 Rex Dieter <rdieter@fedoraproject.org> 5.28.0-1
- maxima-5.28.0

* Fri Aug 10 2012 Rex Dieter <rdieter@fedoraproject.org> 5.27.0-11
- rebuild (ecl)

* Tue Aug 07 2012 Rex Dieter <rdieter@fedoraproject.org> 5.27.0-10
- rebuild (sbcl)

* Mon Jul 23 2012 Rex Dieter <rdieter@fedoraproject.org> 5.27.0-9
- rebuild (sbcl)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.27.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 08 2012 Rex Dieter <rdieter@fedoraproject.org> 5.27.0-7
- RFE: Add patch to allow disabling readline in maxima-runtime-clisp (#837142)

* Mon Jul 02 2012 Rex Dieter <rdieter@fedoraproject.org> 5.27.0-6
- BR: libffi-devel (workaround ecl bug #837102)

* Mon Jul 02 2012 Rex Dieter <rdieter@fedoraproject.org> 5.27.0-5.1
- enable (only) ecl to highlight ftbfs

* Sun Jul 01 2012 Rex Dieter <rdieter@fedoraproject.org> 5.27.0-5
- disable cmucl (orphaned) support

* Sun Jul 1 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 5.27.0-4
- Enable ecl support.
- Build ecl interface to maxima required by sagemath.

* Tue May 29 2012 Rex Dieter <rdieter@fedoraproject.org> 5.27.0-3
- rebuild (sbcl)

* Thu Apr 12 2012 Rex Dieter <rdieter@fedoraproject.org> 5.27.0-2
- rebuild (sbcl)

* Thu Apr 05 2012 Rex Dieter <rdieter@fedoraproject.org> 5.27.0-1
- 5.27.0

* Wed Jan 18 2012 Rex Dieter <rdieter@fedoraproject.org> 5.26.0-1
- 5.26.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.25.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 07 2011 Rex Dieter <rdieter@fedoraproject.org> 5.25.1-3
- rebuild (sbcl)

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 5.25.1-2.1
- rebuild with new gmp without compat lib

* Sat Oct 15 2011 Rex Dieter <rdieter@fedoraproject.org> 5.25.1-2
- rebuild (sbcl)

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 5.25.1-1.1
- rebuild with new gmp

* Tue Sep 06 2011 Rex Dieter <rdieter@fedoraproject.org> 5.25.1-1
- maxima-5.25.1

* Mon Aug 22 2011 Rex Dieter <rdieter@fedoraproject.org> 5.25.0-3
- fix sbcl_vr macro usage 

* Sun Aug 21 2011 Rex Dieter <rdieter@fedoraproject.org> 5.25.0-1
- maxima-5.25.0

* Fri Jul 15 2011 Rex Dieter <rdieter@fedoraproject.org> 5.24.0-1
- maxima-5.24.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.23.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Rex Dieter <rdieter@fedoraproject.org> - 5.23.2-1
- maxima-5.23.2

* Fri Dec 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.23.0-1
- maxima-5.23.0

* Mon Nov 29 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.22.1-6
- rebuild (clisp, libsigsegv)

* Mon Oct 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.22.1-5
- maxima-runtime-cmucl: missing cmucl dependency (#646186)
- tighten -runtime-related deps
- add dep on default runtime
- enable gcl runtime (#496124)

* Thu Sep 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.22.1-4
- rebuild (sbcl)

* Wed Sep 29 2010 jkeating - 5.22.1-3
- Rebuilt for gcc bug 634757

* Sat Sep 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.22.1-2 
- rebuild (sbcl)

* Mon Aug 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.22.1-1
- maxima-5.22.1

* Sat Jul 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.21.1-3
- rebuild (sbcl)

* Fri May 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.21.1-2
- rebuild (sbcl)

* Sun Apr 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.21.1-1
- maxima-5.21.1

* Mon Apr 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.21.0-1
- maxima-5.21.0

* Fri Apr 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.20.1-4
- rebuild (sbcl)

* Tue Feb 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.20.1-3
- rebuild (sbcl)

* Wed Dec 16 2009 Stephen Beahm <stephenbeahm@comcast.net> - 5.20.1-2
- enable rmaxima (#551910)

* Tue Dec 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 5.20.1-1
- maxima-5.20.1 (#547012)

* Thu Dec 10 2009 Rex Dieter <rdieter@fedoraproject.org> - 5.20.0-1
- maxima-5.20.0
