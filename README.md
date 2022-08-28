# Notal Autograder
**Author: Muhammad Hasan**

Control Flow Graph Based Notasi Algoritmik Autograder.

# Dependencies

This project requires __python__ version __3.9__ or __later__.

(This is mainly because there are many typing hints used in this project, i.e `data: dict[str, any]`)

## Installing all dependencies
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

# How to Run

## Running on Docker

Luckily, this project does not require many dependencies, so you can simply run this service with [Docker](https://www.docker.com/).

Once `docker` and `docker-compose` is installed you can simply run this command on your terminal:

```bash
docker-compose up
```

This will build and run the [Dockerfile](./Dockerfile). If no problems were found, you will see this in your terminal:

```bash
...
app_1  |  * Serving Flask app "main" (lazy loading)
app_1  |  * Environment: production
app_1  |    WARNING: This is a development server. Do not use it in a production deployment.
app_1  |    Use a production WSGI server instead.
app_1  |  * Debug mode: off
app_1  |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Note that even though it says `http://0.0.0.0:5000`, the service can only be accessed at `http://127.0.0.1:5000` or `localhost:5000`.

Now you can check `localhost:5000/health-check` to see if it's successfully running or not.

<!-- TODO: Add Documentation on API -->

## Running on Virtual Environment

You can also run this on python virtual environment. Follow the steps bellow:

### Create new virtual env
you only need to do this once
```sh
python3.9 -m venv .venv
```

### Start virtualenv
On linux
```sh
source .venv/bin/activate
```

On windows
```cmd
.venv\Scripts\activate.bat
```

### Run Project

First off install all the packages first using this command:

```bash
python3.9 -m pip install -r requirements.txt
```

Then run the service by using this command:

```bash
PYTHONPATH=$(pwd) python3.9 web_service/src/main.py
```

You can then try to hit the endpoint `localhost:5000/health-check` to see if it's working or not.


### Terminate Virtualenv
```sh
deactivate
```
