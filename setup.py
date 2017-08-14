from setuptools import setup


setup(
    name='batteries',
    entry_points={
        'console_scripts': ['batteries=batteries.cli:cli'],
    }
)
