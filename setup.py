import ast
import re
from setuptools import find_packages, setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('bottery/__init__.py', encoding='utf8') as f:
    # Search for `__version__` on bottery/__init__.py and get its values
    version = ast.literal_eval(_version_re.search(f.read()).group(1))


setup(
    name='bottery',
    description='A bot framework with batteries included',
    version=version,
    url='https://github.com/rougeth/bottery',
    license='MIT',
    author='Marco Rougeth',
    author_email='marco@rougeth.com',
    packages=find_packages(),
    package_data={
        'bottery': ['conf/project_template/*-tpl'],
    },
    entry_points={
        'console_scripts': ['bottery=bottery.cli:cli'],
    },
    install_requires=[
        'aiohttp',
        'click',
        'halo',
        'jinja2',
        'requests',
    ],
    extras_require={
        'dev': [
            'coverage',
            'flake8',
            'isort',
            'pytest',
            'pytest-asyncio',
            'pytest-cov',
            'pytest-mock',
            'sphinx',
            'testfixtures',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
