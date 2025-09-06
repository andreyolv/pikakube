https://github.com/python-poetry/poetry

#  install poetry
sudo apt install pipx
pipx install poetry

poetry config --list

# iniciar poetry no projeto (se não tiver arquivo project.toml)
poetry init

# atualizar dependencias pelo cli
poetry add <lib>
poetry add <lib> --group dev
poetry remove <lib>

# após atualizar dependencias pelo pyproject.toml
poetry lock
poetry install

# entrar no poetry venv
poetry env activate -> show the command to active venv
eval "$(poetry env activate)" or venv -> echo "alias venv='source \"\$(poetry env info --path)/bin/activate\"'" >> ~/.bashrc

or 
poetry run <command>

poetry env remove --all

poetry env list

# analisar dependencias
poetry show

# sair do poetry venv
exit

boas praticas pra docker
https://github.com/orgs/python-poetry/discussions/1879
https://github.com/python-poetry/poetry/pull/9542

not support for constraints sad, uv has
https://github.com/python-poetry/poetry/issues/7051

Document docker poetry best practices
https://github.com/orgs/python-poetry/discussions/1879
https://github.com/python-poetry/poetry/pull/9542

poetry not support constraints
https://github.com/python-poetry/poetry/issues/7051
