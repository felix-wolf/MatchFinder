## [Zurück zur Übersicht](../dokumentation.md)

# Fachliches

## Inhaltsverzeichnis

- [Home](#home)
- [Verteilung auswerten](#verteilung-auswerten)
- [Verteilung erstellen](#verteilung-erstellen)
- [Daten anlegen](#daten-anlegen)
- [Angelegte Daten](#angelegte-daten)
- [Präferenzvergabe](#praferenzvergabe)

## Home

Auf der Home-Seite (```/```) findet der Nutzer allgemeine Informationen über den Dienst und die angebotenen Funktionen. Sie ist sowohl über den Menüpunkt *Home* als auch über den Schriftzug *MatchFinder* in der oberen Leiste zu erreichen.

## Verteilung auswerten

Über den Menüpunkt *Verteilung auswerten* (```/evaluate```) wird die Funktion angeboten, Verteilungen (aus Dateien oder aus Datenbankdaten) auszuwerten. Die volle Funktionalität steht nur einem authentifizierten Benutzer zu Verfügung. Unauthentifizierte Benutzer haben nur Zugriff auf die Funktion eine Verteilung aus einer Datei zu erstellen:

### Verteilung aus einer Datei auswerten

Eine Verteilung kann auch ausgewertet werden, wenn die Präferenzen als CSV-Datei vorliegen. Voraussetzung hierfür ist, dass die Datei folgendes Format unterstützt:

1. die durch die Datei beschriebene Matrix ist rechteckig (alle Zeilen gleicher Länge)
2. in der ersten Zeile sind die Namen der Gruppen / Themen, wobei Zelle 0,0 frei bleibt bzw. nur einen Platzhalter beinhaltet
3. in der ersten Spalte befinden sich die Namen der Teilnehmer nur durch Leerzeichen getrennt, keine Kommata
4. die Präferenzen sind als Bezeichnung angegeben, nicht als Zahl (Erstwahl statt 1, Zweitwahl statt 2 etc.)
5. die maximal angebenen Präferenz ist die Zehntwahl, darüber hinaus werden keine weiteren Präferenzen angegeben

Beispielformat:

Eine formatgerechte Datei sieht demnach so aus

```
PLATZHALTER,Thema1,Thema2,Thema3,Thema4
Teilnehmer1,Erstwahl,Zweitwahl,Drittwahl,Viertwahl
Teilnehmer2,Viertwahl,Drittwahl,Zweitwahl,Erstwahl
Teilnehmer3,Erstwahl,Zweitwahl,,
Teilnehmer4,,Zweitwahl,Drittwahl,Erstwahl
```

Für eine optimale Auswertung sollten so viele Angaben wie möglich gemacht werden.

### Verteilung aus Datenbankdaten auswerten

Sind noch keine Daten in der Datenbank angelegt, steht dem authentifizierten Benutzer die gleiche Funktionalität wie [oben](#verteilung-aus-einer-datei-auswerten) beschrieben. Er erhält außerdem noch einen Verweis auf die *Verteilung anlegen*-Funktion, über welche er eine Verteilung anlegen kann.

WEITERSCHREIBEN

## Verteilung erstellen

*Dieser Seitenabschnitt steht nur authentifizierten Benutzern zur Verfügung.*

Sind zuvor Teilnehmer und Gruppen angelegt worden, kann auf dieser Unterseite eine Verteilung erstellt werden. Wenn nicht, beinhaltet die Seite einen Verweis auf die [*Daten-anlegen*](#daten-anlegen)-Funktion, über welche dann Teilnehmer und Gruppen / Themen erstellt werden können.

Verteilungen zu erstellen bedeutet, zu einer gegebenen Gruppe eine Liste an Teilnehmern (vorausgesetzt, die Verteilung ist geschützt) zuzuordnen und den Teilnehmern die Möglichkeit zu geben, ihre Präferenzen zu den Themen / Gruppen abzugeben.

Eine Verteilung wird dabei beschrieben durch eine Reihe von Eigenschaften:

- **Name**: Jede Verteilung braucht einen Namen, um sie später identifizieren zu können, wenn die Verteilung ausgewertet werden soll
- **Gruppenliste**: Die Liste der Gruppen / Themen, zu denen Präferenzen angegeben werden sollen
- **# / Gruppe**: Diese Eigenschaft gibt an, wie viele Teilnehmer auf eine Gruppe kommen dürfen. Beispeil: Ist *# / Gruppe = 1*, so darf nur ein Teilnehmer auf jede Gruppe verteilt werden, eine 1:1 Beziehung. Ist *# / Gruppe = n*, mit n > 1, handelt es sich um eine 1:n Beziehung, wobei nur dann jede Gruppe voll ist, wenn es genau ```längeDerGruppeliste * # / Gruppe``` Teilnehmer gibt.
- **Mindeststimmen**: Gibt an, wie viele Präferenzen jeder Teilnehmer mindestens vergeben muss. Dabei ist der Wert nach unten bis 1 und nach oben bis 10 bzw. Anzahl der Themen beschränkt (je nach dem, was zuerst eintritt).
- **Veto erlaubt**: Wenn der Haken gesetzt ist darf ein Teilnehmer eine der angebotenen Themen / Gruppen vollkommen ausgeschließen.
- **geschützt**: Ist diese Option angewählt muss sich jeder Teilnehmer mit seiner Matrikelnummer gegenüber dem System authentifizieren, bevor er seine Präferenzen angeben darf. Ist die Option nicht ausgewählt fallen die beiden nächsten Optionen weg.
- **Teilnehmerliste**: Soll die Verteilung geschützt sein muss im Vorhinein feststehen, welche Teilnehmer teilnehmen werden. Über diese Option wird diese Teilnehmerliste ausgewählt.
- **editierbar**: Diese Option gibt an, ob Teilnehmer nach dem ersten Bestätigen ihrer Präferenzen ihre Angabe erneut anpassen dürfen. Diese Funktion gilt für alle Teilnehmer und unbegrenzt.

Mit dem Auswählen des *Erstellen*-Knopfes wird die Verteilung erstellt und der Benutzer wird auf eine Seite weitergeleitet, auf welcher die Verteilung geteilt werden kann.

## Verteilung teilen

*Dieser Seitenabschnitt steht nur authentifizierten Benutzern zur Verfügung.*

Auf dieser Seite kann eine erstellte Verteilung geteilt werden. Zu diesem Zweck wird der Link angezeigt, welcher benötigt wird, um zu der Verteilung zu navigieren. Darunter ist ein QR-Code, welcher von den Teilnehmern gescannt werden kann, er führt ebenfalls zur Präferenzvergabe.

## Daten anlegen

*Dieser Seitenabschnitt steht nur authentifizierten Benutzern zur Verfügung.*

Um eine Verteilung aus Datenbankdaten erstellen zu können, müssen diese im Voraus angelegt werden. Diese Funktionalität bildet der Unterpunkt *Daten anlegen* (```/upload```).

Die App arbeitet mit zwei Arten von Daten: Teilnehmer und Gruppen bzw. Themen. Beide lassen sich über einen Datei-Upload oder per Formular erstellen.

### Erstellung mittels Formular

Liegen die Daten nicht als Dateien vor, ist die Erstellung mittels Formular eine effiziente und angenehme Art, dies zu ändern. Hierzu muss vor der eigentlichen Erstellen zunächst festgelegt werden, wie viele Teilnehmer oder Gruppen / Themen angelegt werden sollen:

![image](images/manual_creation.png)

Es müssen mindestens 1 ein Teilnehmer oder Gruppe angelegt werden. Nach oben gibt es keine Beschränkung.

An Verteilungen können immer nur ganze Gruppen von Teilnehmern teilnehmen. Es gibt **nicht** die Möglichkeit, nach der Erstellung einer Gruppen- oder Teilnehmerliste die dazugehörigen Gruppen oder Teilnehmer zu bearbeiten, d.h. die Daten zu bearbeiten oder Einträge zu löschen / hinzuzufügen. Diese Listen sind erst zu erstellen, wenn alle Einträge feststehen.

Bei der Erstellung von Teilnehmern oder Gruppen / Themen gibt es Informationen, die ausgefüllt werden müssen, während andere optional sind. Der Name der Teilnehmer- bzw. Gruppenliste ist immer erforderlich, die Notwendigkeit der weiteren Feldern ist den Tabellen zu entnehmen:

#### Teilnehmer

| Feld 			| benötigt	|
|---------------|-----------|
| Vorname		| Ja		|
| Nachname		| Nein		|
| Matrikelnummer| Ja 		|

#### Gruppen / Themen

| Feld 		| benötigt	|
|-----------|-----------|
| Name		| Ja		|
| Uhrzeit	| Nein		|
| Betreuer	| Nein 		|

Sind die benötigten Felder nicht ausgefüllt lässt sich die Verteilung nicht erstellen.

Wenn die Erstellung erfolgreich war, wird der Benutzer zur vorherigen Seite zurückgeleitet und es erscheint ein kleines Banner, welches Auskunft über die Anzahl der erstellen Einträge gibt.

Erstellte Daten können unter [*Angelegte Daten*](#angelegte-daten) betrachtet und bearbeitet werden.

### Erstellung mittels Datei

## Angelegte Daten

## Präferenzvergabe


Wird bei der Präferenzvergabe eine der Antwortmöglichkeiten (z.B. Erstwahl) für eine der Themen angegeben, verschwindet diese Möglichkeit aus den Antwortmöglichkeiten der anderen Themen. Darüber hinaus