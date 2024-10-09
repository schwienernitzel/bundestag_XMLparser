from sys import argv
from sys import stderr
import re

def main(filename):
    content = get_content(filename)

    redner = '-'
    rede_id = '-'
    rede = []
    datum = '-'
    print_text = ''
    rede_aktiv = False
    redner_aktiv = False

    for i, line in enumerate(content):
        line = re.sub('[\s]+', ' ', line)

        if re.search('sitzung-datum', line):
            datum = re.sub('.*sitzung-datum="([^"]+)".*', r'\1', line)

        # Mehrzeilige Rede-Absätze erfassen
        if re.search('<p', line)  and not re.search('<vorname>', line) or rede_aktiv:
            absatz = re.sub("<[^>]*>", '', line).strip()  # Entferne HTML-Tags und bereinige den Text

            if absatz:  # Nur hinzufügen, wenn der Absatz nicht leer ist
                rede.append(absatz)
                rede_aktiv = True  # Weiterhin Rede sammeln

            if re.search('</p>', line):  # Wenn das Ende des Absatzes erreicht ist
                rede_aktiv = False  # Sammeln beenden

        # Rednername sammeln, auch mehrzeilig
        if re.search('</redner>', line) or redner_aktiv:
            if not redner_aktiv:
                # Nur den Text nach dem Redner-Tag erfassen und HTML-Tags entfernen
                redner = re.sub('.*/redner>([^<]*).*', r'\1', line).strip()
                redner_aktiv = True  # Aktivieren des Sammelns mehrzeiliger Namen
            else:
                # Fortsetzen des Redners, nur den Text sammeln und HTML-Tags entfernen
                line = re.sub('<[^>]*>', '', line).strip()  # HTML-Tags wie </p> entfernen
                redner += ' ' + line

            # Überprüfen, ob der Rednername endet
            if ':' in line:
                redner = re.sub(':', '', redner).strip()  # ":" entfernen, um den vollständigen Namen zu haben
                redner_aktiv = False  # Rednersammeln beenden

        if re.search('rede id', line) or re.search('<sitzungsende', line):
            gesamte_rede = ' ## '.join(rede)
            print_text += '\n'+rede_id+'\t'+redner+'\t'+datum+'\t'+gesamte_rede
            redner = '-'
            rede = []
            rede_id = re.sub('.*rede id="([^"]+)".*', r'\1', line)

        if re.search('<sitzungsende', line):
            break
        
    print (print_text)
    pass

def get_content(filename):
    content = []
    with open(filename, "r") as file_content:
        for line in file_content.readlines():
            line = line.strip()
            content.append(line)           
    return content

if __name__ == '__main__':
    if len(argv) == 2:
        main(argv[1])
    else:
        stderr.write("Error: Wrong number of arguments.\n")