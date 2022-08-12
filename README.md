# Prototypische Entwicklung eines Frameworks zur Simulation von Command-and-Control-Kommunikation über Drittanbieter

## Abschlussarbeit zur Erlangung des akademischen Grades: Bachelor of Science an der HTW Berlin

Eingereicht von Jerome Eble

-----

### Abstract

-----

### Grundvorraussetzungen

- Python 3 muss installiert sein
- Folgende Python-Bibliothekten müssen installiert sein
    - discord
    - black
    - declxml
- Ein Discord-Account muss eingerichtet sein
- Git muss installiert sein

-----

### Einrichtung

1. **Klonen des GiHub-Repositories:** Klone dieses Repository in den gewünschten Ordner auf dem lokalen System.

2. **Konfiguration von Discord:** Folgende Konfigurationen müssen vor Anwendung des Systems im Discord Account vorgenommen werden.

  **a.) Erstellung eines Discord-Servers mit beliebigem Namen**

  **b.) Erstellung der Channels:** Erstelle zwei Channels mit beliebigem Namen in dem in Punkt a. erstellten Server.

  **c.) Erstellung der Bots:** 
In der Discord-Anwendung unter "Benutzereinstellungen -> Erweitert" den "Entwicklermodus" aktivieren. In den Anwendungseinstellungen einen neuen Bot mit beliebigem Namen erstellen. Unter „OAuth2 -> URL-Generator“ im Auswahlfenster „Scopes“ „Bot“ anwählen und
unter „Bot Permissions“ „Administrator “auswählen. Dann die generierte URL am
Ende der Seite kopieren. Die kopierte URL aufrufen und den in Schritt a.) erstellten Server auswählen. Die letzten vier Schritte wiederholen um eine weitere Anwendung mit Bot zu erstellen
und diese dem Server hinzuzufügen.

  **d.) Einpflegen der Credentials in das XML-Template:** 
Im geklonten Projekt, die Datei „_discord_template_muster.xml_“ kopieren, einfügen und umbenennen zu „_discord_template.xml_“. Nun im Discord Entwicklerportal den ersten Bot unter der ersten Anwendung auswäh- len, „Reset Token“ auswählen, den erstellen Token kopieren und im XML-Template unter server-token einfügen. Den vorherigen Schritt mit dem zweiten Bot wiederholen und im XML-Template unter client-token einfügen.Nun in den Benutzereinstellungen unter „Mein Account“ auf die drei Punkte neben dem Nutzernamen klicken und ID kopieren. Im XML-Template unter commander-hash einfügen. Im erstellten Server auf die erstellten Channel rechts klicken, „ID kopieren “ auswählen und im XML-Template jeweils in client-channel und server-channel einfügen, dass ein channel als Server-Channel fungiert und der andere als Client-Channel.

3. **Einpflegen Übertragungsparameter**
  - Im XML-Template einen Namen unter *name* vergeben.
  - Eine maximale Übertragungseinheitsgröße unter _max_chunk_size_ eintragen. (Maximal 2000,
Minimal 100.
  - Eine minimale Übertragungseinheitsgröße unter _min_chunk_size_ eintragen. Diese muss mini-
mal 100 betragen und darf nicht größer als die _max_chunk_size_ sein.
  - Unter _payload_percentage_ eine Zahl zwischen 0.1 (entspricht 10%) und 1.0 (entspricht 100%)
eintragen. Diese bestimmt den Anteil der payload and den Übertragungseinheiten.

-----

### Ausführung

1. Zwei Terminals oder Terminal-Tabs öffnen. In beiden in den core-Ordner des Projekts navigieren. Die Dateien discord_agent.py und discord_server.py in je einem Terminal-Tab oder -Fenster ausführen:
> python3 discord_agent.py
> python3 discord_server.py
Das Terminal-Fenster muss „Agent-Bot is ready! “ bzw. „Server-Bot is ready! “ ausgeben.

2. In Discord den erstellten Server auswählen, den im XML-Template als server-token eingefügten Bot auswählen und eine Direktnachricht an diesen mit folgendem Inhalt senden: „.file_transfer {valider Dateipfad} “. Die Datei unter dem mitgesendeten Dateipfad muss sich dabei auf dem System das das discord_agent.py-Skript ausführt befinden.

3. Bei erflogreichem Transfer sollte das Terminal-Fenster in dem der discord_server.py ausgeführt wird eine Erfolgsmeldung ausgeben. Nun sollte im assets/recieved-Ordner die geünschte Datei zu finden sein.

-----
