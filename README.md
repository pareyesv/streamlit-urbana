# Introduction

Streamlit demo for spatial data

# Getting Started

To run the app, do

```console
make run-app
```

and follow the instructions.

# Contribute

## Init

To start, please create a virtualenvironment. The `Makefile` assumes the name of the virtualenv is `streamlit-urbana`. Then, activate the environment.

Then, run:

```console
make init
```

Then, install the rest of the dependencies as suggested in [](#dependencies).

## Dependencies

To add/change a dependency, please edit the file `requirements.in`.

Then, run

```console
pip-compile
```

The command abobe will update the `requirements.txt` accordingly.

If the dependency is related to development, please edit the file `requirements-dev.in`.
Then, run

```console
pip-compile requirements-dev.in
```

The command will update the file `requirements-dev.txt`.

Then, to update the environment with the new changes in `requirements.txt` (or `requirements-dev.txt`), run

```console
pip-sync requirements.txt requirements-dev.txt
```

All the steps above can be done by using the `Makefile`:

```console
make update-env
```

## Run the app

To run the app, do:

```console
make run-app
```

## Commits convention

This project adheres to the [Conventional commits](https://www.conventionalcommits.org/) conventions.
