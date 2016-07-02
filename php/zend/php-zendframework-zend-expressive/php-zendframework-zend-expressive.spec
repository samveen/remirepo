# remirepo/Fedora spec file for php-zendframework-zend-expressive
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    4e6b1821e116425c76a515cae9b78141f17b2e1a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-expressive
%global php_home     %{_datadir}/php
%global library      Expressive
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0.0
Release:        2%{?dist}
Summary:        PSR-7 Middleware Microframework based on Stratigility

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-composer(container-interop/container-interop)    >= 1.0
BuildRequires:  php-composer(psr/http-message)                       >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-diactoros)             >= 1.1
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-router)     >= 1.1
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-template)   >= 1.0.1
BuildRequires:  php-composer(%{gh_owner}/zend-stratigility)          >= 1.1
BuildRequires:  php-reflection
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "filp/whoops": "^1.1",
#        "phpunit/phpunit": "^4.7",
#        "squizlabs/php_codesniffer": "^2.3",
#        "zendframework/zend-expressive-aurarouter": "^1.0",
#        "zendframework/zend-expressive-fastroute": "^1.0",
#        "zendframework/zend-expressive-zendrouter": "^1.0",
#        "zendframework/zend-servicemanager": "^2.6"
BuildRequires:  php-composer(phpunit/phpunit)                        >= 4.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)                >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-aurarouter) >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-fastroute)  >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-expressive-zendrouter) >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)        >= 2.6
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                        >= 2.5.1-4
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "container-interop/container-interop": "^1.1",
#        "psr/http-message": "^1.0",
#        "zendframework/zend-diactoros": "^1.1",
#        "zendframework/zend-expressive-router": "^1.1",
#        "zendframework/zend-expressive-template": "^1.0.1",
#        "zendframework/zend-stratigility": "^1.1"
Requires:       php(language) >= 5.5
Requires:       php-composer(container-interop/container-interop)    >= 1.0
Requires:       php-composer(container-interop/container-interop)    <  2
Requires:       php-composer(psr/http-message)                       >= 1.0
Requires:       php-composer(psr/http-message)                       <  2
Requires:       php-composer(%{gh_owner}/zend-diactoros)             >= 1.1
Requires:       php-composer(%{gh_owner}/zend-diactoros)             <  2
Requires:       php-composer(%{gh_owner}/zend-expressive-router)     >= 1.1
Requires:       php-composer(%{gh_owner}/zend-expressive-router)     <  2
Requires:       php-composer(%{gh_owner}/zend-expressive-template)   >= 1.0.1
Requires:       php-composer(%{gh_owner}/zend-expressive-template)   <  2
Requires:       php-composer(%{gh_owner}/zend-stratigility)          >= 1.1
Requires:       php-composer(%{gh_owner}/zend-stratigility)          <  2
# From phpcompatinfo report for version 1.2.0
Requires:       php-reflection
Requires:       php-spl
%if ! %{bootstrap}
# From composer, "suggest": {
#        "filp/whoops": "^1.1 to use the Whoops error handler",
#        "zendframework/zend-expressive-helpers": "^1.0 for its UrlHelper, ServerUrlHelper, and BodyParseMiddleware",
#        "zendframework/zend-expressive-aurarouter": "^1.0 to use the Aura.Router routing adapter",
#        "zendframework/zend-expressive-fastroute": "^1.0 to use the FastRoute routing adapter",
#        "zendframework/zend-expressive-zendrouter": "^1.0 to use the zend-mvc routing adapter",
#        "zendframework/zend-expressive-platesrenderer": "^1.0 to use the Plates template renderer",
#        "zendframework/zend-expressive-twigrenderer": "^1.0 to use the Twig template renderer",
#        "zendframework/zend-expressive-zendviewrenderer": "^1.0 to use the zend-view PhpRenderer template renderer",
#        "aura/di": "3.0.*@beta to make use of Aura.Di dependency injection container",
#        "xtreamwayz/pimple-container-interop": "^1.0 to use Pimple for dependency injection",
#        "zendframework/zend-servicemanager": "^2.5 to use zend-servicemanager for dependency injection"
%if 0%{?fedora} >= 21
#Suggests:       php-composer(filp/whoops)
Suggests:       php-composer(%{gh_owner}/zend-expressive-helpers)
Suggests:       php-composer(%{gh_owner}/zend-expressive-aurarouter)
Suggests:       php-composer(%{gh_owner}/zend-expressive-fastroute)
Suggests:       php-composer(%{gh_owner}/zend-expressive-zendrouter)
Suggests:       php-composer(%{gh_owner}/zend-expressive-platesrenderer)
Suggests:       php-composer(%{gh_owner}/zend-expressive-twigrenderer)
Suggests:       php-composer(%{gh_owner}/zend-expressive-zendviewrenderer)
Suggests:       php-composer(aura/di)
#Suggests:       php-composer(xtreamwayz/pimple-container-interop)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
%endif
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-zendframework-zend-loader                   >= 2.5.1-4
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
zend-expressive builds on zend-stratigility to provide a minimalist PSR-7
middleware framework for PHP, with the following features:
* Routing. Choose your own router; we support:
  - Aura.Router
  - FastRoute
  - ZF2's MVC router
* DI Containers, via container-interop. Middleware matched via routing is
  retrieved from the composed container.
* Optionally, templating. We support:
  -  Plates
  -  Twig
  -  ZF2's PhpRenderer

Documentation: http://zend-expressive.readthedocs.io/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE

: Create dependency autoloader
cat << 'EOF' | tee autoload.php
<?php
if (file_exists('%{php_home}/Aura/Di/autoload.php')) {
   require_once '%{php_home}/Aura/Di/autoload.php';
}
EOF


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}

install -m644 autoload.php %{buildroot}%{php_home}/Zend/%{library}-autoload.php


%check
%if %{with_tests}
: drop tests using optional filp/whoops
rm test/Whoops*
rm test/Container/Whoops*

mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
define('RPM_BUILDROOT', '%{buildroot}%{php_home}/Zend');

require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --include-path=%{buildroot}%{php_home} --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{php_home}/Zend/%{library}/*
%{php_home}/Zend/%{library}-autoload.php


%changelog
* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- clean autoloader, rely on zend-loader >= 2.5.1-4

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

