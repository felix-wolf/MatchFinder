# MatchFinder
Matchfinder ist ein Service der bei gegebenen Teilnehmern, Themen/Gruppen und Präferenzen ein faires Match findet.

## TODO
- Fix bug bei dem die Aktionen der Verteilungen clippen, wenn nur ein Eintrag existiert
- Vuejs in Prod mode
- Editierfunkion einbauen
- Veto-Funktion optional machen
- MindestAnzahl von Stimmen
- Gruppen per Datei erstellen
- Teilnehmer mit Formular erstellen
- Inhalt für Home-Seite erstellen
- Datenbankeinträge nach einer Zeit löschen?
- offene Verteilungen können nicht erstellt werden
- falsche matr_nr führt zu fehler, hashed id
- Wahlen beschränken
- Keine Präferenzen hochzählen
- WikiDoc export



### Inhaltsverzeichnis
- [Dokumentation & Spezifikation](#dokumentation-spezifikation)
    - [Projektziel](#projektziel)
    - [Anforderungen](#anforderungen)
    - [Möglicher Technologiestack](#möglicher-technologiestack)
    - [Bereits bestehende Technologien](#bereits-bestehende-technologien)
    - [Prüfungsleistung](#prüfungsleistung)
- [Installation](#installation)
	- [Create Environment](#create-environment)
	- [Activate the Environment](#activate-the-environment)
	- [Install Flask](#install-flask)
	- [Run the Application](#run-the-application)

## Dokumentation & Spezifikation

Die Software dieses Repositorys entsteht im Rahmen des Projekt *Parallelrechnerevaluation* an der Universität Hamburg im Wintersemester 2020. Dabei ist [Felix Wolf](mailto:8fwolf@informatik.uni-hamburg.de) (ich) der alleinige Teilnehmer und Mitarbeiter dieses Projekts. Ansprechpartner sind [Anna Fuchs](mailto:anna.fuchs@informatik.uni-hamburg.de) und [Jannek Squar](mailto:squar@informatik.uni-hamburg.de).

### Projektziel

Innerhalb des WS 2020 soll eine Software entstehen, die bei gegebenen Teilnehmer, einer Anzahl Gruppen bzw. Themen und Präferenzen der Teilnehmer für die Themen ein faires Match findet (siehe [ungarische Methode](https://en.wikipedia.org/wiki/Hungarian_algorithm)). Als Grundlage dient ein Python-Script des Arbeitsbereichs, welches schon exisitert.

### Anforderungen

Es ist anzumerken, dass nicht alle der unten genannten Anforderungen erfüllt werden müssen. Vielmehr geht es darum, dass in der Zeit Mögliche umzusetzen, anstatt Anforderungen als unwartbaren Spaghetticode einzubauen.

- das System soll als eine Art Webapp in die Webseite des Arbeitsbereichs integriert werden
- funktionierendes Script, das gefundene Match soll nachweisbar ideal sein
- Liste der TeilnehmerInnen soll als Textdatei in einem Format, wie es durch STiNE ausgegeben wird, in das System ladbar sein
- wenn es mehrere, gleichgute Lösungen gibt, sollen die als Alternativen angezeigt werden
- Zuteilungsergebnisse sollen (auf ein Semester begrenzt) persistent gespeichert werden
- Möglichkeit für Studis, von Zuhause die Präferenzen vorzunehmen. Das beinhaltet:
	- Das System kennt im Voraus alle teilnehmenden StudentInnen mit Vor- und Nachnamen und Matrikelnummer.
	- Es gibt einen generischen Link, über den man zur gewünschten Verteilung kommt
	- Ein Studi kann sich gegenüber dem System authentifizieren, indem er/sie seine Matrikelnummer eingibt. Nur wenn die Matrikelnummer dem System bekannt ist, darf er/sie Präferenzen verteilen
	- Studis dürfen ein Veto für ein Thema/Gruppe abgeben, die sie unter keinen Umständen haben wollen
- Studis, die eine objektive schlechte Wahl bekommen haben (ab 4. aufwärts?), sollen irgendwie vertröstet werden
- Erstellung des Wahlszenarios
	- Zuordnung Thema : Studi soll für 1:1 oder 1:n einstellbar sein
	- Themen/Gruppen sollen eine Obergrenze an Teilnehmern haben
	- Es soll einstellbar sein, wieviele Präferenzen mindestens vergeben werden müssen
	- ein Wahlszenario soll in die Nachmeldephase gehen können, hier gilt Sudden death
- Sicherheitskonzepte in Theorie und/oder Umsetzung
	- Anfragen pro Minute begrenzen
	- Robustheit gegenüber falschen Anfragen (ungültige Matrikelnummer?)
	- Korrektur der Auswahl im Nachhinein möglich?
	- Risikoanalyse für mögliche Angriffe?

### Möglicher Technologiestack

- Python als Programmiersprache
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) als Backend/Webapplication engine
- [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) als Templatesprache
- Postresql als Datenbank (weil schon vorhanden)

### Bereits bestehende Technologien

- Python 3
- Postgres DBS
- Apache
- Ubuntu Server
- PHP 7.2
- Dokuwiki Instanz

### Prüfungsleistung

Der praktische Teil der Prüfungsleistung ist die Software selbst. Der theoretische Teil setzt sich zusammen aus einer Spezifikation und Dokumentation (dieses README, nur größer und besser) sowie einem kleinen Bericht, in dem der Arbeitsprozess zusammengefasst wird.

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

# Mitschrift Treffen 07.12.2020 (Muss überarbeitet werden)

### Fragen für Projekt:

- Wie viele Auswertungen maximal?
- was ist das für eine id bei den Gruppen?
- Strengere Trennung von Gruppen und Themen?
- Persistent speichern?



- alle Verteilungen drin lassen
    - nur 2 einblenden
    - hat jemand was dagegen?
    - wenn beide schlecht sind, eine würfeln
- Prio mit einbinden
- Alle Permutationen pro Matrix?
- ist es für mich ein Vorteil, ganz oben zu stehen? (Belohnung, weil früher eingetragen)
    - keine Permutation!
- Exportierfunktion (DokuWiki Format (markdown)) ohne Prios
- liste mit Übungen Enthalten Studenten, keine Tutoren!!!!!
- Angabe für Anzahl der Gruppen -> Studis werden auf die Gruppen verteilt
- Formular zum Gruppen erstellen
- Authentifizierung:
    - auch ohne Matrikelnummer?
    - Checkbox für mit oder ohne Matrikelnummer
- Editierfunktion
- 2 Checkboxen
    - Authentifizierung
    - Editierbar
- 2 root Passwörter (Brute Force Defence)
- Begrenzung für Matrikelnummereingaben (Brute Force Defence)
- Weitere Tabelleninhalte optional anzeigen (ausklappen?)
- Datenbank Tabelle für Thema erweitern um weitere optionale Felder
    - Studi und name sind safe
- Studi Liste aus Stine (mit oder ohne Gruppe, Gruppen direkt verwerfen)
- Themen in Formular erstellt oder aus simpler Liste (manuell erstellt)
- Datenbankeinträge nach einiger Zeit löschen?
- Nachwort im Bericht über mögliche Verbesserungen, ausstehende Features, Bugs
- Bitpoll api für Prios setzen?
    - beim button press csv von Bitpoll ziehen
- Studis, die keine Prios gesetzt haben, kriegen irgendwas
- QR-code zu link
- hash statt id für prios angeben (Hash aus id + Salt)
- immer max 10 Stimmen
- Priorität: 1-10 (lower is better)
- Themen, die keine Prio haben, sind alle gleich gewichtet

Gruppe Schema
- Name (required)
- Zeitpunkt (optional)
- Betreuer (optional)
    - Name, Zeitraum, Betreuer,
    - Name,,,

Umfrageplattformen
- Terminplaner4
- Bitpoll
- doodle
- moodle
