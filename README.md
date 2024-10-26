# HamelnHack 2024 - Phoenix Contact

Test: `python3 -m coverage run -m unittest`
HTML: `python3 -m coverage html`

## Behälter

|                                   | Hochbehälter 1 | Hochbehälter 2 |
| --------------------------------- | -------------- | -------------- |
| Auflösung                         | 15 min         | 15 min         |
| Volumen [m³]                      | 540            | 154            |
| Leistungsaufnahme [kW]            | 20             | 15             |
| Energieverbrauch pro Stunde [kWh] | 20             | 15             |
| Förderleistung [l/s]              | 16.5           | 11.2           |

Randbedingungen:

- Der Hochbehälter muss immer zu mind. 10 % gefüllt sein.
- Eine Pumpe läuft mind. 15 Minuten am Stück.
- Am Anfang der Zeitverläufe ist der Hochbehälter zu 50% gefüllt.
- Am Ende der Zeitverläufe ist der Hochbehälter zu 50% gefüllt.

## PV

|                              | Stromerzeugung PV-Anlage 1 |
| ---------------------------- | -------------------------- |
| Auflösung                    | 5 min                      |
| Nennleistung [kWp]           | 24.86                      |
| Maximale Leistung April [kW] | 21.69                      |
