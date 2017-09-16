from setuptools import find_packages, setup


setup(
    name='bottery',
    version='0.0.1-alpha.1',
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
)
