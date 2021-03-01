## [Zurück zur Übersicht](../README.md)

# Installation

In diesem Kapitel ist beschrieben, welche Abhängigkeiten installiert sein müssen, um die Flask-App zu starten und sie weiterzuentwickeln. Darüber hinaus können weitere Informationen zur Funktionsweise von Flask-Applikationen und deren Entwicklung [diesem Guide](https://flask.palletsprojects.com/en/1.1.x/installation/#install-create-env) und [diesem Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/) der Herausgeber von Flask entnommen werden.

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
pip install flask

pip install flask_sqlalchemy

pip install munkres

pip install pandas

pip install markdown

pip install flask_limiter

pip install Flask-WTF

pip install qrcode

pip install Pillow

pip install bcrypt
```

Innerhalb des Environment kann der Befehl ```pip``` verwendet werden, um ```pip3``` auszuführen.

##### Die App ausführen

```bash
export FLASK_APP=matchFinder
export FLASK_ENV=development # <-- nur für development-Zwecke
flask run
```

Alternativ kann mit

```bash
flask run --host=0.0.0.0
```
die Flask App gestartet und allen Geräten im gleichen Netz zur Verfügung gestellt werden. Die App kann dann über ```<IP DES HOSTS>:5000``` erreicht werden.