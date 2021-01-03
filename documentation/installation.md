## [Zurück zur Übersicht](../README.md)

# Installation

For more information, see [this setup guide](https://flask.palletsprojects.com/en/1.1.x/installation/#install-create-env) and [this tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/).

##### Environment erstellen

```bash
python3 -m venv venv
```

##### Environment aktivieren

```bash
. venv/bin/activate
```

##### Dependencies installieren

Benötigte Dependencies innerhalb es aktivierten Environment installieren:

```bash
pip3 install flask

pip3 install flask_sqlalchemy

pip3 install munkres

pip3 install pandas

pip3 install markdown

pip3 install flask_limiter

pip3 install Flask-WTF

pip3 install qrcode

pip3 install Pillow

pip3 install bcrypt
```

##### Run the Application

```bash
export FLASK_APP=matchFinder
export FLASK_ENV=development # <-- nur für development-Zwecke
flask run
```

Alternativ kann mit

```bash
flask run --host=0.0.0.0
```
die Flask App gestartet werden und allen geräten im gleichen Netz zur verfügung gestellt werden. Die App kann dann über ```<IP DES HOSTS>:5000``` erreicht werden.