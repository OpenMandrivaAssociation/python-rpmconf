%bcond_with tests

Name:		python-rpmconf
Summary:	Tool to handle rpmnew and rpmsave files
License:	GPLv3
Version:	1.1.4
Release:	2
URL:		http://wiki.github.com/xsuchy/rpmconf
# source is created by:
# git clone https://github.com/xsuchy/rpmconf.git
# cd rpmconf; tito build --tgz
Source0:	https://github.com/xsuchy/rpmconf/archive/rpmconf-%{version}-1/rpmconf-rpmconf-%{version}-1.tar.gz
Patch0:		fix-sphinx-build-binary-naming.patch
Patch1:		fix-path-to-ls.patch
BuildArch:	noarch
BuildRequires:	docbook-utils
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	python-sphinx
BuildRequires:	pkgconfig(python)
Requires:	%{name}-base
Requires:	python-rpm
BuildRequires:	python-rpm
%if %{with tests}
BuildRequires:	python-pylint
BuildRequires:	python-six
%endif
# mergetools
Suggests:	diffuse
Suggests:	kdiff3
Suggests:	meld
Suggests:	vim-X11
Suggests:	vim-enhanced
# sdiff
Suggests:	diffutils

%description
This tool search for .rpmnew, .rpmsave and .rpmorig files and ask you what to do
with them:
Keep current version, place back old version, watch the diff or merge.

%package doc
Summary:	Documentation of python interface for %{name}
BuildArch:	noarch

%description doc
Documentation generated from code of python3-rpmconf.

%package base
Summary:	Filesystem for %{name}
BuildArch:	noarch

%description base
Directory hierarchy for installation scripts, which are handled by rpmconf.

%prep
%autosetup -p1 -n rpmconf-rpmconf-%{version}-1

%build
%py_build

docbook2man rpmconf.sgml
make -C docs html man

%install
%py_install -- --install-scripts %{_sbindir}

install -D -m 644 rpmconf.8 %{buildroot}%{_mandir}/man8/rpmconf.8
install -D -m 644 docs/build/man/rpmconf.3 %{buildroot}%{_mandir}/man3/rpmconf.3
mkdir -p %{buildroot}%{_datadir}/rpmconf/

%check
%if %{with tests}
pylint-3.6 rpmconf bin/rpmconf || :
%endif

%files
%license LICENSE
%{_sbindir}/rpmconf
%dir %{python3_sitelib}/rpmconf
%{python_sitelib}/rpmconf/*
%{python_sitelib}/rpmconf-*.egg-info

%files doc
%doc README.md LICENSE
%doc docs/build/html/
%doc %{_mandir}/man3/rpmconf.3*
%doc %{_mandir}/man8/rpmconf.8*

%files base
%dir %{_datadir}/rpmconf
