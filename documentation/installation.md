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

#### Vor dem ersten Start

Vor dem ersten Start der Anwendung müssen ein paar Vorkehrungen getroffen werden, damit die App richtig startet.

1. Um die Cookies für die Authentifizierung zu verwenden muss der App ein Secret-Key zugeteilt werden. Dieser wird in ```MatchFinder/matchFinder/config.py``` unter ```SECRET_KEY``` definiert und sollte möglichst sicher sein (siehe [hier](https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask) für eine beispielhafte Generierung).
2. Vor dem ersten Start müssen auch die Datenbanktabellen und gleichzeitig auch die Passwörter für die Authentifizierung erstellt werden. Die zu erstellenden Passwörter werden als Plain-Text in eine Datei mit dem Namen ```passwords.txt``` geschrieben (Datei auf Root-Ebene erstellen). Anschließend müssen folgende Zeilen einkommentiert werden:
    
```python
	# __init__.py
    
	with create_app().app_context():
		# ...
		from . import database_helper   #<- this line
		database_helper.init_db()       #<- this line


	# database_helper.py
            
	def init_db():
        
		reset_db() # <-- DANGER # this line
        
		rows = password_model.Password.query.count()
		if rows == 0:
			password_model.Password.query.delete()
			from . import password_helper
			password_helper.create_passwords()
```

Die ersten beiden Zeilen rufen ```init_db()``` in ```database_helper.py``` auf. Die Funktion ```reset_db()``` setzt die Datenbank zurück, indem alle Tabellen verworfen und neu angelegt werden. Anschließend speichern die unteren Zeilen die Passwörter aus passwords.txt als Hash in die Datenbank. **Wichtig:** Nach dem ersten erfolgreichen Start **müssen** die mit ```\# <- this line``` kommentierten Zeilen wieder auskommentiert werden, um bei einem späteren App-Neustart nicht versehentlich die Datenbank zurückzusetzen.


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