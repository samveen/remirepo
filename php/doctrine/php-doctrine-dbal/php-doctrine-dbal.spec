# remirepo spec file for php-doctrine-dbal, from Fedora:
#
# Fedora spec file for php-doctrine-dbal
#
# Copyright (c) 2013-2017 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Adam Williamson <awilliam@redhat.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      dbal
%global github_version   2.5.12
%global github_commit    7b9e911f9d8b30d43b96853dab26898c710d8f44

%global composer_vendor  doctrine
%global composer_project dbal

# "php": ">=5.3.2"
%global php_min_ver 5.3.2
# "doctrine/common": ">=2.4,<2.8-dev"
#     NOTE: Min version not 2.4 because autoloader required
%global doctrine_common_min_ver 2.5.0
%global doctrine_common_max_ver 2.8
# "symfony/console": "2.*||^3.0"
%global symfony_console_min_ver 2.0
%global symfony_console_max_ver 4.0

%{!?phpdir:  %global phpdir  %{_datadir}/php}

%if 0%{?rhel} == 5
# No test as no SQlite3 ext
%global with_tests 0
%else
# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}
%endif

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Doctrine Database Abstraction Layer (DBAL)

Group:         Development/Libraries
License:       MIT
URL:           http://www.doctrine-project.org/projects/dbal.html

# Run "php-doctrine-dbal-get-source.sh" to create source
Source0:       %{name}-%{version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

# Update bin script:
# 1) Add she-bang
# 2) Auto-load using Doctrine\Common\ClassLoader
Patch0:        %{name}-bin.patch

# Fix test suite using PHPUnit 5.4
Patch1:        %{name}-phpunit54.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(doctrine/common) >= %{doctrine_common_min_ver}
BuildRequires: php-composer(doctrine/common) <  %{doctrine_common_max_ver}
## composer.json (optional)
BuildRequires: php-composer(symfony/console) >= %{symfony_console_min_ver}
BuildRequires: php-composer(symfony/console) <  %{symfony_console_max_ver}
## phpcompatinfo (computed from version 2.5.12)
BuildRequires: php-date
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-pdo
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(doctrine/common) >= %{doctrine_common_min_ver}
Requires:      php-composer(doctrine/common) <  %{doctrine_common_max_ver}
# composer.json (optional)
Requires:      php-composer(symfony/console) >= %{symfony_console_min_ver}
Requires:      php-composer(symfony/console) <  %{symfony_console_max_ver}
# phpcompatinfo (computed from version 2.5.12)
Requires:      php-date
Requires:      php-json
Requires:      php-pcre
Requires:      php-pdo
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# PEAR
Provides:      php-pear(pear.doctrine-project.org/DoctrineDBAL) = %{version}
# Rename
Obsoletes:     php-doctrine-DoctrineDBAL < %{version}
Provides:      php-doctrine-DoctrineDBAL = %{version}

%description
The Doctrine database abstraction & access layer (DBAL) offers a lightweight
and thin runtime layer around a PDO-like API and a lot of additional, horizontal
features like database schema introspection and manipulation through an OO API.

The fact that the Doctrine DBAL abstracts the concrete PDO API away through the
use of interfaces that closely resemble the existing PDO API makes it possible
to implement custom drivers that may use existing native or self-made APIs. For
example, the DBAL ships with a driver for Oracle databases that uses the oci8
extension under the hood.

Autoloader: %{phpdir}/Doctrine/DBAL/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Patch bin script
%patch0 -p1

if %{_bindir}/phpunit --atleast-version 5.4; then
%patch1 -p0
fi

: Remove empty file
rm -f lib/Doctrine/DBAL/README.markdown


%build
: Create autoloader
cat <<'AUTOLOAD' | tee lib/Doctrine/DBAL/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Doctrine\\DBAL\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Doctrine/Common/autoload.php',
));

\Fedora\Autoloader\Dependencies::optional(array(
    array(
        '%{phpdir}/Symfony3/Component/Console/autoload.php',
        '%{phpdir}/Symfony/Component/Console/autoload.php',
    ),
));
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{phpdir}
cp -rp lib/Doctrine %{buildroot}/%{phpdir}/

mkdir -p %{buildroot}/%{_bindir}
install -pm 0755 bin/doctrine-dbal.php %{buildroot}/%{_bindir}/doctrine-dbal


%check
%if %{with_tests}
# Rewrite "tests/Doctrine/Tests/TestInit.php" (aka PHPUnit bootstrap)
mv tests/Doctrine/Tests/TestInit.php tests/Doctrine/Tests/TestInit.php.dist
cat > tests/Doctrine/Tests/TestInit.php <<'BOOTSTRAP'
<?php
require_once '%{buildroot}/%{phpdir}/Doctrine/DBAL/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4(
    'Doctrine\\Tests\\',
    dirname(dirname(dirname(__DIR__))).'/tests/Doctrine/Tests'
);
BOOTSTRAP

: Upstream tests
RETURN_CODE=0
for PHP_EXEC in php %{?rhel:php54 php55} php56 php70 php71; do
    if which $PHP_EXEC; then
        $PHP_EXEC %{_bindir}/phpunit --verbose || RETURN_CODE=1
    fi
done
exit $RETURN_CODE
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/Doctrine/DBAL
%{_bindir}/doctrine-dbal


%changelog
* Sat Mar 11 2017 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.5.12-1
- Updated to 2.5.12 (RHBZ #1412852)
- Switch autoloader to php-composer(fedora/autoloader)
- Run upstream tests with SCLs if available

* Wed Feb  8 2017 Remi Collet <remi@remirepo.net> - 2.5.12-1
- update to 2.5.12

* Mon Feb  6 2017 Remi Collet <remi@remirepo.net> - 2.5.11-1
- update to 2.5.11

* Tue Jan 24 2017 Remi Collet <remi@remirepo.net> - 2.5.10-1
- update to 2.5.10

* Fri Jan 20 2017 Remi Collet <remi@remirepo.net> - 2.5.9-1
- update to 2.5.9

* Mon Sep 26 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.5.5-1
- Updated to 2.5.5 (RHBZ #1374891)

* Mon Jun 13 2016 Remi Collet <remi@fedoraproject.org> - 2.5.4-2
- add workaround for test suite with PHPUnit 5.4

* Mon Mar 14 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.5.4-1
- Updated to 2.5.4 (RHBZ #1153987)
- Added autoloader

* Wed Jan 14 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.5.1-1
- Updated to 2.5.1 (BZ #1153987)

* Fri Jan 02 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.5.1-0.2.20150101git185b886
- Updated to latest snapshot
- Fixed bin script
- Added tests

* Thu Jul 31 2014 Remi Collet <rpms@famillecollet.com> 2.4.2-6
- backport for remi repo
- fix license handling

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 2.4.2-6
- really apply the patch

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 2.4.2-5
- backport another OwnCloud-related pgsql fix from upstream master

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.2-4
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Updated Doctrine dependencies to use php-composer virtual provides

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 2.4.2-2
- backport for remi repo

* Tue Jan 07 2014 Adam Williamson <awilliam@redhat.com> - 2.4.2-2
- primary_index: one OwnCloud patch still isn't in upstream

* Sat Jan 04 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.2-1
- Updated to 2.4.2
- Conditional %%{?dist}

* Tue Dec 31 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.1-2.20131231gitd08b11c
- Updated to latest snapshot
- Removed patches (pulled into latest snapshot)

* Sun Dec 29 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.1-1
- Initial package
