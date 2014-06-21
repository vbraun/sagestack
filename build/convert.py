#!/usr/bin/env python
"""
Tools for upgrading Sage spkgs to hashdist
"""

import os
import re
from textutil import dedent


PACKAGE_YAML_TEMPLATE = """
sage:   # for the Sage UI only
  name: {name}
  category: {category}

extends:
- spkg_install
{copy_patches}


sources:
- url: {url}
  key: tar.gz:aducy6ybplnbwvkakckpxvked4yc6zc3

build_stages:

{extra_build_stages}

""".strip('\n')


EXTRA_BUILD_STAGES = {
    'bzip2': dedent("""
        - name: copy_patches
          after: prologue
          before: run_spkg_install
          handler: bash
          files: [patches/autotools/*]
          bash: |
            # copy_patches_autotools
            ln -s _hashdist/patches patches
    """),
}



DEPENDENCIES = {
    'conway_polynomials': [],
    'sqlite': ['readline', ],
    'bzip2': ['pkgconf'],
    'patch': ['bzip2'],
    'atlas': ['python'],
    'boehm_gc': ['pkgconf'],
    'boost_cropped': [],
    'cliquer': [],
    'ncurses': ['pkgconf'],
    'readline': ['ncurses'],
    'iconv': [],
    'docutils': ['python'],
    'elliptic_curves': ['python', 'sqlite'],
    'conway': ['sage_python_library', 'sage_noarch', 'sagenb', 'ipython'],
    'graphs': [],
    'glpk': ['mpir', 'zlib'],
    'python': ['zlib', 'bzip2', 'pkgconf', 'readline', 'sqlite', 'libpng'],
    'mpir': ['iconv'],
    'gsl': ['atlas'],
    'gf2x': [],
    'ntl': ['mpir', 'gf2x'],
    'libfplll': ['mpir', 'mpfr'],
    'pari': ['readline', 'mpir', 'pari_galdata', 'pari_seadata_small'],
    'pari_galdata': [],
    'pari_seadata_small': [],
    'polybori': ['python', 'ipython', 'scons', 'boost_cropped', 'libm4ri', 'gd'],
    'polytopes_db': [],
    'ppl': ['mpir', 'glpk'],
    'mpc': ['mpir', 'mpfr'],
    'mpfr': ['mpir'],
    'mpfi': ['mpir', 'mpfr'],
    'givaro': ['mpir'],
    'git': ['zlib', 'python'],
    'fflas_ffpack': ['mpir', 'givaro', 'gsl', 'atlas'],
    'linbox': [
        'mpir', 'ntl', 'givaro',
        'mpfr', 'libfplll', 'iml',
        'libm4ri', 'libm4rie', 'fflas_ffpack'],
    'iml': ['mpir', 'gsl', 'atlas'],
    'genus2reduction': ['pari'],
    'palp': [],
    'lcalc': ['pari', 'mpfr'],
    'lrcalc': [],
    'pynac': ['python'],
    'sympow': [],
    'symmetrica': [],
    'gap': ['ncurses', 'readline', 'mpir'],
    'libgap': ['gap'],
    'ipython': ['python'],
    'pexpect': ['python'],
    'gd': ['libpng', 'freetype', 'iconv'],
    'gdmodule': ['python', 'gd', 'iconv'],
    'scons': ['python'],
    'rubiks': [],
    'sqlite': ['readline'],
    'sagetex': ['python',
                'maxima', 'scipy',
                'matplotlib', 'pillow', 'tachyon'],
    'setuptools': ['python'],
    'singular': ['mpir', 'ntl', 'readline', 'mpfr'],
    'pycrypto': ['python'],
    'networkx': ['python'],
    'mpmath': ['python'],
    'zlib': [],
    'jmol': ['sagenb'],
    'freetype': ['libpng'],
    'libpng': ['zlib'],
    'six': ['python'],
    'dateutil': ['python', 'six', 'setuptools'],
    'pyparsing': ['python'],
    'tornado': ['python'],
    'matplotlib': [
        'python', 'numpy',
        'freetype', 'libpng',
        'gdmodule', 'dateutil',
        'pkgconf', 'pyparsing',
        'setuptools'],
    'cddlib': ['mpir'],
    'gfan': ['mpir', 'cddlib'],
    'tachyon': ['libpng'],
    'ecm': ['mpir'],
    'ratpoints': ['mpir'],
    'ecl': ['mpir', 'readline', 'boehm_gc'],
    'maxima': ['ecl'],
    'r': ['atlas', 'iconv', 'readline', 'pkgconf'],
    'rpy2': ['python', 'r'],
    'sympy': ['python'],
    'cython': ['python'],
    'flintqs': ['mpir'],
    'flint': ['mpir', 'mpfr', 'ntl'],
    'eclib': ['pari', 'ntl', 'flint'],
    'libm4ri': ['libpng', 'pkgconf'],
    'libm4rie': ['libm4ri', 'givaro', 'ntl'],
    'zn_poly': ['mpir', 'python'],
    'sagenb': [
        'python', 'setuptools', 'pexpect',
        'jinja2', 'sphinx', 'docutils'],
    'sqlalchemy': ['python', 'setuptools'],
    'sphinx': [
        'python', 'setuptools', 'docutils',
        'jinja2', 'pygments'],
    'jinja2': ['python', 'setuptools', 'docutils'],
    'pygments': ['python', 'setuptools'],
    'gcc': ['mpir', 'mpfr', 'mpc', 'zlib'],
    'pillow': ['python', 'setuptools'],
    'pkgconf': [],
    'pkgconfig': ['python', 'setuptools'],
    'numpy': ['python', 'atlas', 'pkgconf'],
    'scipy': ['atlas', 'numpy'],
    'cvxopt': [
        'numpy',
        'atlas', 'cephes',
        'gsl', 'glpk', 'matplotlib'],
    'cephes': [],
}

'- copy_patches'




PKGS = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pkgs'))

def upgrade_all():
    """
    Upgrade all packages
    """
    for name in os.listdir(PKGS):
        fullname = os.path.join(PKGS, name)
        if not os.path.isdir(fullname):
            continue
        if not os.path.exists(os.path.join(fullname, 'package-version.txt')):
            continue
        print('upgrading ' + name)
        upgrade(name, fullname)


class OldPkg(object):

    def __init__(self, name, pkg_dir):
        self.name = name
        self.pkg_dir = pkg_dir

    @property
    def yaml_filename(self):
        return os.path.join(self.pkg_dir, self.name + '.yaml')

    def upgrade(self):
        """
        Upgrade a single package
        """
        package_yaml = self.package_yaml()

        print package_yaml
        return

        with open(self.yaml_filename, 'w') as yaml:
            yaml.write(package_yaml)

    def old_version(self):
        with open(os.path.join(self.pkg_dir, 'package-version.txt'), 'r') as f:
            version_patchlevel = f.read().strip()
        return re.sub(r'\.p[0-9]*', '', version_patchlevel)

    def old_tarball(self):
        with open(os.path.join(self.pkg_dir, 'checksums.ini'), 'r') as f:
            for line in f.readlines():
                if line.startswith('tarball='):
                    tarball = line[8:].strip()
                if line.startswith('sha1='):
                    sha1 = line[5:].strip()
        return tarball

    def url(self):
        return 'http://www.sagemath.org/packages/upstream/{name}/{tarball}'.format(
            name=self.name, tarball=self.tarball)
    
    def has_patches(self):
        return os.path.isdir(os.path.join(self.pkg_dir, 'patches'))

    def has_check(self):
        return os.path.exists(os.path.join(self.pkg_dir, 'spkg-check')):
    
    def package_yaml(self):
        """
        Package.yaml from old-style directory
        """
        if name in DEPENDENCIES:
            category = 'standard'
            dependencies = DEPENDENCIES[name]
        else:
            category = 'optional'
        result = PACKAGE_YAML_TEMPLATE.format(
            name=self.name,
            category=category,
            url=self.url,
            copy_patches='- copy_patches' if self.has_patches() else ''
        )
        result += '\n'
        return result
    
    

if __name__ == '__main__':
    update_all()
