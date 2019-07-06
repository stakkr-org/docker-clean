import os
from setuptools import setup


extra_packages = []
if os.name == 'nt':
    extra_packages.append('pypiwin32')

__version__ = '0.9.9'

# Get the long description from the README file
def readme():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read()

setup(
    name='docker-clean',
    version=__version__,
    description='A command to clean docker images, containers, networks and volumes.',
    long_description=readme(),
    url='http://github.com/stakkr-org/docker-clean',
    author='Emmanuel Dyan',
    author_email='emmanueldyan@gmail.com',
    license='Apache 2.0',
    py_modules=['docker-clean'],
    entry_points='''[console_scripts]
docker-clean=stakkr.docker_clean:main''',
    include_package_data=True,
    install_requires=[
        'click>=7',
        'clint==0.5.1',
        # Docker compose includes requests and docker
        'docker>3.7',
        'humanfriendly==4.18'
        ] + extra_packages,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration',
    ],
    keywords='docker,python',
)
