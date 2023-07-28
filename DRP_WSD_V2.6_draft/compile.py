"""
    Cythonize the python files to protect the source codes.

    python compile.py build_ext --inplace

"""
import glob
import os

from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize


if __name__ == '__main__':

    packages = ['utils', 'conf', 'screens', 'widgets']

    setup(
        name="Wireless Scale Display",
        ext_modules=cythonize(
            [
                Extension("wsd", ['wsd.py']),
                Extension("settings", ['settings.py']),
                Extension("utils.*", ['utils/*.py']),
                Extension("conf.*", ['conf/*.py']),
                Extension("screens.*", ['screens/*.py']),
                Extension("widgets.*", ['widgets/*.py']),

            ],
            build_dir="build",
            compiler_directives=dict(
                always_allow_keywords=True,
            )
        ),
        cmdclass=dict(
            build_ext=build_ext
        ),
        packages=packages
    )

    print('===== Deleting source files =====')
    os.remove('settings.py')
    os.remove('wsd.py')
    for package in packages:
        for path in glob.glob('{}/*.py'.format(package)):
            if '__init__.py' not in path:
                os.remove(path)
        os.system('mv display/{}/*.so {}/'.format(package, package))
    os.system('rm -r display')
    os.system('rm -r ../node')
    os.system('rm -r ../doc')

    print('Finished!')
