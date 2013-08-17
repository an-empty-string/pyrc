#!/bin/bash
cd $(dirname $0)
sphinx-apidoc-python3.3 -H PyRC -f -o doc .
sphinx-build-python3.3 -E -b html doc gh-pages
