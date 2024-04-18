#!/usr/bin/env bash
pyinstaller --onefile clearsaves.py
mv dist/clearsaves ~/.bin/clearsaves
rm -r build
rm -r dist
rm clearsaves.spec
