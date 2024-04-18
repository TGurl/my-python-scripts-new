#!/usr/bin/env bash
pyinstaller --onefile porngames.py
mv dist/porngames ~/.bin/porngames
rm -r build
rm -r dist
rm porngames.spec
