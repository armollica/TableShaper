from setuptools import setup, find_packages

setup(
    name='tableshaper',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
        'fiona==1.7.11',
        'geopandas',
        'inflection'
    ],
    entry_points='''
        [console_scripts]
        ts=tableshaper.cli:cli
    ''',
)
