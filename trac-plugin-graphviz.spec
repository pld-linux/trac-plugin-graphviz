%define		trac_ver	0.12
%define		plugin		graphviz
Summary:	Graphviz Plugin for Trac
Name:		trac-plugin-%{plugin}
Version:	0.7.5
Release:	1
License:	BSD-like
Group:		Applications/WWW
Source0:	http://trac-hacks.org/changeset/latest/graphvizplugin/0.11-%{version}?old_path=/&format=zip#/%{plugin}-%{version}.zip
# Source0-md5:	5ffbcb4743c85c0a34eff98918c814b6
URL:		http://trac-hacks.org/wiki/GraphvizPlugin
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	unzip
Requires:	graphviz
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The graphviz wiki processor is a plugin for Trac that allows the the
dynamic generation of diagrams by the various graphviz programs. The
text of a wiki page can contain the source text for graphviz and the
web browser will show the resulting image.

%prep
%setup -qc
mv %{plugin}plugin/0.11-%{version}/* .

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
trac-enableplugin "graphviz.*"

%files
%defattr(644,root,root,755)
%doc COPYING README.txt ReleaseNotes.txt
%{py_sitescriptdir}/%{plugin}
%{py_sitescriptdir}/*-*.egg-info
%{_examplesdir}/%{name}-%{version}
