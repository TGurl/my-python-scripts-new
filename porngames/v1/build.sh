#!/usr/bin/env bash

[ -d dist ] && rm -r dist
[ -d build ] && rm -r build
[ -f porngames.spec ] && rm porngames.spec

pyinstaller --onefile porngames.py
mv dist/porngames ~/.bin/

rm -r dist
rm -r build
rm porngames.spec
