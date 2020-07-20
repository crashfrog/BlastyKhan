#!/usr/bin/env python3.7

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = ['flask>=1.1.2', 'Click>=7.1.2', 'biopython>=1.76']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Justin Payne",
    author_email='crashfrog@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="BLAST as a web service",
    entry_points={
        'console_scripts': [
            'bkhan=blastykhan.cli:cli',
        ]
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='blastykhan',
    name='blastykhan',
    packages=find_packages(include=['blastykhan', 'blastykhan.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/crashfrog/blastykhan',
    version='0.1.0',
    zip_safe=False,
)
