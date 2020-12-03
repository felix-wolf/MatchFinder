#!/bin/bash

. venv/bin/activate

export FLASK_APP=matchFinder

export FLASK_ENV=development

#flask init-db

flask run