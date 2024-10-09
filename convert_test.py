import re
from sys import argv, stderr

def main(filename):
    content = get_content(filename)

    redner = '-'
    partei = '-'
    rede_id = '-'
    rede = []
    datum = '-'
    print_text = ''

    for i, line in enumerate(content):
        line = re.sub('[\s]+', ' ', line)

        # Sitzung-Datum extrahieren
        if re.search('sitzung-datum', line):
            datum = re.sub('.*sitzung-datum="([^"]+)".*', r'\1', line)

        # Rednername extrahieren
        if re.search('<redner id=', line):
            # Suche nach Vorname, Nachname und evtl. Titel
            vorname = '-'
            nachname = '-'
            titel = ''

            # Schleife durch die nächsten Zeilen, um Vorname, Nachname und Titel zu finden
            j = i + 1
            while j < len(content) and not re.search('</redner>', content[j]):
                if re.search('<vorname>', content[j]):
                    vorname = re.sub('.*<vorname>([^<]+)</vorname>.*', r'\1', content[j])
                if re.search('<nachname>', content[j]):
                    nachname = re.sub('.*<nachname>([^<]+)</nachname>.*', r'\1', content[j])
                if re.search('<titel>', content[j]):
                    titel = re.sub('.*<titel>([^<]+)</titel>.*', r'\1', content[j])
                j += 1

            # Rednername formatieren
            if titel:
                redner = f'{titel} {vorname} {nachname}'
            else:
                redner = f'{vorname} {nachname}'

        # Partei/Fraktion extrahieren
        if re.search('<fraktion>', line):
            partei = re.sub('.*<fraktion>([^<]+)</fraktion>.*', r'\1', line)

        if re.search('<rolle_lang>', line):
            partei = re.sub('.*<rolle_lang>([^<]+)</rolle_lang>.*', r'\1', line)

        # Rede-Absatz extrahieren
        if re.search('<p', line) and not re.search('<redner', line):
            absatz = re.sub("<[^>]*>", '', line)
            absatz = absatz.strip()
            if absatz:
                rede.append(absatz)

        # Rede-ID extrahieren und Rede abschließen
        if re.search("rede id=", line):
            if rede_id != '-':
                gesamte_rede = ' ## '.join(rede)
                print_text += f'\n{rede_id}\t{datum}\t{redner}\t{partei}\t{gesamte_rede}'
            rede_id = re.sub('.*rede id="([^"]+)".*', r'\1', line)
            rede = []

        # Sitzung Ende
        if re.search('<sitzungsende', line):
            break

    # Letzte Rede hinzufügen
    if rede_id != '-':
        gesamte_rede = ' ## '.join(rede)
        print_text += f'\n{rede_id}\t{datum}\t{redner}\t{partei}\t{gesamte_rede}'

    print(print_text)

def get_content(filename):
    with open(filename, "r", encoding="utf-8") as file_content:
        return [line.strip() for line in file_content.readlines()]

if __name__ == '__main__':
    if len(argv) == 2:
        main(argv[1])
    else:
        stderr.write("Error: Wrong number of arguments.\n")