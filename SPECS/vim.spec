%define debug_package %{nil}

%define patchlevel 0678
%define baseversion 8.1
%define vimdir vim81
%define vimdirsrc vim-%{baseversion}.%{patchlevel}

%define WITH_SELINUX 0
%define withnetbeans 0
%define withvimspell 0
%define withhunspell 0
%define withruby 1
%define withlua 1

%if %{?rhel}%{!?rhel:0} == 7
%define tlib		ncurses
%define python2		python2.7
%define rubyopt 	dynamic
%else
%define tlib		tinfo
%define python2		python2.6
%define rubyopt 	yes
%endif

Name:		vim8
Version:	%{baseversion}.%{patchlevel}	
Release:	1%{?dist}
Summary:	The VIM editor

Group:		Applications/Editors
License:	Vim
URL:		http://www.vim.org/
Source0:	https://github.com/vim/vim/archive/v%{baseversion}.%{patchlevel}.tar.gz

Patch3004:      vim-7.0-rclocation.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: lua-devel,python-devel,ruby,ruby-devel,ncurses-devel
BuildRequires: python34u-devel,python35u-devel,python36u-devel
%if %{?rhel}%{!?rhel:0} == 7
BuildRequires: rh-python34-python-devel
%endif
BuildRequires: rh-python35-python-devel,rh-python36-python-devel
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))	
Requires:	vim-common

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.


%prep
# change vim directory in github's tgz
if ! tar -tf %{SOURCE0} %{vimdir}/README.txt; then
    cd ../SOURCES
    tar -zxf %{SOURCE0} > /dev/null
    mv %{vimdirsrc} %{vimdir}
    rm -f %{SOURCE0}
    tar -zcf %{SOURCE0} %{vimdir}
    rm -fr %{vimdirsrc} %{vimdir}
    rm -fr %{vimdir}
    cd ../BUILD
fi

rm -fr %{build}
%setup -q -b 0 -n %{vimdir}

%patch3004 -p1


# ---------------------------------------------------------------------------- #
# ---------------------------------< SCRIPT >--------------------------------- #
# ---------------------------------------------------------------------------- #

%build
cd src
autoconf

sed -e "s+VIMRCLOC	= \$(VIMLOC)+VIMRCLOC	= /etc+" Makefile > Makefile.tmp
mv -f Makefile.tmp Makefile

# ---------------------------------------------------------------------------- #
# compile py34
# ---------------------------------------------------------------------------- #
%define python3		python3.4m
%define python3conf	/usr/lib64/python3.4/config-3.4m
%define python3path	%{_includedir}/%{python3}
%define python3bin	%{_bindir}/%{python3}

export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"

%configure --with-features=huge \
    --enable-pythoninterp=dynamic \
    --with-python-config-dir=/usr/lib64/%{python2}/config \
    --enable-python3interp=dynamic vi_cv_path_python3=%{python3bin} \
    --with-python3-config-dir=%{python3conf} \
    --disable-tclinterp \
    --with-x=no \
    --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
    --enable-cscope --with-modified-by="<funkypythonista@gmail.com>" \
    --with-tlib=%{tlib} \
    --with-compiledby="<funkypythonista@gmail.com>" \
%if "%{withnetbeans}" == "1"
    --enable-netbeans \
%else
    --disable-netbeans \
%endif
%if %{WITH_SELINUX}
    --enable-selinux \
%else
    --disable-selinux \
%endif
%if "%{withruby}" == "1"
    --enable-rubyinterp=%{rubyopt} \
%else
    --disable-rubyinterp \
%endif
%if "%{withlua}" == "1"
    --enable-luainterp=dynamic \
%else
    --disable-luainterp \
%endif
    --enable-fail-if-missing

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim vim8-py34
make clean


# ---------------------------------------------------------------------------- #
# compile py35
# ---------------------------------------------------------------------------- #
%define python3		python3.5m
%define python3conf	/usr/lib64/python3.5/config-3.5m
%define python3path	%{_includedir}/%{python3}
%define python3bin	%{_bindir}/%{python3}

export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"

%configure --with-features=huge \
    --enable-pythoninterp=dynamic \
    --with-python-config-dir=/usr/lib64/%{python2}/config \
    --enable-python3interp=dynamic vi_cv_path_python3=%{python3bin} \
    --with-python3-config-dir=%{python3conf} \
    --disable-tclinterp \
    --with-x=no \
    --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
    --enable-cscope --with-modified-by="<funkypythonista@gmail.com>" \
    --with-tlib=%{tlib} \
    --with-compiledby="<funkypythonista@gmail.com>" \
%if "%{withnetbeans}" == "1"
    --enable-netbeans \
%else
    --disable-netbeans \
%endif
%if %{WITH_SELINUX}
    --enable-selinux \
%else
    --disable-selinux \
%endif
%if "%{withruby}" == "1"
    --enable-rubyinterp=%{rubyopt} \
%else
    --disable-rubyinterp \
%endif
%if "%{withlua}" == "1"
    --enable-luainterp=dynamic \
%else
    --disable-luainterp \
%endif
    --enable-fail-if-missing

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim vim8-py35
make clean

# ---------------------------------------------------------------------------- #
# compile py36
# ---------------------------------------------------------------------------- #
%define python3		python3.6m
%define python3conf	/usr/lib64/python3.6/config-3.6m-x86_64-linux-gnu
%define python3path	%{_includedir}/%{python3}
%define python3bin	%{_bindir}/%{python3}

export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"

%configure --with-features=huge \
    --enable-pythoninterp=dynamic \
    --with-python-config-dir=/usr/lib64/%{python2}/config \
    --enable-python3interp=dynamic vi_cv_path_python3=%{python3bin} \
    --with-python3-config-dir=%{python3conf} \
    --disable-tclinterp \
    --with-x=no \
    --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
    --enable-cscope --with-modified-by="<funkypythonista@gmail.com>" \
    --with-tlib=%{tlib} \
    --with-compiledby="<funkypythonista@gmail.com>" \
%if "%{withnetbeans}" == "1"
    --enable-netbeans \
%else
    --disable-netbeans \
%endif
%if %{WITH_SELINUX}
    --enable-selinux \
%else
    --disable-selinux \
%endif
%if "%{withruby}" == "1"
    --enable-rubyinterp=%{rubyopt} \
%else
    --disable-rubyinterp \
%endif
%if "%{withlua}" == "1"
    --enable-luainterp=dynamic \
%else
    --disable-luainterp \
%endif
    --enable-fail-if-missing

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim vim8-py36
make clean

# ---------------------------------------------------------------------------- #
# compile rhpy34
# ---------------------------------------------------------------------------- #
%if %{?rhel}%{!?rhel:0} == 7
%define python3		python3.4m
%define python3conf	/opt/rh/rh-python34/root/usr/lib64/python3.4/config-3.4m
%define python3path	/opt/rh/rh-python34/root/usr/include/%{python3}
%define python3bin	/opt/rh/rh-python34/root/usr/bin/%{python3}

export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"

export LD_LIBRARY_PATH=/opt/rh/rh-python34/root/usr/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

%configure --with-features=huge \
    --enable-pythoninterp=dynamic \
    --with-python-config-dir=/usr/lib64/%{python2}/config \
    --enable-python3interp=dynamic vi_cv_path_python3=%{python3bin} \
    --with-python3-config-dir=%{python3conf} \
    --disable-tclinterp \
    --with-x=no \
    --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
    --enable-cscope --with-modified-by="<funkypythonista@gmail.com>" \
    --with-tlib=%{tlib} \
    --with-compiledby="<funkypythonista@gmail.com>" \
%if "%{withnetbeans}" == "1"
    --enable-netbeans \
%else
    --disable-netbeans \
%endif
%if %{WITH_SELINUX}
    --enable-selinux \
%else
    --disable-selinux \
%endif
%if "%{withruby}" == "1"
    --enable-rubyinterp=%{rubyopt} \
%else
    --disable-rubyinterp \
%endif
%if "%{withlua}" == "1"
    --enable-luainterp=dynamic \
%else
    --disable-luainterp \
%endif
    --enable-fail-if-missing

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim vim8-rhpy34
make clean
%endif

# ---------------------------------------------------------------------------- #
# compile rhpy35
# ---------------------------------------------------------------------------- #
%define python3		python3.5m
%define python3conf	/opt/rh/rh-python35/root/usr/lib64/python3.5/config-3.5m
%define python3path	/opt/rh/rh-python35/root/usr/include/%{python3}
%define python3bin	/opt/rh/rh-python35/root/usr/bin/%{python3}

export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"

export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

%configure --with-features=huge \
    --enable-pythoninterp=dynamic \
    --with-python-config-dir=/usr/lib64/%{python2}/config \
    --enable-python3interp=dynamic vi_cv_path_python3=%{python3bin} \
    --with-python3-config-dir=%{python3conf} \
    --disable-tclinterp \
    --with-x=no \
    --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
    --enable-cscope --with-modified-by="<funkypythonista@gmail.com>" \
    --with-tlib=%{tlib} \
    --with-compiledby="<funkypythonista@gmail.com>" \
%if "%{withnetbeans}" == "1"
    --enable-netbeans \
%else
    --disable-netbeans \
%endif
%if %{WITH_SELINUX}
    --enable-selinux \
%else
    --disable-selinux \
%endif
%if "%{withruby}" == "1"
    --enable-rubyinterp=%{rubyopt} \
%else
    --disable-rubyinterp \
%endif
%if "%{withlua}" == "1"
    --enable-luainterp=dynamic \
%else
    --disable-luainterp \
%endif
    --enable-fail-if-missing

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim vim8-rhpy35
make clean

# ---------------------------------------------------------------------------- #
# compile rhpy36
# ---------------------------------------------------------------------------- #
%define python3		python3.6m
%define python3conf	/opt/rh/rh-python36/root/usr/lib64/python3.6/config-3.6m-x86_64-linux-gnu
%define python3path	/opt/rh/rh-python36/root/usr/include/%{python3}
%define python3bin	/opt/rh/rh-python36/root/usr/bin/%{python3}

export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -I%{python3path}"

export LD_LIBRARY_PATH=/opt/rh/rh-python36/root/usr/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

%configure --with-features=huge \
    --enable-pythoninterp=dynamic \
    --with-python-config-dir=/usr/lib64/%{python2}/config \
    --enable-python3interp=dynamic vi_cv_path_python3=%{python3bin} \
    --with-python3-config-dir=%{python3conf} \
    --disable-tclinterp \
    --with-x=no \
    --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
    --enable-cscope --with-modified-by="<funkypythonista@gmail.com>" \
    --with-tlib=%{tlib} \
    --with-compiledby="<funkypythonista@gmail.com>" \
%if "%{withnetbeans}" == "1"
    --enable-netbeans \
%else
    --disable-netbeans \
%endif
%if %{WITH_SELINUX}
    --enable-selinux \
%else
    --disable-selinux \
%endif
%if "%{withruby}" == "1"
    --enable-rubyinterp=%{rubyopt} \
%else
    --disable-rubyinterp \
%endif
%if "%{withlua}" == "1"
    --enable-luainterp=dynamic \
%else
    --disable-luainterp \
%endif
    --enable-fail-if-missing

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim vim8-rhpy36

# ---------------------------------------------------------------------------- #
# install
# ---------------------------------------------------------------------------- #
%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/vim/%{vimdir}/{after,autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
mkdir -p %{buildroot}/%{_datadir}/vim/%{vimdir}/after/{autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
cp runtime/doc/uganda.txt LICENSE
rm -f README*.info


cd src
make install DESTDIR=%{buildroot} BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
make installgtutorbin  DESTDIR=%{buildroot} BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}

rm -fr %{buildroot}%{_bindir}/*
rm -fr %{buildroot}%{_datadir}/man
rm -fr %{buildroot}%{_datadir}/icons
rm -fr %{buildroot}%{_datadir}/applications
rm -fr %{buildroot}/%{_datadir}/vim/%{vimdir}/tools
rm -f vim8
ln -sf %{_sysconfdir}/alternatives/vim8 vim8
cp -d vim8 %{buildroot}%{_bindir}/vim8
#install -m755 vim8 %{buildroot}%{_bindir}/vim8
install -m755 vim8-py34 %{buildroot}%{_bindir}/vim8-py34
install -m755 vim8-py35 %{buildroot}%{_bindir}/vim8-py35
install -m755 vim8-py36 %{buildroot}%{_bindir}/vim8-py36
%if %{?rhel}%{!?rhel:0} == 7
install -m755 vim8-rhpy34 %{buildroot}%{_bindir}/vim8-rhpy34
%endif
install -m755 vim8-rhpy35 %{buildroot}%{_bindir}/vim8-rhpy35
install -m755 vim8-rhpy36 %{buildroot}%{_bindir}/vim8-rhpy36


%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc READMEdir/README*
%{_bindir}/vim8
%{_bindir}/vim8-py34
%{_bindir}/vim8-py35
%{_bindir}/vim8-py36
%if %{?rhel}%{!?rhel:0} == 7
%{_bindir}/vim8-rhpy34
%endif
%{_bindir}/vim8-rhpy35
%{_bindir}/vim8-rhpy36
%{_datadir}/vim/%{vimdir}

# ---------------------------------------------------------------------------- #
# %post
# ---------------------------------------------------------------------------- #
%post
if [ $1 == 1 ];then
    # initial install
%if %{?rhel}%{!?rhel:0} == 7
    alternatives --install /usr/bin/vim8 vim8 /usr/bin/vim8-rhpy34 4
%endif
    alternatives --install /usr/bin/vim8 vim8 /usr/bin/vim8-rhpy35 5
    alternatives --install /usr/bin/vim8 vim8 /usr/bin/vim8-rhpy36 5
    alternatives --install /usr/bin/vim8 vim8 /usr/bin/vim8-py34 34
    alternatives --install /usr/bin/vim8 vim8 /usr/bin/vim8-py35 35
    alternatives --install /usr/bin/vim8 vim8 /usr/bin/vim8-py36 36
    if [ -f /usr/bin/python3.6m ]; then
        alternatives --set vim8 /usr/bin/vim8-py36
    elif [ -f /usr/bin/python3.5m ]; then
        alternatives --set vim8 /usr/bin/vim8-py35
    elif [ -f /usr/bin/python3.4m ]; then
        alternatives --set vim8 /usr/bin/vim8-py34
    elif [ -f /opt/rh/rh-python36/root/usr/bin/python3.6m ]; then
        alternatives --set vim8 /usr/bin/vim8-rhpy36
    elif [ -f /opt/rh/rh-python35/root/usr/bin/python3.5m ]; then
        alternatives --set vim8 /usr/bin/vim8-rhpy35
%if %{?rhel}%{!?rhel:0} == 7
    elif [ -f /opt/rh/rh-python34/root/usr/bin/python3.4m ]; then
        alternatives --set vim8 /usr/bin/vim8-rhpy34
%endif
    else
        alternatives --auto vim8
    fi
elif [ $1 == 2 ];then
    echo "upgrading. do nothing"
fi

# ---------------------------------------------------------------------------- #
# %postun
# ---------------------------------------------------------------------------- #
%postun
if [ $1 == 1 ];then
    echo "upgrading"
elif [ $1 == 0 ];then
    echo "removing"
%if %{?rhel}%{!?rhel:0} == 7
    alternatives --remove vim8 /usr/bin/vim8-rhpy34
%endif
    alternatives --remove vim8 /usr/bin/vim8-rhpy35
    alternatives --remove vim8 /usr/bin/vim8-rhpy36
    alternatives --remove vim8 /usr/bin/vim8-py34
    alternatives --remove vim8 /usr/bin/vim8-py35
    alternatives --remove vim8 /usr/bin/vim8-py36
fi


%changelog

