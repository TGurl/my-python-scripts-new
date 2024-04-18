#!/usr/bin/env bash
pyinstaller --onefile mdb.py
mv dist/mdb ~/.bin/mdb
rm -r build
rm -r dist
rm mdb.spec
