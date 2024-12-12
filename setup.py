#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module sets up the package for the lib_work_login"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ivonet",
    author="Ivo Woltring",
    author_email="ivonet@gmail.com",
    maintainer="Ivo Woltring",
    maintainer_email="ivonet@gmail.com",
    version="0.0.1",
    url="https://github.com/ivonet/GIT_REPO_HERE.git",
    download_url='https://github.com/ivonet/GIT_REPO_HERE.git',
    keywords=['KEYWORDS_HERE'],
    license="Apache 2.0",
    description="DESCRIPTION_HERE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/ivonet/PROJECT_HERE/issues",
    },
    python_requires=">=3.12",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PIP_DEPENDENCY_HERE==VERSION_HERE',
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': [
        ]},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
