#!/usr/bin/env python3

from distutils.core import setup

setup(name='join_to_python',
      version='2022.06.10',
      description='JOIN to Python: Implementation of LINQ to Objects in Python',
      author='Hachiko (8ko)',
      long_description='README.md',
      long_description_content_type="text/markdown",
      author_email='spam@me.not',
      url='https://www.github.com/hachiko-8ko/join-to-python/',
      license='LGPL',
      packages=[
            'join_to_python',
            'join_to_python.EnumerableType',
            'join_to_python.Generators',
            'join_to_python.Types'
            ],
      include_package_data=True,
      classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: LGPL License',
            'Operating System :: OS Independent'
          ]
     )

