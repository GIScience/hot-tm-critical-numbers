from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("readme.md", 'r') as f:
    long_description = f.read()

setup(
    name='critical_numbers',
    version='0.1',
    description='A GIScience Heidelberg project for the HOT Tasking Manager',
    long_description=long_description,
    author='GIScience Heidelberg',
    author_email='schaub@stud.uni-heidelberg.de',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        cli=cli:cli
        ''',
    keywords=['HOT', 'GIScience',],
    classifiers=[
        'Development Status :: Alpha',
        'Natural Language :: English',
    ],
)
