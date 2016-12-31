%define _disable_lto 1
%define _disable_ld_no_undefined 1

%define major 0
%define libname %mklibname %name %major
%define grlibname %mklibname %{name}_groebner %major
%define devname %mklibname -d %name

Name:		brial
Version:	0.8.5
Release:	1
Summary:	Framework for Boolean Rings
Group:		Sciences/Mathematics
# The entire source code is GPLv2+ except the Cudd directory that is BSD
License:	GPLv2+ and BSD
URL:		https://github.com/BRiAl/BRiAl/
Source0:	https://github.com/BRiAl/BRiAl/releases/download/%{version}/%{name}-%{version}.tar.bz2
# brial-0.8.5/Cudd/cudd/cudd.h:#define CUDD_VERSION "2.5.0"
Provides:	bundled(cudd) = 2.5.0
BuildRequires:	boost-devel
BuildRequires:	gd-devel
BuildRequires:	python2-devel
BuildRequires:	python2-setuptools
BuildRequires:	m4ri-devel
Obsoletes:	polybori <= %{version}-1
Provides:	polybori = %{version}-%{release}

# FIXME This full block, as well as other Provides/Obsoletes
# can be removed once f25 reaches EOL
# Obsolete unsupported/unused packages that may be left after an
# update from previous sagemath package versions.
# NOTE that the Provides is just to remove polybori, as besides
# the -static not generated on purpose, the others do not yet
# have a real provides from upstream, as noted at
# https://github.com/BRiAl/BRiAl/issues/6
Obsoletes:	polybori-gui <= %{version}-1
Provides:	polybori-gui <= %{version}-1
Obsoletes:	polybori-docs <= %{version}-1
Provides:	polybori-docs <= %{version}-1
Obsoletes:	polybori-static <= %{version}-1
Provides:	polybori-static <= %{version}-1
Obsoletes:	polybori-ipbori <= %{version}-1
Provides:	polybori-ipbori <= %{version}-1
# END FIXME

%description
The core of BRiAl is a C++ library, which provides high-level data
types for Boolean polynomials and monomials, exponent vectors, as well
as for the underlying polynomial rings and subsets of the powerset of
the Boolean variables. As a unique approach, binary decision diagrams
are used as internal storage type for polynomial structures. On top of
this C++-library we provide a Python interface. This allows parsing of
complex polynomial systems, as well as sophisticated and extendable
strategies for Gröbner base computation. BRiAL features a powerful
reference implementation for Gröbner basis computation.

%package -n	%devname
Summary:	Development files for %{name}
Requires:	%libname = %{version}-%{release}
Requires:	%grlibname = %{version}-%{release}
Requires:	boost-devel%{?_isa}
Obsoletes:	polybori-devel <= %{version}-1
Provides:	polybori-devel = %{version}-%{release}
Provides:	brial-devel = %{version}-%{release}

%description -n %devname
Development headers and libraries for %{name}.

%package	-n python2-%{name}
Summary:	Python interface to %{name}
Obsoletes:	python-polybori <= %{version}-1
Provides:	python-polybori = %{version}-%{release}
Requires:       %libname = %{version}-%{release}
Requires:       %grlibname = %{version}-%{release}

%description	-n python2-%{name}
Python interface to %{name}.

%libpackage %name %{major}
%libpackage %{name}_groebner %{major}

%prep
%setup -q

%build
export CXXFLAGS="%{optflags} -std=c++98"
export CC=gcc
export CXX=g++
export PYTHON=%__python2
%configure --enable-shared --disable-static
# Get rid of undesirable hardcoded rpaths, and workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/*.la

%files -n %devname
%doc ChangeLog README LICENSE
%{_includedir}/polybori.h
%{_includedir}/polybori/
%{_libdir}/lib%{name}*.so

%files -n python2-%{name}
%{python2_sitelib}/%{name}/

%changelog
* Thu Aug 18 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> 0.8.5-4
- Add Provides/Obsoletes to remaining polybori packages (#1367526#c6)

* Wed Aug 17 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> 0.8.5-3
- Correct summary to talk about BRiAl and not PolyBori (#1367526#c4)

* Tue Aug 16 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> 0.8.5-2
- Correct setting of CXXFLAGS (#1367526#c2)
- Add proper multiple license information (#1367526#c2)
- Add Provides/Obsoletes to devel package (#1367526#c2)
- Remove unused shared library dependencies (#1367526#c2)
- Add version information to bundled Cudd (#1367526#c2)
- Change to a more informational summary (#1367526#c2)

* Wed Aug 10 2016 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> 0.8.5-1
- Initial brial spec file
