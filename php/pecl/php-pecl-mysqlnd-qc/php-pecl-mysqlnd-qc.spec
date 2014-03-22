# spec file for php-pecl-mysqlnd-qc
#
# Copyright (c) 2011-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package             php-pecl-mysqlnd-ms}
%{!?scl:         %global _root_prefix     %{_prefix}}
%{!?scl:         %global _root_sysconfdir %{_sysconfdir}}
%{!?php_inidir:  %global php_inidir       %{_sysconfdir}/php.d}
%{!?php_incldir: %global php_incldir      %{_includedir}/php}
%{!?__pecl:      %global __pecl           %{_bindir}/pecl}
%{!?__php:       %global __php            %{_bindir}/php}

%global pecl_name mysqlnd_qc
%global prever    alpha
%global with_zts  0%{?__ztsphp:1}

%if 0%{?fedora} < 9 && 0%{?rhel} < 6
%global with_sqlite 0
%else
%global with_sqlite 1
%endif

%if "%{?vendor}" == "Remi Collet"
%global with_memcache 1
%else
%if 0%{?fedora} < 14 && 0%{?rhel} < 7
%global with_memcache 0
%else
%global with_memcache 1
%endif
%endif


Summary:      A query cache plugin for mysqlnd
Name:         %{?scl_prefix}php-pecl-mysqlnd-qc
Version:      1.2.0
Release:      4%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/mysqlnd_qc

Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
# From http://www.php.net/manual/en/mysqlnd-qc.configuration.php
Source1:      mysqlnd_qc.ini
# Apache configuration for the web panel
Source2:      httpd.conf

# http://svn.php.net/viewvc?view=revision&revision=333056
# Fix for PHP 5.6
Patch0:       %{pecl_name}-svn.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel >= 5.3.4
BuildRequires: %{?scl_prefix}php-mysqlnd
BuildRequires: %{?scl_prefix}php-pear
%if %{with_memcache}
BuildRequires: libmemcached-devel >= 0.38
%endif
%if %{with_sqlite}
BuildRequires: sqlite-devel >= 3.5.9
%endif

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     %{?scl_prefix}php-mysqlnd%{?_isa}
Requires:     %{?scl_prefix}php-sqlite3%{?_isa}
Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}

Provides:     %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet"
# Other third party repo stuff
Obsoletes:     php53-pecl-mysqlnd-qc
Obsoletes:     php53u-pecl-mysqlnd-qc
Obsoletes:     php54-pecl-mysqlnd-qc
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-mysqlnd-qc
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-mysqlnd-qc
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The mysqlnd query result cache plugin is a mysqlnd plugin. 
It adds basic client side result set caching to all PHP MySQL extensions
(ext/mysql, ext/mysqli, PDO_MySQL). if they are compiled to use mysqlnd.
It does not change the API of the MySQL extensions and thus it operates
virtually transparent for applications.

Documentation : http://www.php.net/mysqlnd_qc

%package devel
Summary:       Mysqlnd_qc developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel

%description devel
These are the files needed to compile programs using mysqlnd_qc extension.


%package -n %{?scl_prefix}mysqlnd-qc-panel
Summary:       Mysqlnd Query Cache Monitor
Group:         Applications/Internet
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildArch:     noarch
%endif
Requires:      %{name} = %{version}-%{release}
Requires:      %{?scl_prefix}mod_php
Requires:      httpd

%description -n %{?scl_prefix}mysqlnd-qc-panel
This package provides the Mysqlnd Query Cache Monitor, with Apache
configuration, available on http://localhost/mysqlnd-qc/


%prep 
%setup -c -q

mv %{pecl_name}-%{version} NTS
cd NTS
%patch0 -p3 -b .svn

# Check version (often broken)
extver=$(sed -n '/#define MYSQLND_QC_VERSION_STR/{s/.* "//;s/".*$//;p}' php_mysqlnd_qc.h)
if test "x${extver}" != "x%{version}%{?prever:-}%{?prever}"; then
   : Error: Upstream %{pecl_name} version is now ${extver}, expecting %{version}%{?prever}.
   : Update the pdover macro and rebuild.
   exit 1
fi
cd ..

cp %{SOURCE1} %{pecl_name}.ini
sed -e 's:@DATADIR@:%{_datadir}:' \
    %{SOURCE2} >httpd.conf

%if %{with_zts}
# Build ZTS extension if ZTS devel available
cp -r NTS ZTS
%endif


%build
# required by libmemcached
LIBS="-lpthread"
export LIBS

peclconf() {
# don't use --enable-mysqlnd-qc-apc because:
# APC is onlysupported if both APC and MySQL Query Cache are compiled statically
%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-qc \
%if %{with_memcache}
    --enable-mysqlnd-qc-memcache \
    --with-libmemcached-dir=%{_root_prefix} \
%endif
%if %{with_sqlite}
    --enable-mysqlnd-qc-sqlite \
    --with-sqlite-dir=%{_root_prefix} \
%endif
    --with-php-config=$1
}

cd NTS
%{_bindir}/phpize
peclconf %{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclconf %{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Install the Apache configuration
install -D -m 644 httpd.conf %{buildroot}%{_root_sysconfdir}/httpd/conf.d/mysqlnd-qc-panel.conf

# Install the web interface
mkdir -p %{buildroot}%{_datadir}
cp -pr NTS/web %{buildroot}%{_datadir}/mysqlnd-qc

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
cd NTS
# only check if build extension can be loaded
%{__php} -n -q \
    -d extension=mysqlnd.so \
%if %{with_sqlite}
    -d extension=sqlite3.so \
%endif
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
cd ../ZTS
# only check if build extension can be loaded
%{__ztsphp} -n -q \
    -d extension=mysqlnd.so \
%if %{with_sqlite}
    -d extension=sqlite3.so \
%endif
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%files
%defattr(-, root, root, -)
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files devel
%defattr(-,root,root,-)
%doc %{pecl_testdir}/%{pecl_name}
%{_includedir}/php/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%files -n %{?scl_prefix}mysqlnd-qc-panel
%defattr(-,root,root,-)
%{_root_sysconfdir}/httpd/conf.d/mysqlnd-qc-panel.conf
%{_datadir}/mysqlnd-qc


%changelog
* Sat Mar 22 2014  Remi Collet <remi@fedoraproject.org> - 1.2.0-4
- add PHP 5.6 patch
- allow SCL build
- move doc in pecl_docdir
- move tests in pecl_testdir (devel)
- create mysqlnd-qc-panel sub package

* Tue Mar 12 2013  Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0-alpha

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.1.1-3.1
- also provides php-mysqlnd_qc

* Sat Sep 22 2012 Remi Collet <remi@fedoraproject.org> - 1.1.1-3
- rebuild for new libmemcached
- Obsoletes php53*, php54*

* Mon Apr 30 2012 Remi Collet <remi@fedoraproject.org> - 1.1.1-2
- rebuild for EL and PHP 5.4

* Mon Apr 30 2012  Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1-alpha
- add devel sub-package
- update configuration file provided
  add collect_statistics-log-file and ignore_sql_comments
  remove apc_prefix (not supported in this build)

* Mon Jan 30 2012  Remi Collet <remi@fedoraproject.org> - 1.1.0-0.1.svn322926
- new snapshot, update to 1.1.0-alpha

* Mon Nov 21 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-3.svn322926
- fix from svn, build against php 5.4

* Sun Sep 18 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- build zts extension

* Sun Sep 18 2011  Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial RPM
