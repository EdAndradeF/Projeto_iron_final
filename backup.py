








def save(aqr, txt):
    caminho = './data/backup/{aqr}.txt'
    with open(fr'data\backup\{aqr}.txt', 'w', encoding="utf-8") as a:
        a.write(txt + '\n')
