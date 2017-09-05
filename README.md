# json-pointer [![Build Status](https://travis-ci.org/ermel272/json-pointer.svg?branch=master)](https://travis-ci.org/ermel272/json-pointer) [![Coverage Status](https://coveralls.io/repos/github/ermel272/json-pointer/badge.svg?branch=master)](https://coveralls.io/github/ermel272/json-pointer?branch=master)

A Python 2.7 implementation of [IETF RFC 6901](https://tools.ietf.org/html/rfc6901).

Please click [here](https://ermel272.github.io/json-pointer-docs/) to go to the docs.

# Contributing
### Getting the code

Fork the repository, then:

```
git clone https://github.com/<username>/json-pointer.git
cd json-pointer
make install-full
```

The install-full make directive installs all module, test, and development external dependencies.
From there, simply open a PR against master (please add unit tests where applicable) and note that test coverage
must meet a certain percentage threshold, otherwise the unit test build will fail.