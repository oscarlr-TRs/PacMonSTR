from setuptools import setup
from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name='PacMonSTR',
    version='1.1',
    packages=['PacMonSTR'],
    url='oscarlr.github.io',
    license='',
    author='Oscar Rodriguez',
    author_email='oscar.rodriguez@icahn.mssm.edu',
    description='',
    entry_points = {
        'console_scripts': ['pacmonstr = PacMonSTR.main:main',
                            'str = PacMonSTR.main:main']
    },
    ext_modules = cythonize("PacMonSTR/dpFuncs_sw2.pyx"),
    include_dirs=[numpy.get_include()]
)
