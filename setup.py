from setuptools import setup, find_packages

setup(
    name='tidytable',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
        'inflection'
    ],
    entry_points='''
        [console_scripts]
        tidytable=tidytable.cli:cli
    ''',
)
