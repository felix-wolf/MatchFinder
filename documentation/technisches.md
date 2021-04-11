## [Zurück zur Übersicht](../dokumentation.md)

# Technisches

## Inhaltsverzeichnis

- [Layout](#layout)
- [Struktur](#struktur)
- [Python-Dateien](#python-dateien)
	- [init.py](#initpy)
	- [database_helper.py](#database_helperpy)
	- [config.py](#configpy)
	- [matchCalculator.py](#matchcalculatorpy)
	- [password_helper.py](#password_helperpy)
	- [Endpunkte](#endpunkte)
- [Templates](#html-templates)
- [Technologien](#technologien)
	- [Flask](#flask)
		- [Flask-Limiter](#flask-limiter)
		- [Flask-SQLAlchemy](#flask-sqlalchemy)
		- [Flask-WTF](#flask-wtf)
	- [Jinja2](#jinja2)
	- [Vue.js](#vuejs)
	- [SQLAlchemy](#sqlalchemy)
	- [WTForms](#wtforms)

## Struktur

Die allgemeine Struktur des Repositories und folglich auch der Flask-App lässt sich wie folgt darstellen:

```
.
├── matchFinder
│   ├── <Python-Dateien>
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
├── requirements.txt
└── list_of_blocked_ips.txt
...
```

Die Dateien auf root haben folgende Aufgaben:

- ```install.sh``` erstellt und aktiviert ein virtuelles Environment, bevor alle nötigen Dependencies, die von der App benötigt werden, installiert werden.
- ```setup.sh``` started die Flask-App im Develop-Modus.
- ```list_of_blocked_ips.txt``` ist eine Liste von IP-Adressen, die in Vergangenheit verantwortlich für Spam und unerwünschte Aufrufe waren. Bei erstmaligem Aufrufen der Webseite eines Nutzers wird geprüft, ob sich die IP-Adresse des Benutzers auf dieser Liste befindet. Ist dies der Fall, wird der Zugriff verwehrt.
- ```README.md``` beinhaltet die Übersicht der Dokumentation.
- ```requirements.txt``` listet alle benötigten (transitiven) Abhängigkeiten des Systems auf. Die Datei wird mit Pip Freeze generiert und kann dazu genutzt werden, ähnlich wie install.sh alle Abhängigkeiten gebündelt zu installieren.

Der Unterordner ```matchFinder``` beinhaltet die Flask App.

- **Root Level:** Auf Root Level von ```matchFinder``` befinden sich alle Endpunkte der App. Mehr dazu [hier](#python-dateien).
- **Forms**: In ```forms``` sind die Formularvorlagen von ```WTForms``` für einige Formularabfragen abgelegt.
- **Models**: In ```models``` befinden sich die ORM-Klassen für ```SQLAlchemy```, also die Vorlagen aller Datenbanktabellen.
- **Static**: Im ```static``` Ordner sind statische HTML-Resourcen, wie das Favicon, das CSS für das Layout und die Vuejs-Library gespeichert.
- **Templates**: Der ```templates```-Ordner beinhaltet alle HTML-Templates der App, die mit Jinja ausgebaut werden
- **Documentation**: In ```documentation``` liegen die Markdown-Dateien der Dokumentation und die verwendeten Abbildungen.

## Layout

Die Webapp bietet ein simples Layout mit einer Seitenleiste für die Navigation, einem Button zur Authentifikation in der Topbar und eine Überschrift auf jeder Seite.

Bei Darstellung auf kleinen Displays (z.B. auf mobilen Geräten) wechselt die App in ein mobile-freundliches Layout. Hier ist die Seitenleiste nicht dauerhaft sichtbar, sondern wird ausgeklappt.

Für die visuelle Aufbereitung von HTML-Elementen über CSS etc. wird [Bootstrap](https://getbootstrap.com) verwendet.

## Python-Dateien

Die Python-Dateien im ```matchFinder```-Order beinhalten die gesamte Logik der App. Einzelne Dateien werden nun genauer beschrieben.

### [__init__.py](../matchFinder/__init__.py)

Hier wird die Flask-App initialisiert und die Blueprints (definierte Endpunkte in anderen Dateien) registriert. Auch die Datenbank wird hier initialisiert.

Hier ist auch die Logik der Blacklist definiert: Die App blockiert alle auf IP-Adressen, die auf der [Blacklist](../list_of_blocked_ips.txt) stehen. Beim ersten Aufrufen der App wird die IP-Adresse des Aufrufers einmalig mit diesen gesperrten IPs verglichen. Der Status (Zutritt erlaubt oder verweigert) wird in einem Cookie festgehalten. So muss der Status innerhalb einer Session nicht zweimal geprüft werden.

Zusätzlich beinhaltet die Datei einen Endpunkt für den Index ('/') und einen Endpunkt für alle Anfragen, die auf keinen gültigen Endpunkt verweisen. Index wird auf ```/home``` weitergeleitet, ungültige Anfragen geben einen 404-Fehler zurück.

### [database_helper.py](../matchFinder/database_helper.py)

Database_helper ist die Schnittstelle zwischen App und Datenbank. Datenbankzugriffe geschehen nur in dieser Datei. Aus diesen Gründen bietet die Datei alle benötigten Datenbankoperationen für die andere Klassen und Blueprints an.

### [config.py](../matchFinder/config.py)

Dies ist eine Konfigurationsdatei, ohne die die App nicht startet. In ihr wird der Pfad zur Datenbank, der Secret-Key (siehe [Secret-Key](https://flask.palletsprojects.com/en/1.1.x/api/?highlight=secret%20key#flask.Flask.secret_key)) und Eigenschaften der Dateien, die das System für den Upload erlaubt, definiert.

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
Das höchste unterstützte Gewicht ist zehn (*Zehntwahl*). Wenn eine Option ganz ausgeschlossen werden soll, kann diese mit *Veto* markiert werden. Optionen ohne Präferenz werden automatisch durch das System aufgefüllt.

Eine formatgerechte Datei sieht demnach so aus

```
Name,Thema1,Thema2,Thema3,Thema4
Teilnehmer1,Erstwahl,Zweitwahl,Drittwahl,Viertwahl
Teilnehmer2,Viertwahl,Drittwahl,Zweitwahl,Erstwahl
Teilnehmer3,Erstwahl,Zweitwahl,,Viertwahl
Teilnehmer4,Viertwahl,Zweitwahl,Drittwahl,Erstwahl
```

#### Begrenzung auf nur zehn Präferenzen

Das System unterstützt momentan bis zu 10 Präferenzen. Die bedeutet, dass die Felder  nach der Zehntwahl entweder dynamisch hochgezählt (Bei Präferenzvergabe über das System) oder mit dem statischen Gewicht von 100 (bei Berechnung aus Datei) belegt werden.

Dieser Umstand ist eine bewusste Entscheidung. Unter anderem sprechen diese Gründe für eine Begrenzung:

1. In den seltensten Fällen möchte ein Teilnehmer mehr als 10 Präferenzen angeben. Die Wahrscheinlichkeit, nicht eine der ersten 10 Wahlen zu bekommen ist bei moderat großen Themen und Teilnehmern gering.
2. Um den Teilnehmern die Vergabe einer ```Erstwahl``` anstatt einer ```1``` zu ermöglichen, müssen diese Antwortmöglichkeiten hardgecodet werden und können nicht (anders als Zahlen) dynamisch generiert werden. Hier stellt sich die Frage, ob sich eine Implementation von beispielsweise 100 Antwortmöglichkeiten überhaupt lohnt, wenn in den meisten Fällen nur die ersten 10 Vergeben werden.

### [password_helper.py](../matchFinder/password_helper.py)

Die Datei ```password_helper``` ist zuständig für das Generieren und Überprüfen von Passwörtern. MatchFinder benutzt kein vollständiges User-Password-System, hierfür existiert schlichtweg keine Notwendigkeit. Vielmehr können sich User über zuvor definierte geheime Schlüssel gegenüber dem System authentifizieren. Einmal authentifiziert stehen dem User dann eine Vielzahl von Funktionen zur Verfügung, die vor dem Zugriff eines unauthorisiertem Benutzers verborgen und blockiert sind.

Geschützte Seitenendpunkte sind visuell in der Seitenleiste nicht sichtbar und die einzelnen Endpunkte überprüfen bei jedem Zugriff den Status des Nutzers. Ist dieser nicht berechtigt wird der User auf die Hauptseite zurückgeleitet:

```python
@bp.before_request
def check_status():
    if session.get('is_authenticated') != True:
        return redirect(url_for('home.index'))
```

Die auf diese Weise geschützen Endpunkte sind: ```/share, /edit, /preview, /upload, /create```.

Mithilfe der ```Session``` können Informationen über die Session des Nutzers gespeichert werden. In diesem Fall wird sie genutzt für die Authentifizierung mittels Passwort. In ihr wird auch gespeichert, ob der Seitenbesucher mit einer vertrauenswürdigen IP-Adresse die Seite ansteuert (mehr dazu [hier](#initpy)).

Diese Informationen werden in einem Cookie gespeichert. Dieser Cookie ist der einzige, der auf der Webseite zum Einsatz kommt. Es gibt **kein** Tracking oder ähnliches.

### Endpunkte

Pro Endpunkt der Flaskapp gibt es eine Datei, die einen sog. Blueprint definiert. Die Endpunkte der App sind:

- [/auth](../matchFinder/auth.py)
- [/create](../matchFinder/create.py)
- [/edit](../matchFinder/edit.py)
- [/evaluate](../matchFinder/evaluate.py)
- [/home](../matchFinder/home.py)
- [/preview](../matchFinder/preview.py)
- [/preference](../matchFinder/preference.py)
- [/share](../matchFinder/share.py)
- [/upload](../matchFinder/upload.py)

Jeder dieser Blueprints definiert bestimmte Haupt- und Unterendpunkte, generiert Inhalte und veranlasst Redirects bzw. das Rendern von HTML-Dateien.

Einige diesen Endpunkte sind nur für authentifizierte Benutzer erreichbar. Geschütze Endpunkte sind: /create, /edit, /share und /upload.

## HTML-Templates

Die HTML Templates befinden sich im Verzeichnis [matchFinder/templates](../matchFinder/templates).

Die Datei ```layout.html``` ist das Base-Template. Die anderen Templates erben mithilfe des Befehls

```{% extends "layout.html" %}```

vom Base-Template und können die in layout.html definierten Blöcke befüllen. So muss z.B. die Seitenleiste und die Topbar nur einmal im Base-Template definiert werden und steht durch Vererbung in allen anderen Templates zur Verfügung.

Das Base-Template lädt auch Bootstrap für das Styling, das Favicon und bindet bei Bedarf Vue.js ein.

## Technologien

### [Flask](https://flask.palletsprojects.com/en/1.1.x/)

Flask ist die Hauptkomponente des Backends der App. Mit Flask wird das Routing konfiguriert und die allgemeine Struktur der App. Flask bietet im Vergleich zu Alternativen wie z.b. [Django](https://www.djangoproject.com) nur die absolute Basisfunktionalität und wird dann suksessive durch Erweiterungen ausgebaut.

Im Folgenden soll kurz etwas zu den verwendeten Erweiterungen gesagt werden:

#### [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/)

Mit Flask-Limiter kann die Anzahl der Zugriffe global oder auf spezifische Endpunkte begrenzt werden. Dies wird von MatchFinder genutzt, um einzelne Endpunkte vor Brute-Force-Angriffen zu schützen und die gesamte App gegen Angriffe robuster zu machen. Der Endpunkt für die allgemeine Authentifikation und die der Matrikelnummereingabe haben ein Limit von 5 Anfragen pro Minute.

#### [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

Flask-SQLAlchemy ist die Schnittstelle zwischen Flask und SQLAlchemy, ein ORM für Python. Für mehr Informationen siehe Abschnitt [```SQLAlchemy```](#sqlalchemy) unter ```Technisches```.

#### [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)

Ähnlich wie Flask-SQLAlchemy ist Flask-WTF eine Schnittstelle zwischen Flask und einer bestehenden Python-Erweiterung, hier [WTForms](https://wtforms.readthedocs.io/en/2.3.x/). Für mehr Informationen siehe den Abschnitt [```WTForms```](#wtforms) unter ```Technisches```.

### [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)

Jinja2 ist die Template-Sprache, die standardmäßig bei Flask dabei ist. Mit Jinja können in HTML Basisoperationen wie if-Abfragen, Schleifen u. w. verwirklicht werden. Viel wichtiger ist jedoch die Möglichkeit, Daten, die dem Template mitgegeben werden, zu rendern. Wird Flask zu einem Template mit

```python
render_template('template.html', parameter="Dies ist ein Parameter")
```

auch ein Paramter übergeben, kann dieser mit Jinja über ```{{parameter}}``` als Klartext gerendert und damit sein Inhalt angezeigt werden. Auch können ganze Objekte oder Arrays ins Template geladen und mit Jinja verarbeitet werden (z.B. ein HTML-Block für jeden Arrayeintrag).

### [Vue.js](https://vuejs.org)

Vue.js ist ein progressives JavaScript Framework für dynamisches Rendern von HTML-Elementen. In Matchfinder gibt es mehrere Stellen, in denen Vue.js benutzt wird. Allgemein wird Vue in der App benutzt, um situationsbedingt Seitenelemente anzuzeigen oder zu verstecken. Des Weiteren berechnet Vue einzelne Schwellwerte, von denen die Darstellung von Elementen abhängt. Vue wird in den Bereichen [Präferenzvergabe](#präferenzvergabe), [Verteilung auswerten](#verteilung-auswerten), [Verteilung Erstellen](#verteilung-erstellen) und [Daten anlegen](#daten-anlegen) benutzt.

### [SQLAlchemy](https://www.sqlalchemy.org)

SQLAlchemy bietet die Möglichkeit, ein Datenbankschema als ORM, also Object-Relation-Model anzulegen. Dies bedeutet, dass einzelne Tabellen als Klassen aus der Objektorientierung erstellt werden, welche die Tabellenspalten als Exemplarvariablen beinhalten. In diesen Exemplarvariablen werden dann Eigenschaften wie Typ, Referenz zu anderen Tabellen und Cascade-Bedingungen beschrieben.

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

Mit WTForms können Fomulare einfach und effizient über Klassen erstellt werden. Wie bei SQLAlchemy wird durch eine Klasse und ihre Variablen definiert, welche Arten von Feldern ein Formular hat. Besonders interessant ist hier die Möglichkeit zu überprüfen, ob ein Formular alle nötigen Informationen beinhaltet um als 'gültig' zu gelten. Mit WTForms können also Formulare und Formularinformationen ohne großen Aufwand in Objekte umgewandelt werden.

WTForms wird für die Erstellung der Teilnehmer und Themen per Formular benutzt. Hier ist im Voraus nicht bekannt, wie viele Teilnehmer und Themen erstellt werden sollen, also wie viele Formularfelder erzeugt werden müssen. WTForms erzeugt dynamisch die richtige Anzahl von *TeilnehmerEntryForm* (siehe Codebeispiel) und validiert diese später.

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

An Stellen, an denen die Komplexität der Formulare überschaubarer ist, konnte auf WTForms verzichtet werden. Dort werden die Formularfelder manuell definiert.

## [zurück nach oben](#zuruck-zur-ubersicht)