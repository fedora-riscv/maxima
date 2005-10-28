
Summary: Symbolic Computation Program
Name: 	 maxima
Version: 5.9.2

Release: 6%{?dist} 
License: GPL
Group:	 Applications/Engineering 
URL: 	 http://maxima.sourceforge.net/
Source:	 http://dl.sourceforge.net/sourceforge/maxima/maxima-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# add ppc (and maybe ppc64)  when lisps build again on ppc 
#  (clisp: http://bugzilla.redhat.com/bugzilla/166347) 
ExclusiveArch: %{ix86} x86_64 

%define _with_default_lisp --with-default-lisp=clisp

%ifarch %{ix86} x86_64
%define _enable_clisp --enable-clisp 
# cmucl review pending: http://bugzilla.redhat.com/bugzilla/166796
#define _enable_cmucl --enable-cmucl 
# gcl not built for fc5/development (yet)
%if "%{?fedora}" < "5"
%define _enable_gcl --enable-gcl 
%endif
%define _enable_sbcl --enable-sbcl 
%endif

%ifarch ppc
#define _enable_clisp --enable-clisp 
#define _enable_cmucl --enable-cmucl 
#define _enable_gcl --enable-gcl 
#define _enable_sbcl --enable-sbcl 
%endif

Source1: maxima.png
Source2: xmaxima.desktop
Source6: maxima-modes.el

## Other maxima reference docs
Source10: http://starship.python.net/crew/mike/TixMaxima/macref.pdf
Source11: http://maxima.sourceforge.net/docs/maximabook/maximabook-19-Sept-2004.pdf

Patch1: maxima-5.9.2-htmlview.patch
# (mysterious?) xemacs patch (don't use, for now)
Patch2: maxima.el-xemacs.patch
# use sbcl --disable-debugger
Patch3: maxima-5.9.2-sbcl-disable-debugger.patch
# ghostview -> evince (ps/pdf viewer)
Patch4: maxima-5.9.2-evince.patch
# emaxima fix from Camm Maguire
Patch5: maxima-5.9.2-emaxima.patch

# Inhibit automatic compressing of info files. Compressed info
# files break maxima's internal help.
%define __spec_install_post %{nil} 
# debuginfo.list ends up empty/blank anyway. disable
%define debug_package   %{nil}

BuildRequires: time
BuildRequires: texinfo
BuildRequires: tetex-latex
BuildRequires: desktop-file-utils
# /usr/bin/wish
BuildRequires: tk
BuildRequires: automake

Requires: %{name}-runtime = %{version}
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
%define _with_clisp_runtime --with-clisp-runtime=%{_libdir}/clisp/base/lisp.run
%package runtime-clisp
Summary: Maxima compiled with clisp
Group:	 Applications/Engineering
BuildRequires: clisp-devel
# To appease those who are paranoid about rpm queries at build time
#define clisp_ver %{expand:%%(rpm -q --qf '%%{VERSION}' clisp )}
Requires: clisp %{?clisp_ver: >= %{clisp_ver}}
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
Obsoletes: maxima-exec-gcl < %{version}-%{release}
Provides:  %{name}-runtime = %{version}
%description runtime-gcl
Maxima compiled with Gnu Common Lisp (gcl)
%endif

%if "%{?_enable_sbcl:1}" == "1"
%package runtime-sbcl
Summary: Maxima compiled with SBCL 
Group:   Applications/Engineering
BuildRequires: sbcl >= 0.9.6
## To appease those who are paranoid about rpm queries at build time
#define sbcl_ver %{expand:%%(rpm -q --qf '%%{VERSION}' sbcl )}
Requires: sbcl %{?sbcl_ver: >= %{sbcl_ver}} 
Requires: %{name} = %{version}
Obsoletes: maxima-exec-sbcl < %{version}-%{release}
Provides: %{name}-runtime = %{version}
%description runtime-sbcl
Maxima compiled with Steel Bank Common Lisp (sbcl).
%endif


%prep
%setup -q  -n %{name}%{!?cvs:-%{version}}

# Extra docs
install -p -m644 %{SOURCE10} .

%patch1 -p1 -b .htmlview
#patch2 -p1 -b .xemacs
%if "%{?fedora}" > "3"
%patch4 -p1 -b .evince
%endif
%patch5 -p1 -b .emaxima

sed -i -e 's:/usr/local/info:/usr/share/info:' \
  interfaces/emacs/emaxima/maxima.el
sed -i -e \
  's/(defcustom\s+maxima-info-index-file\s+)(\S+)/$1\"maxima.info-16\"/' \
  interfaces/emacs/emaxima/maxima.el

# remove CVS crud
find -name CVS -type d | xargs rm -r

%if "%{?_enable_sbcl:1}" == "1"
%patch3 -p1 -b .sbcl-disable-debugger
# seems to be needed only if --enable-sbcl
aclocal
automake --add-missing --copy
autoconf
%endif


%build
%configure \
  %{?_with_default_lisp} \
  %{?_enable_clisp} %{?_with_clisp_runtime} %{!?_enable_clisp: --disable-clisp } \
  %{?_enable_cmucl} %{?_with_cmucl_runtime} %{!?_enable_cmucl: --disable-cmucl } \
  %{?_enable_gcl} %{!?_enable_gcl: --disable-gcl } \
  %{?_enable_sbcl} %{!?_enable_sbcl: --disable-sbcl }

make %{?_smp_mflags}

# docs
pushd doc

 install -D -p -m644 %{SOURCE11} maximabook/maxima.pdf

 pushd info
  texi2dvi -p maxima.texi
 popd

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

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category "X-Fedora" \
  %{SOURCE2} 

## emaxima
# LaTeX style
install -d $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/emaxima
cp -alf $RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/emacs/*.sty \
	$RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/emaxima/
# emacs
install -d $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/{maxima,site-start.d}
cp -alf $RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/emacs/*.el \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/emacs/*.lisp \
	$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/maxima/
install -D -m644 -p %{SOURCE6} \
	$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/maxima.el

# xemacs
install -d $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/{maxima,site-start.d}
cp -alf $RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/emacs/*.el \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/emacs/*.lisp \
	$RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/maxima/
install -D -m644 -p %{SOURCE6} \
	$RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/site-start.d/maxima.el

## unwanted/unpackaged files
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
# until we get/Require rlwrap from http://utopia.knoware.nl/~hlub/uck/rlwrap/
rm -f $RPM_BUILD_ROOT%{_bindir}/rmaxima
# docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/maxima/%{version}/doc/{contributors,implementation,misc,maximabook,EMaximaIntro.ps}

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
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun gui
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL README README.lisps
%doc doc/misc/ doc/implementation/
%doc doc/intromax/intromax.pdf
%doc doc/maximabook/maxima.pdf
%doc macref.pdf
%doc %{_datadir}/maxima/%{version}/doc
%{_bindir}/maxima
%dir %{_datadir}/maxima
%dir %{_datadir}/maxima/%{version}
%{_datadir}/maxima/%{version}/[a-c,f-r,t-w,y-z,A-Z]*
%{_datadir}/maxima/%{version}/demo/
%{_datadir}/maxima/%{version}/share/
%{_libexecdir}/maxima
%{_infodir}/*.info*
%{_mandir}/man1/maxima.*
# emaxima     
%{_datadir}/maxima/%{version}/emacs
%{_datadir}/emacs/site-lisp/*
%{_datadir}/xemacs/site-packages/*
%{_datadir}/texmf/tex/latex/emaxima/

%files src
%defattr(-,root,root)
%{_datadir}/maxima/%{version}/src/

%files gui
%defattr(-,root,root)
%{_bindir}/xmaxima
%{_datadir}/maxima/%{version}/xmaxima
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*

%if "%{?_enable_clisp:1}" == "1"
%files runtime-clisp
%defattr(-,root,root)
%dir %{_libdir}/maxima/
%dir %{_libdir}/maxima/%{version}/
%{_libdir}/maxima/%{version}/binary-clisp
%endif

%if "%{?_enable_cmucl:1}" == "1"
%files runtime-cmucl
%defattr(-,root,root)
%dir %{_libdir}/maxima/
%dir %{_libdir}/maxima/%{version}/
%{_libdir}/maxima/%{version}/binary-cmucl
%endif

%if "%{?_enable_gcl:1}" == "1"
%files runtime-gcl
%defattr(-,root,root)
%dir %{_libdir}/maxima/
%dir %{_libdir}/maxima/%{version}/
%{_libdir}/maxima/%{version}/binary-gcl
%endif

%if "%{?_enable_sbcl:1}" == "1"
%files runtime-sbcl
%defattr(-,root,root)
%dir %{_libdir}/maxima/
%dir %{_libdir}/maxima/%{version}/
%{_libdir}/maxima/%{version}/binary-sbcl
%endif


%changelog
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
