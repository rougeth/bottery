from setuptools import find_packages, setup

setup(
    name='bottery',
    version='0.0.1a2',
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
        'jinja2',
        'requests',
    ],
    extras_require={
        'dev': [
            'coverage',
            'flake8',
            'isort',
            'pytest',
            'sphinx',
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
