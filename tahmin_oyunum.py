import random
sayı=random.randint(1,100)
sınır=10
tahminsayısı=0
liste={0,1,2,3,4,5}
print('______________\n\nMerhaba\n'
      'Bu bir tahmin oyunudur\n'
      '10 hakkınız var\n'
      '\n'
      )
    
while tahminsayısı <sınır:

    tahmin=int(
        input(
        'tahmin?'
        ))
    if tahmin==sayı:
        print(
        '\t\t_____________________________\n'
        f'\t\tI\tSayı:{sayı}\t\tI\n'
        f'\t\tI\tBravo \t\tI\n'
        f'\t\tI______{tahminsayısı}. denemede bildin.'
        '______I')
        break
    elif int(sayı-tahmin) in liste :
        print(
        'Çok yaklaştın , ha gayret'
        '')
        tahminsayısı +=1
    elif tahmin>sayı:
        print(
        'çok oldu , in biraz'
        '')
        tahminsayısı +=1

    elif tahmin<sayı:
        print(
        'çık çık , daha yukarı'
        '')
        tahminsayısı +=1

print('oyun bitti!\n'
      )





