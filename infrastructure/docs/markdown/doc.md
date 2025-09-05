# linter
https://github.com/DavidAnson/markdownlint

# converter word do markdown
https://cloudconvert.com/doc-to-docx 
https://github.com/microsoft/markitdown -> lixo demais, não funciona direito
https://github.com/jgm/pandoc -> esse funciona, só instalação merda, melhor docker -> use o shellscript

docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/core kibana.docx --extract-media=./ -o kibana.md