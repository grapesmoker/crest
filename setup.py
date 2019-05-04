from setuptools import setup


setup(
    name='cREST',
    version='0.1.5',
    packages=['crest', 'crest.tests'],
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    install_requires=[
        'requests==2.20.0',
        'marshmallow==3.0.0rc5'
    ],
    author='Jerry Vinokurov',
    author_email='grapesmoker@gmail.com'
)
