import os

from setuptools import setup

# Using vbox, hard links do not work
if os.environ.get('USER','') == 'vagrant':
    del os.link

setup(
    name='lingo2',
    version='0.1',
    description='A simple CouchDB ORM for Python',
    long_description='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='orm python couchdb',
    url='https://github.com/BasementCat/lingo2',
    author='Alec Elton',
    author_email='alec.elton@gmail.com',
    license='MIT',
    packages=['lingo2'],
    install_requires=[
        'couchdb',
        'marshmallow',
        'requests',
        'purl',
        # 'pytz',
        # 'arrow',
    ],
    test_suite='nose2.collector.collector',
    tests_require=['nose2'],
    zip_safe=False
)