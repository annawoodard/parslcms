from setuptools import setup

from parslcms import VERSION

setup(
    name='parslcms',
    version=VERSION,
    url='https://github.com/annawoodard/parsl.cms',
    author='The Parsl Team',
    author_email='annawoodard@uchicago.edu',
    license='Apache 2.0',
    download_url='https://github.com/annawoodard/cms-parsl/archive/{}.tar.gz'.format(VERSION),
    package_data={
        '': ['LICENSE'],
        'parslcms': [
            'data/vc3-builder',
            'data/parsl.json',
            'data/wrapper.sh'
        ]
    },
    packages=[
        'parslcms',
        'parslcms.data',
        'parslcms.configs'
    ],
    install_requires=[
        'parsl'
    ],
    keywords=['Workflows', 'Scientific computing', 'High Energy Physics', 'Compact Muon Solenoid'],
)
