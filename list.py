command_list=['a','s','r','o','q']
black_list=open('test.txt','r')
bl=len(black_list.readlines())
f=black_list.read()
print(bl)
black_list.close()
z=0
while z==0:
    print('ekle=a','sorgula=s','çıkar=r','liste gör=o','çıkış=q')
    giriş=input()
    if giriş=='a':
            a=input('eklemek istediğiniz kişiyi yazın:')
            black_list=open('test.txt','a')
            black_list.write('\n')
            black_list.write(a)
            print('_________________\n\n---->kişi listeye başarıyla eklendi.')
            print('eklenen:',a)
            print('_________________')
            black_list.close()
            print('çıkmak için:q')
            if a=='q':
                black_list.close()
                break
    if giriş=='s':
            ss=input('sorgulamak istediğiniz kişiyi yazın:')
            black_list=open('test.txt','r')
            removed=open('removed.txt','r')

            if ss in removed and black_list :
                print('\n---->kişi listeye alınmış daha sonra silinmiş\n')
            else:
                if ss in black_list:
                    print('_________________\n\n---->kişi listede\n_________________\n\n')
                    print('çıkmak için:q')
                else:
                    print('\n---->kişi listede değil\n'
                          '---->doğru yazdığınızdan emin olun ve tekrar sorgulayın\n')
                    print('çıkmak için:q')

    if giriş=='r':
            r=input('silmekk istediğiniz kişiyi yazın:')
            removed=open('removed.txt','a')
            removed.write('\n')
            removed.write(r)
            removed.close()
            print('_________________\n\n---->kişi silindi.')
            print('---->silinen:',r)

    if giriş=='o':
        print('---->kara liste')
        black_list=open('test.txt','r')
        removed=open('removed.txt','r')
        f=black_list.read()
        r=removed.read()
        print(f)
        print('\n')
        print('---->aşağıdaki kişiler listeden kaldırıldı')
        print(r)
        print('\n')
        removed.close()
        black_list.close()
        
    if giriş=='q':
        print('_________________\n\nçıkılıyor...\n'
              'uygulama kapatıldı.\n_________________')
        break
    if giriş not in command_list:
        print('hatalı komut')        


#eklenecekler
#dosya konumu için farklı yol üzerinden açma butonları eklenecek.

            

