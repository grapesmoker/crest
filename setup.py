from setuptools import setup


setup(
    name='cREST',
    version='0.1.4',
    packages=['crest', 'crest.tests'],
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    install_requires=[
        'requests==2.18.4',
        'jsonschema==2.6.0',
        'simplejson==3.13.2'
    ],
    author='Jerry Vinokurov',
    author_email='grapesmoker@gmail.com'
)
