from setuptools import setup, find_packages

setup(
    name='tableshaper',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
        'fiona',
        'geopandas',
        'inflection',
        'tabulate'
    ],
    entry_points={
        'console_scripts': ['tableshaper=tableshaper.cli:cli']
    },
)
