# Undersampling bei Kreditkartenbetrug

Dieses Projekt vergleicht die Ergebnisse einer logistischen Regression ohne Sampling mit Random Undersampling.

Verwendete Kennzahlen: Precision, Recall, F1-Score und Brier Score.

`compare_models.py` visualisiert ausschließlich bereits berechnete Ergebnisse
mithilfe von pandas und matplotlib. Es erzeugt keine synthetischen Daten und
trainiert keine Modelle.

## Installation

Benötigt wird Python 3.12. Im Repository-Verzeichnis:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In der eingerichteten Cloud-Umgebung kann stattdessen die vorhandene Umgebung
mit `source /workspace/undersampling-env/bin/activate` verwendet werden.

## Berechnete Ergebnisse bereitstellen

Speichere die tatsächlichen Kennzahlen in einer UTF-8-Datei `results.csv`.
Die erste Zeile muss lauten:

```csv
model,precision,recall,f1_score,brier_score
```

Darunter gehören genau zwei Zeilen: eine für die logistische Regression ohne
Sampling und eine für Random Undersampling. Verwende diese Modellbezeichnungen
in der Spalte `model`. Alle vier Kennzahlen müssen Dezimalzahlen zwischen 0 und 1
sein, mit Punkt als Dezimaltrennzeichen. Prozentwerte müssen zuvor durch 100
geteilt werden. Die Ergebnisse müssen aus derselben Testgrundlage stammen, damit
der Vergleich aussagekräftig ist. Fehlende, ungültige oder außerhalb des Bereichs
liegende Werte werden abgewiesen.

Die mitgelieferte `results.csv` enthält die vom Nutzer bereits berechneten
Ergebnisse, ohne erneutes Training oder Neuberechnung:

| Modell | Precision | Recall | F1-Score | Brier Score |
| --- | ---: | ---: | ---: | ---: |
| Baseline (ohne Sampling) | 0,8462 | 0,5789 | 0,6875 | 0,000759 |
| Random Undersampling | 0,0659 | 0,8737 | 0,1225 | 0,022348 |

Random Undersampling erzielt einen höheren Recall. Die Baseline erzielt dagegen
eine höhere Precision und einen höheren F1-Score sowie einen niedrigeren Brier
Score. Die zugrunde liegenden Vorhersagen und Testdaten sind nicht enthalten;
die ursprüngliche Berechnung der Kennzahlen wird daher nicht überprüft.

## Diagramme erzeugen

```bash
python compare_models.py results.csv --output-dir plots
```

Das Skript gibt die eingelesenen Kennzahlen aus und speichert vier separate
Diagramme mit 200 dpi:

- `plots/precision.png`
- `plots/recall.png`
- `plots/f1_score.png`
- `plots/brier_score.png`

Bei Precision, Recall und F1-Score sind höhere Werte besser, beim Brier Score
niedrigere Werte. Die Balken zeigen die unveränderten CSV-Werte; nur ihre
Beschriftungen werden für die Anzeige auf sechs signifikante Stellen formatiert.
Die Brier-Score-Achse beginnt bei null und wird an die kleinen Werte angepasst;
die anderen Diagramme zeigen den vollständigen Kennzahlenbereich von 0 bis 1.
Bei erneutem Aufruf werden die gleichnamigen PNG-Dateien überschrieben.
Ein Display oder laufender Webserver ist nicht erforderlich.
