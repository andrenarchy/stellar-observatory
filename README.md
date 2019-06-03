# Stellar Observatory

[![Build Status](https://travis-ci.org/andrenarchy/stellar-observatory.svg?branch=master)](https://travis-ci.org/andrenarchy/stellar-observatory)

Stellar Observatory is a Python package for analyzing the Stellar network. It contains experimental and non-optimized code that is used for conduction research on quorums, quorum slices, and other aspects of the Stellar network.

This work is supported by a research grant in the [Stellar academic research program](https://www.stellar.org/stellar-academic-research-program/) of the [Stellar Development Foundation](https://www.stellar.org/).

## Installation

```
pip install stellar-observatory
```

Note: Stellar Observatory requires Python 3.5 or above.

## Example

See https://colab.research.google.com/drive/1-dOgu35CWWw4J-mQnhrmjnRFkLlEXDzL

## Maintainer docs

### Upload new version

```
rm dist/*
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
