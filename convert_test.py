import re
from sys import argv, stderr

def main(filename):
    content = get_content(filename)

    redner = '-'
    rede_id = '-'
    rede = []
    datum = '-'
    print_text = ''

    for i, line in enumerate(content):
        line = re.sub('[\s]+', ' ', line)

        # Sitzung-Datum extrahieren
        if re.search('sitzung-datum', line):
            datum = re.sub('.*sitzung-datum="([^"]+)".*', r'\1', line)

        # Redner. Format: </redner>Helmut Kleebank (SPD):</p>
        if re.search('</redner>', line):
            redner = re.sub('.*/redner>([^<]+).*', r'\1', line).strip()
            redner = re.sub(':', '', redner).strip()

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
                print_text += f'\n{rede_id}\t{datum}\t{redner}\t{gesamte_rede}'
            rede_id = re.sub('.*rede id="([^"]+)".*', r'\1', line)
            rede = []

        # Sitzung Ende
        if re.search('<sitzungsende', line):
            break

    # Letzte Rede hinzufügen
    if rede_id != '-':
        gesamte_rede = ' ## '.join(rede)
        print_text += f'\n{rede_id}\t{datum}\t{redner}\t{gesamte_rede}'

    print(print_text)

def get_content(filename):
    with open(filename, "r", encoding="utf-8") as file_content:
        return [line.strip() for line in file_content.readlines()]

if __name__ == '__main__':
    if len(argv) == 2:
        main(argv[1])
    else:
        stderr.write("Error: Wrong number of arguments.\n")