import os
from setuptools import setup, find_packages

def fread(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = '0.1'

setup(
    name='django-password',
    version=version,
    description="A Django application to store communal passwords.",
    long_description=fread("README")+"\n\n"+fread('Changelog')+"\n\n"+fread('TODO'),
    classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Topic :: System :: Software Distribution",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='django password',
    author='George Hickman',
    author_email='george@ghickman.co.uk',
    maintainer='George Hickman',
    maintainer_email='george@ghickman.co.uk',
    url='http://github.com/ghickman/django-password',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django',
        'south'
    ],
)
