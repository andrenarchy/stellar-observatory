import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stellar-observatory",
    version="1.0a1",
    author="André Gaul",
    author_email="andre@gaul.io",
    description="Python package for analyzing the Stellar network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrenarchy/stellar-observatory",
    packages=setuptools.find_packages(),
    python_requires="~=3.3",
    install_requires=[
      "requests~=2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research"
    ],
)
