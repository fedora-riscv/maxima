
Summary: Symbolic Computation Program
Name: 	 maxima
Version: 5.15.0

Release: 1%{?dist} 
License: GPLv2
Group:	 Applications/Engineering 
URL: 	 http://maxima.sourceforge.net/
Source:	 http://downloads.sourceforge.net/sourceforge/maxima/maxima-%{version}%{?beta}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

ExclusiveArch: %{ix86} x86_64 sparc

%define maxima_ver %{version}%{?beta}
%define emacs_sitelisp  %{_datadir}/emacs/site-lisp/
%define xemacs_sitelisp %{_datadir}/xemacs/site-packages/lisp/
%define texmf %{_datadir}/texmf

%ifarch %{ix86}
%define _enable_cmucl --enable-cmucl
%if 0%{?fedora} > 2 && 0%{?fedora} < 10
%define _enable_gcl --enable-gcl
%endif
%endif

%ifarch %{ix86} x86_64
%define default_lisp sbcl
%if 0%{?fedora} > 2
%define _enable_clisp --enable-clisp 
# gcl busted on x86_64 atm: http://bugzilla.redhat.com/427250
#define _enable_gcl --enable-gcl
%define _enable_sbcl --enable-sbcl
%else
# epel/rhel
%define _enable_sbcl --enable-sbcl 
%endif
%endif

%ifarch ppc
#define default_lisp sbcl
# clisp: http://bugzilla.redhat.com/166347 (resolved) - clisp/ppc (still) awol.
#define _enable_clisp --enable-clisp 
# gcl:   http://bugzilla.redhat.com/167952
#define _enable_gcl --enable-gcl 
# sbcl:  http://bugzilla.redhat.com/220053 (resolved)
# sbcl: ppc/ld joy, "final link failed: Nonrepresentable section on output" http://bugzilla.redhat.com/448734
#define _enable_sbcl --enable-sbcl 
%endif

%ifarch sparc
%define default_lisp sbcl
%define _enable_sbcl --enable-sbcl
%endif

%if "%{?_enable_cmucl}" == "%{nil}"
Obsoletes: %{name}-runtime-cmucl < %{version}-%{release}
%endif
%if "%{?_enable_gcl}" == "%{nil}"
Obsoletes: %{name}-runtime-gcl < %{version}-%{release}
%endif
%if "%{?_enable_sbcl}" == "%{nil}"
Obsoletes: %{name}-runtime-sbcl < %{version}-%{release}
%endif


Source1: maxima.png
Source2: xmaxima.desktop
Source6: maxima-modes.el

## Other maxima reference docs
Source10: http://starship.python.net/crew/mike/TixMaxima/macref.pdf
Source11: http://maxima.sourceforge.net/docs/maximabook/maximabook-19-Sept-2004.pdf

# maxima-runtime-gcl: Unrecoverable error: fault count too high (#187647)
Patch6: maxima-5.9.4-gcl_setarch.patch

# Inhibit automatic compressing of info files. Compressed info
# files break maxima's internal help.
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

BuildRequires: time
# texi2dvi
%if 0%{?fedora} > 5 || 0%{?rhel} > 4
BuildRequires: texinfo-tex
%else
BuildRequires: texinfo
%endif
BuildRequires: tetex-latex
BuildRequires: desktop-file-utils
# /usr/bin/wish
BuildRequires: tk

Requires: %{name}-runtime = %{version}
## Consider this when rpm supports it -- Rex
#if "%{?default_lisp:1}" == "1"
#Requires(hint): %{name}-runtime-%{default_lisp} = %{version}
#endif
Requires: gnuplot
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

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

%if "%{?_enable_clisp:1}" == "1"
# to workaround mysterious(?) "cpio: MD5 sum mismatch" errors when installing this subpkg
%define __prelink_undo_cmd %{nil}
#define _with_clisp_runtime --with-clisp-runtime=%{_libdir}/clisp/base/lisp.run
%package runtime-clisp
Summary: Maxima compiled with clisp
Group:	 Applications/Engineering
BuildRequires: clisp-devel
Requires: clisp
Requires: %{name} = %{version}
Obsoletes: maxima-exec-clisp < %{version}-%{release}
Provides: %{name}-runtime = %{version}
%description runtime-clisp
Maxima compiled with Common Lisp (clisp) 
%endif

%if "%{?_enable_cmucl:1}" == "1"
%define _with_cmucl_runtime=--with-cmucl-runtime=%{_libdir}/cmucl/bin/lisp
%package runtime-cmucl
Summary: Maxima compiled with CMUCL
Group:	 Applications/Engineering 
BuildRequires: cmucl 
Requires:  %{name} = %{version}
Obsoletes: maxima-exec-cmucl < %{version}-%{release}
Provides:  %{name}-runtime = %{version}
%description runtime-cmucl
Maxima compiled with CMU Common Lisp (cmucl) 
%endif

%if "%{?_enable_gcl:1}" == "1"
%package runtime-gcl
Summary: Maxima compiled with GCL
Group:   Applications/Engineering
BuildRequires: gcl
Requires:  %{name} = %{version}
%if 0%{?fedora} > 4 || 0%{?rhel} > 4
# See http://bugzilla.redhat.com/187647
%define setarch_hack 1
BuildRequires: setarch
Requires:  setarch
%endif
Obsoletes: maxima-exec-gcl < %{version}-%{release}
Provides:  %{name}-runtime = %{version}
Provides:  %{name}-runtime-gcl = %{version}-%{release}
%description runtime-gcl
Maxima compiled with Gnu Common Lisp (gcl)
%endif

%if "%{?_enable_sbcl:1}" == "1"
%package runtime-sbcl
Summary: Maxima compiled with SBCL 
Group:   Applications/Engineering
BuildRequires: sbcl
# maxima requires the *same* (or very similar) version it was built against
# this hack should work, even in mock (-: -- Rex
%global sbcl_ver %(sbcl --version 2>/dev/null | cut -d' ' -f2)
%if "%{?sbcl_ver}" >= "1.0"
Requires: sbcl = %{sbcl_ver}
%endif
Requires: %{name} = %{version}
Obsoletes: maxima-exec-sbcl < %{version}-%{release}
Provides: %{name}-runtime = %{version}
%description runtime-sbcl
Maxima compiled with Steel Bank Common Lisp (sbcl).
%endif


%prep
%setup -q  -n %{name}%{!?cvs:-%{version}%{?beta}}

# Extra docs
install -p -m644 %{SOURCE10} .

%if "%{?setarch_hack}" == "1"
%patch6 -p1 -b .gcl-setarch
%endif

sed -i -e 's|@ARCH@|%{_target_cpu}|' src/maxima.in

sed -i -e 's:/usr/local/info:/usr/share/info:' \
  interfaces/emacs/emaxima/maxima.el
sed -i -e \
  's/(defcustom\s+maxima-info-index-file\s+)(\S+)/$1\"maxima.info-16\"/' \
  interfaces/emacs/emaxima/maxima.el

# remove CVS crud
find -name CVS -type d | xargs rm -r


%build
%configure \
  %{?default_lisp:--with-default-lisp=%{default_lisp} } \
  %{?_enable_clisp} %{!?_enable_clisp: --disable-clisp } %{?_with_clisp_runtime} \
  %{?_enable_cmucl} %{!?_enable_cmucl: --disable-cmucl } %{?_with_cmucl_runtime} \
  %{?_enable_gcl}   %{!?_enable_gcl:   --disable-gcl } \
  %{?_enable_sbcl}  %{!?_enable_sbcl:  --disable-sbcl } \
  --enable-lang-es --enable-lang-es-utf8 \
  --enable-lang-pt --enable-lang-pt-utf8 \
  --enable-lang-pt_BR --enable-lang-pt_BR-utf8 

make %{?_smp_mflags}

# docs
pushd doc

 install -D -p -m644 %{SOURCE11} maximabook/maxima.pdf

# pushd info
#  texi2dvi --pdf maxima.texi
# popd

 pushd intromax
  pdflatex intromax.ltx
 popd

popd


%check 
make check


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# app icon
install -p -D -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/maxima.png

desktop-file-install \
  --dir="$RPM_BUILD_ROOT%{_datadir}/applications" \
  --vendor="fedora" \
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
# until we get/Require rlwrap from http://utopia.knoware.nl/~hlub/uck/rlwrap/
rm -f $RPM_BUILD_ROOT%{_bindir}/rmaxima
# docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/maxima/%{maxima_ver}/doc/{contributors,implementation,misc,maximabook,EMaximaIntro.ps}

# _enable_gcl: debuginfo (sometimes?) fails to get auto-created, so we'll help out
touch debugfiles.list


%post
/sbin/install-info %{_infodir}/maxima.info %{_infodir}/dir ||:
[ -x /usr/bin/texhash ] && /usr/bin/texhash 2> /dev/null ||:

%postun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/maxima.info %{_infodir}/dir ||:
  [ -x /usr/bin/texhash ] && /usr/bin/texhash 2> /dev/null ||:
fi

%post gui
touch --no-create %{_datadir}/icons/hicolor ||:

%postun gui
touch --no-create %{_datadir}/icons/hicolor ||:

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

%triggerin -- tetex-latex
if [ -d %{texmf}/tex/latex ]; then
  rm -rf %{texmf}/tex/latex/emaxima ||:
  ln -sf %{_datadir}/maxima/%{maxima_ver}/emacs %{texmf}/tex/latex/emaxima ||:
  %{_bindir}/texhash 2> /dev/null ||:
fi

%triggerun -- tetex-latex
if [ $2 -eq 0 ]; then
  rm -f %{texmf}/tex/latex/emaxima ||:
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README README.lisps
%doc doc/misc/ doc/implementation/
%doc doc/intromax/intromax.pdf
%doc doc/maximabook/maxima.pdf
%doc macref.pdf
%{_bindir}/maxima
%dir %{_datadir}/maxima
%dir %{_datadir}/maxima/%{maxima_ver}
%{_datadir}/maxima/%{maxima_ver}/[a-c,f-r,t-w,y-z,A-Z]*
%{_datadir}/maxima/%{maxima_ver}/demo/
%doc %{_datadir}/maxima/%{maxima_ver}/doc/
%doc %lang(es) %{_datadir}/maxima/%{maxima_ver}/doc/html/es*
%doc %lang(pt) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt/
%doc %lang(pt) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt.utf8/
%doc %lang(pt_BR) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt_BR*
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

%if "%{?_enable_clisp:1}" == "1"
%files runtime-clisp
%defattr(-,root,root,-)
%{_libdir}/maxima/%{maxima_ver}/binary-clisp
%endif

%if "%{?_enable_cmucl:1}" == "1"
%files runtime-cmucl
%defattr(-,root,root,-)
%{_libdir}/maxima/%{maxima_ver}/binary-cmucl
%endif

%if "%{?_enable_gcl:1}" == "1"
%files runtime-gcl
%defattr(-,root,root,-)
%{_libdir}/maxima/%{maxima_ver}/binary-gcl
%endif

%if "%{?_enable_sbcl:1}" == "1"
%files runtime-sbcl
%defattr(-,root,root,-)
%{_libdir}/maxima/%{maxima_ver}/binary-sbcl
%endif


%changelog
* Wed May 28 2008 Rex Dieter <rdieter@fedoraproject.org> - 5.15.0-1
- maxima-5.15.0
- omit ppc (sbcl, #448734)
- omit gcl (f10+ busted, for now)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.14.0-6
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Rex Dieter <rdieter@fedoraproject.org> 5.14.0-5
- respin (sbcl)

* Wed Jan 02 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 5.14.0-4
- x86_64: --disable-gcl (#427250)
- --disable-gcl (f9+, temporary, until broken deps fixed)

* Tue Jan 01 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 5.14.0-3
- (re)enable gcl

* Thu Dec 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.14.0-2
- respin (sbcl)

* Sat Dec 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.14.0-1
- maxima-5.14.0

* Mon Dec 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.99-0.3.rc2
- disable gcl (for now, doesn't build atm)

* Mon Dec 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.99-0.2.rc2
- maxima-5.13.99rc2

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.99-0.1.rc1
- maxima-5.13.99rc1

* Mon Nov 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.0-10
- rebuild against sbcl-1.0.12/clisp-2.43

* Sat Nov 03 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.0-8
- rebuild against sbcl-1.0.11

* Tue Oct 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.0-7
- rebuild against sbcl-1.0.10

* Fri Sep 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.0-6
- xmaxima.desktop: Categories=Development,Math

* Thu Aug 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.0-4
- (re)--enable-gcl, f8+ (#256281)
- fix inadvertant Obsoletes: maxima-runtime-gcl (f7)

* Mon Aug 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.0-3
- until it is unborked, disable gcl support, f8+ (#256281)
- --with-default-lisp=sbcl (was gcl)

* Sun Aug 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.0-2
- rebuild against sbcl-1.0.9

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.13.0-1
- maxima-5.13.0

* Sun Aug 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.12.99-0.5.rc2
- maxima-5.12.99rc2

* Thu Aug 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.12.99-0.4.rc1
- maxima-5.12.99rc1
- enable langpacks: es, pt, pt_BR

* Sat Jul 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.12.0-6
- respin for sbcl-1.0.8

* Fri Jul 20 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.12.0-5
- disable clisp/ppc, still awol (#166347)
- respin for sbcl-1.0.7

* Thu Jul 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.12.0-4
- enable clisp/ppc (#166347)
- revert koji hack.

* Tue May 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.12.0-3
- ExclusiveArch: %%ix86 -> i386 (for koji)

* Tue May 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.12.0-2
- respin for sbcl-1.0.6

* Thu May 03 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.12.0-1
- maxima-5.12.0

* Mon Apr 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.99-0.4.rc3
- maxima-5.11.99rc3

* Sun Apr 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.99-0.3.rc2
- fix sbcl/ppc build (#238376)

* Sun Apr 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.99-0.1.rc2
- maxima-5.11.99rc2

* Mon Mar 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.0-8
- respin for sbcl-1.0.4

* Wed Feb 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.0-7
- respin for sbcl-1.0.3

* Thu Jan 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.0-6
- respin for sbcl-1.0.2

* Fri Jan 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.0-5
- (re)enable ppc/sbcl builds (#220053)

* Thu Dec 28 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.0-4
- (re)--enable-sbcl

* Wed Dec 27 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.0-3
- updated xdg_utils patch (sent upstream)

* Thu Dec 21 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.0-2
- %%triggerin -- tetex-latex (for emaxima.sty)
- disable ppc builds (for now), sbcl/ppc is segfaulting (#220053)

* Thu Dec 21 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 5.11.0-1
- maxima-5.11.0 (#220512)

* Mon Dec 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.10.99-0.3.rc3
- maxima-5.10.99rc3

* Wed Dec 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.10.99-0.2.rc2
- maxima-5.10.99rc2

* Wed Dec 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.10.0-9
- respin (for sbcl-1.0)

* Fri Nov 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.10.0-8
- omit sbcl-disable-debugger patch (#214568)

* Thu Oct 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.10.0-7
- respin for sbcl-0.9.18
- fixup %%triggerun's
- drop dfi --add-category=X-Fedora

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.10.0-5
- update xdg-utils patch (for .dvi handling too)

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.10.0-4
- -gui: htmlview -> xdg-open, Requires: xdg-utils

* Tue Sep 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.10.0-2
- respin for sbcl-0.9.17

* Thu Sep 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.10.0-1
- 5.10.0

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3.99-0.10.rc4
- respin for new(er) sbcl (#207063)

* Wed Sep 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3.99-0.8.rc4
- 5.9.3.99rc4

* Wed Sep 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3.99-0.7.rc3
- 5.9.3.99rc3

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3.99-0.6.rc2
- fc6 respin

* Sun Aug 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3.99-0.5.rc2
- respin (against newer sbcl)

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3.99-0.4.rc2
- update gcl_setarch patch

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3.99-0.3.rc2
- 5.9.3.99rc2

* Tue Aug 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3.99-0.1.rc1
- 5.9.3.99rc1
- - %ghost (x)emacs site-lisp bits (hint from fedora-rpmdevtools)

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3-5
- respin for sbcl-0.9.14 (and relax Requires = to >= )

* Tue May 30 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3-4
- respin for sbcl-0.9.13

* Mon Apr 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3-3 
- respin, using new ppc bootstrap

* Fri Apr 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3-2.1
- try ppc build against sbcl

* Wed Apr 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3-2
- use setarch -X hack to allow runtime-gcl to function (#187647)
- respin for sbcl-0.9.12

* Wed Apr 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.3-1
- 5.9.3

* Thu Mar 30 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-13
- respin for sbcl-0.9.11

* Mon Mar 27 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc6+: BR: texinfo -> texinfo-tex (#186827)

* Thu Mar 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-12
- enable runtime-cmucl (%%ix86 only, atm)

* Wed Mar 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-11
- fc5: enable runtime-gcl
- runtime-sbcl: Requires: sbcl = %%{sbcl_version_used_to_build}

* Mon Feb 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-10
- respin for sbcl-0.9.10

* Thu Jan 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-9
- OK, loosen Req's again (buildsystem can't handle it)

* Thu Jan 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-8
- tighten Req: on clisp/sbcl runtimes

* Thu Jan 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-7
- rebuild for/with new clisp,sbcl

* Thu Oct 27 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-6
- --enable-sbcl
- avoid rpmquery's at build-time

* Sat Oct 22 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-4
- emaxima patch
- follow icon spec

* Wed Oct 18 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-3
- --with-default-lisp=clisp
- --with-clisp-runtime=%%_libdir/clisp/base/lisp.run

* Wed Oct 12 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.2-2
- 5.9.2

* Thu Oct 06 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1.9rc4-4
- cleanup _with,_enable macros
- -sbcl: --disable-debugger

* Tue Oct 04 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1.9rc4-3
- 5.9.1.9rc4
- banish _without_ macros, use only _with_ (absense of _with_foo implies
  _without_foo)

* Wed Sep 28 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1.9rc3-1
- 5.9.1.9rc3

* Mon Sep 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1.9rc2-1
- 5.9.1.9rc2

* Fri Sep 23 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1.9rc1-4
- --with-clisp only (for now)

* Thu Sep 22 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1.9rc1-3
- runtime-clisp: workaround "cpio: MD5 sum mismatch" error
- --with-gcl
- make %%_libdir/maxima owned by runtime pkgs

* Fri Sep 16 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1.9rc1-2
- -runtime-sbcl: with sbcl_ver macro
- use versioned maxima-exec Obsoletes.

* Mon Sep 12 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1.9rc1-1
- 5.9.1.9rc1

* Fri Sep 09 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1-5
- add more Obsoletes: maxima-exec- for cleaner upgrade from customized,
  rebuilt upstream rpms.
- (re)disable debuginfo.  No point in having empty -debuginfo pkgs.
- a few cleanups getting ready for 5.9.1.1cvs/5.9.2rc

* Tue Sep 06 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1-4
- workaround lack of debuginfo.list when building --with gcl
- ExcludeArch: ppc ppc64 (bug #166347)

* Mon Aug 29 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1-3
- BR: tk (/usr/bin/wish)
- trim %%description
- drop maxima book generation (use pregenerated copy)
- drop emaxima subpkg bits
- -src: lisp source subpkg

* Fri Aug 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1-2
- re-instate %%debuginfo
- put 'make check' in %%check section

* Wed Aug 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 5.9.1-1
- cleanup for Extras

* Fri Jan 28 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:5.9.1-0.fdr.6
- -clisp,-cmucl,-sbcl: Req >= lisp version that was used to build it.

* Thu Sep 30 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.1-0.fdr.5
- respin sbcl,clisp

* Wed Sep 29 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.1-0.fdr.4
- fix %%post/%%postun to handle the now-uncompressed info files
- relax runtime Req/Prov to not include %%release (so we don't have
  to rebuild *every* runtime on every package iteration

* Tue Sep 28 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.1-0.fdr.3
- use pregenerated maxima book and macref.pdf from
  http://maxima.sourceforge.net/docs.shtml

* Tue Sep 28 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.1-0.fdr.2
- fix/cleanup build_book=1 option

* Mon Sep 27 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.1-0.fdr.1
- 5.9.1 

* Fri Sep 17 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.0.9-0.fdr.0.7.rc1
- 5.9.0.9rc1

* Wed Aug 18 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.0.9-0.fdr.0.6.beta2
- updated sbcl patch

* Thu Aug 12 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.0.9-0.fdr.0.5.beta2
- -emaxima: renamed emacs -> emaxima 
- -emaxima: cleanup/expand LaTeX,emacs,xemacs bits
- (optionally) build maxima book (pdf)

* Wed Aug 11 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.0.9-0.fdr.0.4.beta2
- enable sbcl build, thanks to patch from
  http://www.math.utexas.edu/pipermail/maxima/2004/007802.html

* Tue Aug 10 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.0.9-0.fdr.0.3.beta2
- fix conflict with gcl-2.6.4

* Fri Aug 06 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.0.9-0.fdr.0.2.beta2
- (re)enable cmucl

* Wed Aug 04 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.0.9-0.fdr.0.1.beta2
- 5.9.0.9beta2 
- allow sbcl, disabled for now
- nix -emacs subpkg (for now)

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.0-0.fdr.7
- emacs subpkg
- drop cmucl support (cmucl doesn't build on fc2) 
- add desktop Categories: Education;Math;

* Fri Mar 26 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.0-0.fdr.5
- patch xmaxima to use htmlview instead of netscape
- move %%datadir/maxima/5.9.0/xmaxima to -gui pkg

* Thu Mar 25 2004 Rex Dieter <rexdieter at sf.net> 0:5.9.0-0.fdr.4
- desktop-file now default (unless desktop_file=0)

* Thu Dec 18 2003 Rex Dieter <rexdieter at sf.net> 0:5.9.0-0.fdr.3
- make %%post safer
- cleanup --without (clisp|cmucl|gcl) usage.
- use desktop-file-install (on platforms that support it)
- Requires(post,postun): /sbin/install-info

* Wed Oct 01 2003 Rex Dieter <rexdieter at sf.net> 0:5.9.0-0.fdr.2
- runtime-gcl: remove Requires: gcl, not needed after all.
- enable runtime-clisp 
- enable runtime-cmucl 

* Wed Sep 24 2003 Rex Dieter <rexdieter at sf.net> 0:5.9.0-0.fdr.1
- applnk/icon

* Wed Sep 17 2003 Rex Dieter <rexdieter at sf.net> 0:5.9.0-0.fdr.0
- fedora'ize 
