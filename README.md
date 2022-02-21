# Notal Autograder
Author: Muhammad Hasan

Algorithmic Notation Autograder using CFG Similarity.

# Dependencies

This project require having __python__ version __3.8__ or __later__.

## update dependencies
```sh
pip freeze > requirements.txt
```

## install all dependencies
```sh
pip install -r requirements.txt
```

on windows you might encounter problem when installing pygraphviz, you can solve it by informing pip on where is graphviz installed, e.g.
```cmd
python -m pip install --global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib" pygraphviz
```

# How to Use Virtualenv

## create new virtual env
you only need to do this once
```sh
python3 -m venv .venv
```

## start virtualenv
On linux
```sh
source .venv/bin/activate
```

On windows
```cmd
.venv\Scripts\activate.bat
```

## terminate Virtualenv
```sh
deactivate
```