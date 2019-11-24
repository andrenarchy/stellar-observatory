"""setup"""
import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="stellar-observatory",
    version="1.0a9",
    author="André Gaul",
    author_email="andre@gaul.io",
    description="Python package for analyzing the Stellar network",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/andrenarchy/stellar-observatory",
    packages=setuptools.find_packages(),
    python_requires="~=3.5",
    install_requires=[
        "numpy~=1.0",
        "requests~=2.0",
        "scipy~=1.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research"
    ],
)
