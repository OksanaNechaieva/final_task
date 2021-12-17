from setuptools import setup, find_packages

setup(
    name='rss_reader_package',
    version='3.0',
    packages=find_packages(include=['run_rss_reader', 'rss_reader']),
    install_requires=[
        'feedparser',
        'xmltodict',
        'requests',
        'setuptools'],
    entry_points={
        'console_scripts': ['rss_reader=run_rss_reader:result']
    }
)

