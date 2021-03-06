# remirepo spec file for php-pecl-sphinx
#
# Copyright (c) 2011-2017 Remi Collet
#
# Fedora spec file for php-pecl-sphinx
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-selinux
%endif

# https://github.com/php/pecl-search_engine-sphinx/tree/php7
%global gh_commit   201eb00bd370bf8ff2d5787ac1a1b588f14af5a0
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    php
%global gh_project  pecl-search_engine-sphinx
%global gh_date     20170203

%global pecl_name   sphinx
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name    40-%{pecl_name}.ini

Name:           %{?sub_prefix}php-pecl-sphinx
Version:        1.4.0
%if 0%{?gh_date:1}
Release:        0.2.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif
Summary:        PECL extension for Sphinx SQL full-text search engine
Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/%{pecl_name}
%if 0%{?gh_date:1}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz
%else
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
%endif

BuildRequires:  libsphinxclient-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-devel > 7

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension provides PHP bindings for libsphinxclient, 
client library for Sphinx the SQL full-text search engine.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
%if 0%{?gh_date:1}
mv %{gh_project}-%{gh_commit} NTS
%{__php} -r '
  $pkg = simplexml_load_file("NTS/package.xml");
  $pkg->date = substr("%{gh_date}",0,4)."-".substr("%{gh_date}",4,2)."-".substr("%{gh_date}",6,2);
  $pkg->version->release = "%{version}dev";
  $pkg->stability->release = "devel";
  $pkg->asXML("package.xml");
'
%else
mv %{pecl_name}-%{version} NTS
%endif

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS

# Check reported version (phpinfo), as this is often broken
extver=$(sed -n '/#define PHP_SPHINX_VERSION/{s/.* "//;s/".*$//;p}' php_sphinx.h)
if test "x${extver}" != "x%{version}%{?gh_date:-dev}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?gh_date:-dev}.
   exit 1
fi
cd ..

cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
%{?dtsenable}

cd NTS
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%check
: simple module load test for the NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: simple module load test for the ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%install
%{?dtsenable}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Fri Feb  3 2017 Remi Collet <remi@remirepo.net> - 1.4.0-0.2.20170203git201eb00
- update to 1.4.0-dev (git snapshot) for PHP 7
- refresh with fix for 32bits

* Fri Feb  3 2017 Remi Collet <remi@remirepo.net> - 1.4.0-0.1.20160323git9a3d08c
- update to 1.4.0-dev (git snapshot) for PHP 7
- x86_64 only as i386 is broken

* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-3
- adapt for F24

* Tue Jun 23 2015 Remi Collet <remi@fedoraproject.org> - 1.3.3-2
- allow build against rh-php56 (as more-php56)

* Thu May 21 2015 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- Update to 1.3.3
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.3.2-2.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.3.2-2
- improve SCL build

* Tue May 06 2014 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2 (stable)

* Tue May 06 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1 (stable)

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.3.0-5
- add numerical prefix to extension configuration file (php 5.6)

* Mon Mar 24 2014 Remi Collet <remi@fedoraproject.org> - 1.3.0-4
- allow SCL build

* Thu Mar 13 2014 Remi Collet <remi@fedoraproject.org> - 1.3.0-3
- cleanups
- install doc in pecl_docdir
- add missing License file

* Sun May 12 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-2
- Rebuild against latest libsphinx

* Thu Apr 04 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Fri Nov 30 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-2.1
- also provides php-sphinx

* Sat Apr 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-2
- update to 1.2.0, php 5.4

* Sat Apr 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- update to 1.2.0

* Mon Nov 21 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-3
- add patch for php 5.4, see https://bugs.php.net/60349

* Wed Oct 05 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-2
- ZTS extension
- spec cleanups

* Sat Jul 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-1
- rebuild for remi repository

* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.1.0-1
- Update to latest upstream
- Fix bugzilla #715830

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 26 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.0.4-1
- update to 1.0.4

* Sat Sep 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-2
- rebuild for remi repository and PHP 5.3

* Sun Sep 06 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-2
- Add checks
- Add php-devel version requirement

* Wed Aug 05 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-1
- Initial package
