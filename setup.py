from setuptools import setup

setup(
    name = 'TidyTable',
    version = '0.1.0',
    py_modules = ['tt'],
    install_requires = [
        'Click',
        'pandas'
    ],
    entry_points = '''
        [console_scripts]
        tt=tt:cli
    ''',
)