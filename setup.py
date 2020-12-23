from setuptools import setup

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
    }
)
