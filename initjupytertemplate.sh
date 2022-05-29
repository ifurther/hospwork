#!/bin/env bash
pipenv run jupyter contrib nbextension install --user; \
           jupyter nbextension install --py jupytemplate --sys-prefix; \
           jupyter nbextension enable jupytemplate/main --sys-prefix
