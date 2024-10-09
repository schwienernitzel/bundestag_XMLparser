#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Usage: python3 convert_xml.py output.csv
Datum: Okt 2024
Zweck: XML-Dateien (20001.xml bis 20189.xml) einlesen und in einer gemeinsamen CSV-Datei speichern
"""

from sys import argv
from sys import stderr
import re
import os


# Main
def main(output_file):
    # Öffne die Ausgabedatei im Schreibmodus
    with open(output_file, "w", encoding="utf-8") as csv_file:

        # Schreibe die Spaltenüberschriften in die CSV-Datei
        csv_file.write('RedeID\tSitzungsnummer\tRedner\tPartei\tDatum\tRede\n')

        # Iteriere über alle XML-Dateien von 20001.xml bis 20189.xml
        for file_number in range(20001, 20190):
            filename = f"{file_number}.xml"

            # Stelle sicher, dass die Datei existiert, bevor sie verarbeitet wird
            if os.path.exists(filename):
                print(f"Verarbeite Datei: {filename}")
                content = get_content(filename)

                redner = '-'
                partei = '-'
                rede_id = '-'
                rede = []
                datum = '-'
                sitzungsnummer = '-'  # Sitzungsnummer initialisieren

                for i, line in enumerate(content):

                    # Tabulatoren entfernen
                    line = re.sub('[\s]+', ' ', line)

                    # Metadaten in der XML-Datei sammeln:

                    # Datum. Format: sitzung-datum="27.09.2024"
                    if re.search('sitzung-datum', line):
                        datum = re.sub('.*sitzung-datum="([^"]+)".*', r'\1', line)

                    # Sitzungsnummer. Format: <sitzungsnr>3</sitzungsnr>
                    if re.search('<sitzungsnr>', line):
                        sitzungsnummer = re.sub('.*<sitzungsnr>([^<]+)</sitzungsnr>.*', r'\1', line).strip()

                    # Texte. Format: <p klasse="O">Für diese Menschen ist das Ganze eine Rentenkürzung...
                    if re.search('<p', line) and not re.search('<vorname>', line):
                        absatz = re.sub("<[^>]*>", '', line)
                        absatz = absatz.strip()
                        rede.append(absatz)

                    # Redner. Format: </redner>Helmut Kleebank (SPD):</p>
                    if re.search('</redner>', line):
                        redner = re.sub('.*/redner>([^<]+).*', r'\1', line).strip()
                        redner = re.sub(':', '', redner).strip()

                    # Partei. Format: <fraktion>SPD</fraktion>
                    if re.search('<fraktion>.*</fraktion>', line):
                        partei = re.sub('.*<fraktion>(.*)</fraktion>.*', r'\1', line).strip()

                    if re.search('<rolle_kurz>.*</rolle_kurz>', line) and re.search('rede id', content[i - 1]):
                        partei = re.sub('.*<rolle_kurz>(.*)</rolle_kurz>.*', r'\1', line)

                    if re.search("rede id=", line) and rede_id == '-':
                        rede_id = re.sub('.*rede id="([^"]+)".*', r'\1', line)

                    # Abbruchbedingung: Sitzung ist zu Ende
                    if re.search('<sitzungsende', line):
                        # Letzte Rede speichern, falls vorhanden
                        if rede:
                            gesamte_rede = ' ## '.join(rede)
                            csv_file.write(
                                f"{rede_id}\t{sitzungsnummer}\t{redner}\t{partei}\t{datum}\t{gesamte_rede}\n")
                        break  # Beende die Verarbeitung, sobald das Ende der Sitzung erreicht ist

                    # Das Ende einer Rede wurde erreicht.
                    # Entweder, weil die nächste beginnt (neue rede_id),
                    # oder weil am Textende '<sitzungsende' gefunden wird
                    if re.search('rede id', line):
                        gesamte_rede = ' ## '.join(rede)
                        csv_file.write(f"{rede_id}\t{sitzungsnummer}\t{redner}\t{partei}\t{datum}\t{gesamte_rede}\n")

                        # ID der nächsten Rede festhalten
                        redner = '-'
                        rede = []
                        rede_id = re.sub('.*rede id="([^"]+)".*', r'\1', line)

    print(f"Alle Dateien wurden verarbeitet und in {output_file} gespeichert.")


# Datei in Liste
def get_content(filename):
    content = []
    with open(filename, "r", encoding="utf-8") as file_content:
        for line in file_content.readlines():
            line = line.strip()
            content.append(line)
    return content


if __name__ == '__main__':
    if len(argv) == 2:
        main(argv[1])
    else:
        stderr.write("Error: Wrong number of arguments. Please provide the output CSV filename.\n")