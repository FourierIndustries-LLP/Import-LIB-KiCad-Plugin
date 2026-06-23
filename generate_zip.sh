#!/bin/bash

rm Import-LIB-KiCad-Plugin.zip
mv metadata.json metadata_.json
jq --arg today "$(date +%Y.%m.%d)" '.versions[0].version |= $today' metadata_.json > metadata.json

git ls-files  -- 'metadata.json' 'resources*.png' 'plugins*.png' 'plugins*.py' | xargs zip Import-LIB-KiCad-Plugin.zip
mv metadata_.json metadata.json

# add easyeda2kicad.py/easyeda2kicad to plugins
# Pinned to a specific release tag: the plugin's impart_easyeda.py wrapper is
# written against this version's API. Bumping it may introduce breaking changes
# in the wrapper, so update both together.
git clone --depth 1 --branch v1.0.1 https://github.com/uPesy/easyeda2kicad.py
cp -r easyeda2kicad.py/easyeda2kicad plugins/.
zip -r Import-LIB-KiCad-Plugin.zip plugins/easyeda2kicad
rm -rf easyeda2kicad.py
rm -rf plugins/easyeda2kicad