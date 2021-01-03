# Spezifikation

## Überblick

Die Software dieses Repositorys entsteht im Rahmen des Projekt *Parallelrechnerevaluation* an der Universität Hamburg im Wintersemester 2020. Dabei ist [Felix Wolf](mailto:8fwolf@informatik.uni-hamburg.de) der alleinige Teilnehmer und Mitarbeiter dieses Projekts. Ansprechpartner sind [Anna Fuchs](mailto:anna.fuchs@informatik.uni-hamburg.de) und [Jannek Squar](mailto:squar@informatik.uni-hamburg.de).

### Projektziel

Innerhalb des WS 2020 soll eine Software entstehen, die bei gegebenen Daten ein faires Verteilung (ein *Match*) findet. Die gegebenen Daten umfassen:

- Liste an Teilnehmern
- Gruppen bzw. Themen
- Präferenzen der Teilnehmer für die Gruppen/Themen


Eine faire Verteilung ist eine Zuordnung von Teilnehmer zu Themen, die die Kosten minimiert und im Vergleich zu allen anderen Zuordnungen besser oder gleich gut ist. Kosten sind die Präferenzen der Teilnehmer. Die Präferenzen ```Erstwahl, Zweitwahl``` übersetzen sich in die Kosten ```1, 2```. Verteilungen werden nach ihrem Median und der absoluten TODO Streuungsmaß sortiert.

Faire Verteilungen werden mithilfe der [ungarischen Methode](https://en.wikipedia.org/wiki/Hungarian_algorithm) gefunden.

Als Grundlage diente ein Python-Script des Arbeitsbereichs, welches schon exisiterte.

### Anforderungen

Es ist anzumerken, dass nicht alle der unten genannten Anforderungen erfüllt werden müssen. Vielmehr geht es darum, dass in der Zeit Mögliche umzusetzen, anstatt Anforderungen als unwartbaren Spaghetticode einzubauen.

- das System soll als eine Art Webapp in die Webseite des Arbeitsbereichs integriert werden
- die gefundene Verteilung soll nachweisbar ideal sein
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
- 2 Checkboxen
    - Authentifizierung
    - Editierbar
- 2 root Passwörter (Brute Force Defence)
- Editierfunktion
- Begrenzung für Matrikelnummereingaben (Brute Force Defence)
- Weitere Tabelleninhalte optional anzeigen (ausklappen?)
- QR-code zu link
- hash statt id für prios angeben (Hash aus id + Salt)
- immer max 10 Stimmen
- Priorität: 1-10 (lower is better)
- Themen, die keine Prio haben, sind alle gleich gewichtet
- Themen in Formular erstellt oder aus simpler Liste (manuell erstellt)
- Nachwort im Bericht über mögliche Verbesserungen, ausstehende Features, Bugs
- Formular zum Gruppen erstellen
- Exportierfunktion (DokuWiki Format (markdown)) ohne Prios
- Angabe für Anzahl der Gruppen -> Studis werden auf die Gruppen verteilt
- Authentifizierung:
    - auch ohne Matrikelnummer?
    - Checkbox für mit oder ohne Matrikelnummer

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

Der praktische Teil der Prüfungsleistung ist die Software selbst. Der theoretische Teil setzt sich zusammen aus einer Spezifikation und Dokumentation (dieses hier) sowie einem kleinen Bericht, in dem der Arbeitsprozess zusammengefasst wird.