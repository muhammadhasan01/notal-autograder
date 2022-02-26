# Notal Autograder
Author: Muhammad Hasan

Algorithmic Notation Autograder using Control Flow Graph (CFG) Similarity.

# Dependencies

This project requires __python__ version __3.9__ or __later__.

(This is mainly because there are many typing hints used in this project, i.e `data: dict[str, any]`)

## Install all dependencies
```sh
pip install -r requirements.txt
```

## Update dependencies
```sh
pip freeze > requirements.txt
```


on windows you might encounter problem when installing pygraphviz, you can solve it by informing pip on where is graphviz installed, e.g.
```cmd
python -m pip install --global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib" pygraphviz
```

# How to Run in Virtualenv

## Create new virtual env
you only need to do this once
```sh
python3.9 -m venv .venv
```

## Start virtualenv
On linux
```sh
source .venv/bin/activate
```

On windows
```cmd
.venv\Scripts\activate.bat
```

## Run Project

First off install all the packages first using this command:

```bash
python3.9 -m pip install -r requirements.txt
```

Then run the service by using this command:

```bash
PYTHONPATH=$(pwd) python3.9 web_service/src/main.py
```

You can then try to hit the endpoint `http://127.0.0.1:5000/healthcheck` to see if it's working or not.


## Terminate Virtualenv
```sh
deactivate
```