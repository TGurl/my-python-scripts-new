#!/usr/bin/env bash

pyinstaller --onefile fetch.py

mv dist/fetch ~/.bin

rm -r build
rm -r dist
rm -r fetch.spec
