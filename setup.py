from setuptools import find_packages, setup


setup(
    name='battery',
    version='0.0.1',
    author='Marco Rougeth',
    author_email='marco@rougeth.com',
    packages=find_packages(),
    package_data={
        'battery': ['conf/project_template/*-tpl'],
    },
    entry_points={
        'console_scripts': ['battery=battery.cli:cli'],
    },
    install_requires=[
        'aiohttp',
        'requests',
        'click',
    ],
)
