from distutils.core import setup


setup(
    name='cREST',
    version='0.1.0',
    packages=['crest'],
    license='LICENSE.txt',
    long_description=open('README').read(),
    install_requires=[
        'requests==2.18.4',
        'jsonschema==2.6.0'
    ],
)
