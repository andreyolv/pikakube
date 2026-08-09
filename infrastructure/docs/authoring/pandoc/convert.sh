#!/bin/bash

# this script convert docx to markdown
# if your file is not in docx but doc format, convert doc to docx -> https://www.freeconvert.com/doc-to-docx

set -e

FILENAME=velero

# convert .docx to .md
docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/core $FILENAME.docx --extract-media=./ -o $FILENAME.md

# move images to images folder
mkdir images && mv ./media/* ./images/ && rm -rf ./media

# convert images .tmp to .png
find ./images -name "*.tmp" -exec sh -c 'convert "$1" "${1%.tmp}.png" && rm "$1"' _ {} \;

# replace .tmp by .png and remove width/height attributes in markdown file
sed -i 's/\.tmp/\.png/g' $FILENAME.md
sed -i 's|./media/|./images/|g' kibana.md
sed -i 's/{width="[^"]*" height="[^"]*"}//g' kibana.md

echo 'Conversion successful completed!'

# cmd-shift-v -> Open markdown preview