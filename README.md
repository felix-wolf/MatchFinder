# MatchFinder
Matchfinder ist ein Service der bei gegebenen Teilnehmern, Themen/Gruppen und Präferenzen ein faires Match findet.

### Inhaltsverzeichnis
- [Dokumentation & Spezifikation](#dokumentation-spezifikation)
    - [Projektziel](#projektziel)
    - [Anforderungen](#anforderungen)
    - [Möglicher Technologiestack](#möglicher-technologiestack)
    - [Bereits bestehende Technologien](#bereits-bestehende-technologien)
    - [Prüfungsleistung](#prüfungsleistung)

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
- Studis, die eine objektive schlechte Wahl bekommen haben (ab 4. aufwärts?), sollen irgendwie vertröstet werden
- Erstellung des Wahlszenarios
	- Themen/Gruppen sollen eine Obergrenze an Teilnehmern haben
	- Es soll einstellbar sein, wieviele Präferenzen mindestens vergeben werden müssen
	- ein Wahlszenario soll in die Nachmeldephase gehen können, hier gilt Sudden death


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