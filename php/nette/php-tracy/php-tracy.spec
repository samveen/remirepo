# remirepo/fedora spec file for php-tracy
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    152b7602115dd3a66f3190280951390097a15f65
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   tracy
%global ns_vendor    Tracy
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_project}
Version:        2.3.11
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Tracy: useful PHP debugger

Group:          Development/Libraries
License:        BSD or GPLv2 or GPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# pull a git snapshot to get test sutie
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.1
BuildRequires:  php-date
BuildRequires:  php-iconv
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-posix
BuildRequires:  php-reflection
BuildRequires:  php-session
BuildRequires:  php-spl
BuildRequires:  php-xml
# From composer.json, "require-dev": {
#        "nette/di": "~2.3",
#        "nette/tester": "~1.3"
BuildRequires:  php-composer(%{gh_owner}/di) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/tester) >= 1.3
%endif

# from composer.json, "require": {
#        "php": ">=5.3.1"
Requires:       php(language) >= 5.3.1
# from phpcompatinfo report for version 2.3.5, XDebug is optional
Requires:       php-date
Requires:       php-iconv
Requires:       php-json
Requires:       php-pcre
Requires:       php-posix
Requires:       php-reflection
Requires:       php-session
Requires:       php-spl
Requires:       php-xml

# provides tracy/tracy
Provides:       php-composer(%{gh_project}/%{gh_project}) = %{version}


%description
Tracy library is a useful PHP everyday programmer's helper. It helps you to:

- quickly detect and correct errors
- log errors
- dump variables
- measure the time

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# drop upstream autoloader which is outside tree
rm src/tracy.php
# move
mv src/shortcuts.php src/%{ns_vendor}
mv src/Bridges       src/%{ns_vendor}


%build
: Generate a classmap autoloader
phpab --output src/%{ns_vendor}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_vendor}/autoload.php
require_once __DIR__ . '/shortcuts.php';
EOF


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{php_home}
cp -pr src/* %{buildroot}%{php_home}/


%check
%if %{with_tests}
: Generate configuration
cat /etc/php.ini /etc/php.d/*ini >php.ini
export LANG=fr_FR.utf8

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{php_home}/Nette/DI/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/autoload.php';
EOF

: Run test suite in sources tree
%{_bindir}/nette-tester --colors 0 -p php -c ./php.ini tests -s

if which php70; then
  cat /etc/opt/remi/php70/php.ini /etc/opt/remi/php70/php.d/*ini >php.ini
  php70 %{_bindir}/nette-tester --colors 0 -p php70 -c ./php.ini tests -s
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license license.md
%doc readme.md contributing.md
%doc composer.json
%{php_home}/%{ns_vendor}


%changelog
* Mon May 30 2016 Remi Collet <remi@fedoraproject.org> - 2.3.11-1
- update to 2.3.11

* Mon Feb 29 2016 Remi Collet <remi@fedoraproject.org> - 2.3.10-1
- update to 2.3.10

* Mon Feb 22 2016 Remi Collet <remi@fedoraproject.org> - 2.3.9-1
- update to 2.3.9

* Sun Feb 14 2016 Remi Collet <remi@fedoraproject.org> - 2.3.8-2
- add upstream patch for new PHP

* Wed Jan 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.8-1
- update to 2.3.8
- run test suite with both php 5 and 7 when available

* Mon Nov 30 2015 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- update to 2.3.7

* Thu Oct 29 2015 Remi Collet <remi@fedoraproject.org> - 2.3.6-1
- update to 2.3.6

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 2.3.5-1
- initial package
