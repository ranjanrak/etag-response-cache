from setuptools import setup


README = open("README.md").read()

setup(
    name="etag_cache",  
    version="0.2",
    author="Rakesh R",
    author_email="rrrakesh265@gmail.com",
    description="Python package for caching HTTP response based on etag",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ranjanrak/etag-response-cache",
    packages=['etag_cache'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries"
    ],
)