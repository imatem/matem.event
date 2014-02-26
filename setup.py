# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '1.0'

setup(
    name='matem.event',
    version=version,
    description="Event type for the Institute of Mathematics",
    long_description=open('README.txt').read() + '\n' +
    open('docs/CHANGES.txt').read(),
    # Get more strings from
    #http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    platforms='Any',
    author='Gildardo Bautista',
    author_email='gil@matem.unam.mx',
    url='http://www.matem.unam.mx',
    license='GPL',
    namespace_packages=['matem'],
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.dexterity',
    ],
    extras_require={
        'develop': [
            'flake8',
            'jarn.mkrelease',
            'manuel',
            'Sphinx',
            'zest.releaser',
        ],
        'test': [
            'plone.app.testing',
            'unittest2',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
