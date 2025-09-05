https://github.com/mkdocs/mkdocs
https://github.com/squidfunk/mkdocs-material
https://github.com/oprypin/mkdocs-section-index

poetry lock
poetry install

poetry env activate -> show the command to active venv
eval "$(poetry env activate)" or venv -> echo "alias venv='source \"\$(poetry env info --path)/bin/activate\"'" >> ~/.bashrc

or poetry run <command>

---
poetry env remove --all

mkdocs serve

mkdocs build

mkdocs gh-deploy

