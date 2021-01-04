## [Zurück zur Übersicht](../README.md)

# Dokumentation

## Inhaltsverzeichnis

- [Layout](#layout)
- [Struktur](#struktur)
- [Python-Dateien](#python-dateien)
	- [init.py](#initpy)
	- [database_helper.py](#database_helperpy)
	- [config.py](#configpy)
	- [matchCalculator.py](#matchcalculatorpy)
	- [password_helper.py](#password_helperpy)
- [Technisches](#technisches)
	- [Flask](#flask)
		- [Flask-Limiter](#flask-limiter)
		- [Flask-SQLAlchemy](#flask-sqlalchemy)
		- [Flask-WTF](#flask-wtf)
	- [Jinja2](#jinja2)
	- [Vue.js](#vuejs)
	- [SQLAlchemy](#sqlalchemy)
	- [WTForms](#wtforms)
- [Fachliches](#fachliches)
	- [Home](#home)
	- [Verteilung auswerten](#verteilung-auswerten)
	- [Verteilung erstellen](#verteilung-erstellen)
	- [Daten anlegen](#daten-anlegen)
	- [Angelegte Daten](#angelegte-daten)
	- [Präferenzvergabe](#praferenzvergabe)

## Layout

Die Webapp bietet ein simples Layout mit einer Seitenleite für die Navigation, einem Button zur Authentifikation in der Topbar und eine Überschrift auf jeder Seite.

Bei Darstellung auf kleinen Displays (z.B. auf mobilen Geräten) wechselt die App in ein mobile-freundliches Layout, die Seitenleiste kann hier ausgeklappt werden.

Für die visuelle Aufbereitung von HTML-Elementen über CSS etc. wird [Bootstrap](https://getbootstrap.com) verwendet.

## Struktur

Die allgemeine Struktur des Repositories und folglich auch der Flask-App lässt sich wie folgt darstellen:

```
.
├── matchFinder
│   ├── __init__.py
│   ├── auth.py
│   ├── create.py
│   ├── database_helper.py
│   ├── edit.py
│   ├── evaluate.py
│   ├── helper.py
│   ├── home.py
│   ├── matchCalculator.py
│   ├── password_helper.py
│   ├── preference.py
│   ├── share.py
│   ├── txt_parser.py
│   ├── upload.py
│   ├── forms
│   │   └── ...
│   ├── models
│   │   └── ...
│   ├── static
│   │   └── ...
│   └── templates
│       └── ...
├── documentation
│   └── ...
├── README.md
├── setup.sh
├── install.sh
└── list_of_blocked_ips.txt
...
```

Die Dateien auf root haben folgende Aufgaben:

- ```install.sh``` installiert alle nötigen Dependencies, die von der App benötigt werden. Es empfiehlt sich, die Flask App und alle Dependencies in einem *Virtual Environment* zu installieren und zu starten, um Konflikte mit bereits existierenden Dependencies zu vermeiden. Folglich sollte die ```install.sh```-Datei auch in dem Environment zu starten. Ein Environment wird erstellt und activiert mit

```bash
python3 -m venv venv	# <-- erstellt das Environment
. venv/bin/activate		# <-- Activiert das Environment
```

- ```setup.sh``` started die Flask-App
- ```list_of_blocked_ips.txt``` ist eine Liste von IP-Adressen, die in Vergangenheit verantwortlich für Spam und unerwünschte Aufrufe waren.
- ```README.md``` beinhaltet die Übersicht der Dokumentation

Der Unterordner ```matchFinder``` beinhaltet die die Flask App.

- **Root Level:** Auf Root Level des ```matchFinder``` befinden sich alle Endpunkte der App. Mehr dazu in [hier](#python-dateien).
- **Forms**: In ```forms``` sind die Formularvorlagen von ```WTForms```
- **Models**: In ```models``` sind die ORM-Klassen für ```SQLAlchemy```, also die Vorlagen aller Datenbanktabellen.
- **Static**: Im ```static``` Ordner sind statische HTML-Resourcen, wie das Favicon, das CSS für das Layout und die Vuejs-Library.
- **Templates**: Der ```templates``` Ordner beinhaltet alle HTML-Templates der App, die mit Jinja ausgebaut werden
- **Documentation**: In ```documentation``` sind die Markdown-Dateien der Dokumentation

## Python-Dateien

In den Python-Dateien im ```matchFinder``` Order stecken die gesamte Logik der App. Einzelne Dateien werden nun genauer beschrieben

### [__init__.py](../matchFinder/__init__.py)

Hier wird die Flask-App initialisiert und die Blueprints (definierte Endpunkte in anderen Dateien) registriert. Auch die Datenbank wird hier initialisiert.

Die App blockiert alle auf IP-Adressen, die auf der [Blacklist](../list_of_blocked_ips.txt) stehen. Beim ersten Aufrufen der App wird die IP-Adresse des Aufrufers einmalig mit diesen gesperrten IPs verglichen. Der Status (Zutritt erlaubt oder verweigert) wird in einem Cookie festgehalten. So muss der Status innerhalb einer Session nicht zweimal geprüft werden.

Zusätzlich beinhaltet die Datei einen Endpunkt für den Index ('/') und einen Endpunkt für alle Anfragen, die auf keinen gültigen Endpunkt verweisen. Letzterer gibt lediglich einen 404 zurück.

### [database_helper.py](../matchFinder/database_helper.py)

Database_helper ist die Schnittstelle zwischen App und Datenbank. Datenbankzugriffe geschehen nur in dieser Datei. Aus diesen Gründen bietet die Datei alle benötigten Datenbankoperationen für andere Dateien an.

### [config.py](../matchFinder/config.py)

Dies ist eine Config-Datei, ohne die die App nicht startet. In ihr wird der Pfad zur Datenbank, der Secret-Key (siehe [Secret-Key](https://flask.palletsprojects.com/en/1.1.x/api/?highlight=secret%20key#flask.Flask.secret_key)) und Eigenschaften der Dateien, die das System für den Upload erlaubt.

### [matchCalculator.py](../matchFinder/matchCalculator.py)

Das Herz der Matchberechnung. Hier wird mithilfe des Munkres-Algorithmus ein faires Match berechnet. Die Daten zu einem Match kommen dabei entweder aus einer Datei oder aus bestehenden Datenbankdaten.

Das Datenmodell ist dabei eine rechteckige Matrix mit Aufbau


| Name 			  | Thema1	| Thema2	| Thema3	|
|-----------------|---------|-----------|-----------|
| **Teilnehmer1** | w1,1	| w1,2		| w1,3		|
| **Teilnehmer2** | w2,1	| w2,2		| w2,3		|
| **Teilnehmer3** | w3,1	| w3,2		| w3,3		|

Dabei ist ```w2,1``` das Gewicht (die *Präferenz*) von Teilnehmer 2 zu Thema 1. Wird eine Verteilung als Datei hochgeladen, dann als *comma seperated values* (*csv*) Datei, in dem die Präferenzen als Text angegeben sind =>
```
Gewicht 1 = Erstwahl
Gewicht 2 = Zweitwahl
...
Gewicht 5 = Fünftwahl
...
```
Das höchste unterstützte Gewicht ist 10 (*Zehntwahl*). Wenn eine Option ganz ausgeschlossen werden soll, kann diese mit *Veto* markiert werden. Optionen ohne Präferenz kriegen keinen Wert (Achtung: Hier kann ungewolltes Verhalten auftreten, siehe [Details der Verteilungsberechnung](#details-der-verteilungsberechnung)).

Eine formatgerechte Datei sieht demnach so aus

```
Name,Thema1,Thema2,Thema3,Thema4
Teilnehmer1,Erstwahl,Zweitwahl,Drittwahl,Viertwahl
Teilnehmer2,Viertwahl,Drittwahl,Zweitwahl,Erstwahl
Teilnehmer3,Erstwahl,Zweitwahl,Drittwahl,Viertwahl
Teilnehmer4,Viertwahl,Zweitwahl,Drittwahl,Erstwahl
```

#### Details der Verteilungsberechnung

Da Verteilungsprobleme im Kern Kosten-Minimierungsprobleme sind, ergeben sich daraus bestimmte Eigenschaften, die zu beachten sind.

Angenommen, es gibt 2 Teilnehmer und 2 Gruppen. Teilnehmer 1 vergibt die Präferenzen ```Erstwahl, Zweitwahl```, Teilnehmer 2 vergibt ```Erstwahl,```. Teilnehmer 2 hat also für Gruppe 2 keine Präferenz angegeben.

### [password_helper.py](../matchFinder/password_helper.py)

## Technisches

### [Flask](https://flask.palletsprojects.com/en/1.1.x/)

Flask ist die Hauptkomponente des Backends der App. Mit Flask wird das Routing konfiguriert und die allgemeine Struktur der App. Flask bietet im Vergleich zur Alternative wie z.b. [Django](https://www.djangoproject.com) nur die absolute Basisfunktionalität und wird dann suksessive durch Erweiterungen ausgebaut.

Im Folgenden soll kurz etwas zu den verwendeten Erweiterungen gesagt werden:

#### [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/)

Mit Flask-Limiter kann die Anzahl auf der Zugriffe global oder auf spezifische Endpunkte begrenzt werden. Dies wird hier genutzt, um einzelne Endpunkte vor Brute-Force angriffen zu schützen und die gesamte WebApp gegen Angriffe robuster zu machen. Der Endpunkt für die allgemeine Authentifikation und die der Matrikelnummereingabe haben ein Limit von 5 Requests pro Minute. Die gesamte App ein

#### [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

Flask-SQLAlchemy ist die Schnittstelle zwischen Flask und SQLAlchemy, ein ORM für Python. Für mehr informationen siehe Abschnitt [```SQLAlchemy```](#sqlalchemy) unter ```Technisches```.

#### [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)

Ähnlich wie Flask-SQLAlchemy ist Flask-WTF eine Schnittstelle zwischen Flask und einer bestehenden Python-Erweiterung, hier [WTForms](https://wtforms.readthedocs.io/en/2.3.x/). Für mehr informationen siehe den Abschnitt [```WTForms```](#wtforms) unter ```Technisches```.

### [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)

Jinja2 ist die Template-Sprache, die standardmäßig bei Flask dabei ist. Mit Jinja kann in HTML Basisoperationen wie if-Abfragen, Schleifen und weiteres verwirklicht werden. Viel wichtiger ist jedoch die Möglichkeit, Daten die dem Template mitgegeben werden zu rendern. Übergebe ich Flask zu einem Template auch einen oder mehrere Parameter über die ```render_template(...)``` Funktion

```python
render_template('template.html', parameter="Dies ist ein Parameter")
```

kann dieser mit Jinja über ```{{parameter}}``` gerendert und damit der Inhalt angezeigt werden.

### [Vue.js](https://vuejs.org)

Vue.js ist ein progressives JavaScript Framework für dynamisches Rendern von HTML-Elementen. In Matchfinder gibt es mehrere Stellen, in denen Vue.js benutzt wird. Allgemein wird Vue in der App benutzt, um situationsbedingt Seitenelemente anzuzeigen oder zu verstecken. Des Weiteren berechnet Vue einzelne Schwellwerte, von denen die Darstellung von Elementen abhängt. Vue wird in den Bereichen [Präferenzvergabe](#präferenzvergabe), [Verteilung auswerten](#verteilung-auswerten), [Verteilung Erstellen](#verteilung-erstellen) und [Daten anlegen](#daten-anlegen) benutzt.

### [SQLAlchemy](https://www.sqlalchemy.org)

SQLAlchemy bietet die Möglichkeit, ein Datenbankschema als ORM, also Object-Relation-Model anzulegen. Dies bedeutet, dass einzelne Tabellen als Klassen aus der Objektorientierung erstellt werden, welche die Tabellenspalten als Exemplarvariablen beinhalten. In diesen Exemplarvariablen werden dann Eigenschaften wie Typ, Referenz zu anderen Tabellen und Cascade-Vorgänge beschrieben.

Beispielsweise ist die Teilnehmer-Tabelle wie folgt definiert:

```python
from flask_sqlalchemy import *

class Teilnehmer(db.Model):
	__tablename__ = "teilnehmer"
	id = db.Column(db.Integer, primary_key=True)
	list_id = db.Column(db.Integer, db.ForeignKey("teilnehmer_lists.id"), nullable=False)
	praeferenzen = db.relationship("Praeferenz", cascade="all,delete", backref="teilnehmer", lazy=True)
	first_name = db.Column(db.String(80), nullable=False)
	last_name = db.Column(db.String(80))
	matr_nr = db.Column(db.Integer)
```

### [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)

Mit WTForms können Fomulare einfach und effizient erstellt werden über Klassen erstellt werden. Wie bei SQLAlchemy wird durch eine Klasse und ihre Variablen definiert, welche Arten von Feldern ein Formular hat. Besonders interessant ist hier die Möglichkeit zu überprüfen, ob ein Formular alle nötigen Informationen beinhaltet um als 'gültig' zu gelten. Mit WTForms können also Formulare und Formularinformationen ohne großen Aufwand in Objekte umgewandelt werden.

WTForms wird für die Erstellung der Teilnehmer und Themen per Formular benutzt. Hier ist im Voraus nicht bekannt, wie viele Teilnehmer und Themen erstellt werden sollen, also wie viele Formularfelder erzeugt werden müssen.

Die Klasse für das Formular der Teilnehmer ist wie folgt definiert:

```python
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired

class TeilnehmerEntryForm(FlaskForm):
	first_name = StringField('Vorname', validators=[DataRequired()])
	last_name = StringField('Nachname')
	matr_nr = IntegerField('Matrikelnummer')


class TeilnehmerForm(FlaskForm):
	teilnehmer_name = StringField('Name', validators=[DataRequired()])
	teilnehmer = FieldList(FormField(TeilnehmerEntryForm), validators=[DataRequired()])
```

An anderen Stellen, an denen die Komplexität überschaubarer war, konnte auf WTForms aus Aufwandgründen verzichtet werden.

## Fachliches

### Home

### Verteilung auswerten

### Verteilung erstellen

### Daten anlegen

### Angelegte Daten

### Präferenzvergabe


Wird bei der Präferenzvergabe eine der Antwortmöglichkeiten (z.B. Erstwahl) für eine der Themen angegeben, verschwindet diese Möglichkeit aus den Antwortmöglichkeiten der anderen Themen. Darüber hinaus