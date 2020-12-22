## Installation

For more information, see [this setup guide](https://flask.palletsprojects.com/en/1.1.x/installation/#install-create-env) and [this tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/).

##### Create Environment

```bash
python3 -m venv venv
```

##### Activate the Environment

```bash
. venv/bin/activate
```

##### Install Flask

Install Flask within the activated environment

```bash
pip3 install Flask
```

##### Run the Application

```bash
export FLASK_APP=matchFinder
export FLASK_ENV=development
flask run
```