import random
import sqlite3 as sql
import csv

# Açılış ekranını txt dosyasına yazdırıyoruz
giris_ekrani = open("giris_ekrani.txt", "w")
giris_ekrani.write("""
-------------------------------------------------------
Bu Oyun İstanbul Sefiri Süleyman Çakıra Aittir
Burada Şansınızı Test Edebilirsiniz
Hatta Biraz Para Bile Kazanabilirsiniz
Oyunları Oynarken Süleyman Çakırın Şu Sözünü Unutmayın:
KİMSE BENDEN ÇALAMAAAZ!!
İyi Oyunlar Dileriz :)
-------------------------------------------------------
""")
giris_ekrani.close()

# Hazırladığımız giriş ekranını okutuyoruz
dosya = open("giris_ekrani.txt", "r")
okuma = dosya.read()
print(okuma)

class UserDatabase:
    def __init__(self):
        self.connection = sql.connect("user.db") # Self Connection ile veri tabanıyla bağlantı oluşturuyoruz 
        self.cursor = self.connection.cursor()
        self.create_table() # Tablo oluşturuyoruz
        self.check_admin() # Adminlik kontrolünü yapıyoruz

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS USERS ( 
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                USERNAME TEXT NOT NULL UNIQUE,
                PASSWORD TEXT NOT NULL,
                ADMIN INTEGER DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS LOGS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                USERNAME TEXT NOT NULL,
                TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ACTION TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def check_admin(self): #Girilen Girdinin admin olup olmadığını kontrol ediyoruz
        admin = self.search_username('cakir') # cakir adında bir kullanıcı olup olmadığını kontrol ediiyoruz
        if not admin: # cakir yok ise
            self.insert_user('cakir', 'istanbul', 1) # cakir kullanicisini admin olarak ekliyoruz

    def insert_user(self, kullanici_adi, sifre, admin=0): #Burada Veritabanına yeni kullanıcı ekliyoruz
        add_command = """INSERT INTO USERS(USERNAME, PASSWORD, ADMIN) VALUES (?, ?, ?)"""
        data = (kullanici_adi, sifre, admin)
        self.cursor.execute(add_command, data)
        self.connection.commit()

    def print_all_users(self):
        self.cursor.execute("""SELECT * FROM USERS""")#Tüm kullanıcıları seçiyor
        users = self.cursor.fetchall()
        for user in users:
            print(user)#Seçtiğimiz tüm kullanıcıları ekrana yazıyor

    def search_username(self, kullanici_adi):
        search_command = """SELECT * FROM USERS WHERE USERNAME = ?"""#Veritabanında kullanıcı adi yani username arrıyoruz
        self.cursor.execute(search_command, (kullanici_adi,))
        user = self.cursor.fetchone()
        return user

    def update_password(self, kullanici_adi, yeni_sifre):
        upd_command = """UPDATE USERS SET PASSWORD = ? WHERE USERNAME = ?"""#Veritabanındaki kullanici adi aldığımız girdi olan kişinin şifresini değiştiriyoruz
        self.cursor.execute(upd_command, (yeni_sifre, kullanici_adi))
        self.connection.commit()

    def delete_user(self, kullanici_adi):
        dlt_command = """DELETE FROM USERS WHERE USERNAME = ?"""#Veritabanındaki kullanici adi aldığımız girdi olan kullanıcıyı siliyoruz
        self.cursor.execute(dlt_command, (kullanici_adi,))
        self.connection.commit()

    def insert_log(self, kullanici_adi, action):
        add_command = """INSERT INTO LOGS(USERNAME, ACTION) VALUES (?, ?)""" #Log kayıtlarını eklemek için veri tabanına LOGS adında yeni bir giriş yapıyoruz
        data = (kullanici_adi, action)
        self.cursor.execute(add_command, data)
        self.connection.commit()

    def view_logs(self):
        self.cursor.execute("SELECT * FROM LOGS")#Üst fonksiyonda oluşturduğumuz logları görüntülemek için kullanıyoruz
        logs = self.cursor.fetchall()

        if logs:
            print("ID\tKullanıcı Adı\tTarih\t\t\tİşlem")
            for log in logs:
                print(f"{log[0]}\t{log[1]}\t{log[2]}\t{log[3]}")
        else:
            print("Log bulunmamaktadır.")

    def yazi_tura(self):
        bozuk_para = ["yazi", "tura"] #İhtimalleri yazdık
        yazi_tura = random.choice(bozuk_para)#Rastgele seçmesini istedik
        print("""
        Tahmininizi Yapın:
        Yazı mı?
        Tura mı?
        !!!SADECE 'yazi' ve 'tura' ŞEKLİNDE TAHMİNDE BULUNABİLİRSİNİZ AKSİ TAKDİRDE SÜREKLİ KAYBEDERSİNİZ!!!
        """)
        tahmin = input().lower()  # Tahmini küçük harfe çevirerek karşılaştırmak için

        if tahmin == yazi_tura:
            print("Tebrikler Kazandınız!") #Eğer seçim ile bilgisayarın tercihi aynı ise kazandınız değil ise kaybettiniz yazmasını sağlıyoruz
        else:
            print("Tekrar Deneyiniz!")

    def admin_menu(self):
        user = self.search_username('cakir')
        if user and user[3] == 1:  #Admin menümüzü oluşturuyoruz
            print("""
            Çakır Abi Hoşgeldin. Senin için ne yapabiliriz?
            1- Kullanıcı Adlarını Listele
            2- Kullanıcı Ekle
            3- Kullanıcı Sil
            4- Şifre Değiştir
            5- Logları Görüntüle (CSV)
            6- Oyun Oyna
            7- Çıkış
            """)

            while True:
                try:#Burada kullanıcıdan bir seçim yapmasını ve bunu sadece sayı ile yapmasını istedik aksi takdirde 159.Satırda uyardık
                    secim = int(input())#Kullanıcıdan girdi aldık ve if ardından elif ve else karar yapıları ile kullanıcıdan aldığımız girdiyi seçtik
                    if secim == 1:
                        self.print_all_users()
                    elif secim == 2:
                        kullanici_adi = input("Yeni kullanıcı adı: ")
                        sifre = input("Yeni şifre: ")
                        self.insert_user(kullanici_adi, sifre)
                        print("Kullanıcı başarıyla eklendi!")
                    elif secim == 3:
                        kullanici_adi = input("Silinecek kullanıcı adı: ")
                        self.delete_user(kullanici_adi)
                        print("Kullanıcı başarıyla silindi!")
                    elif secim == 4:
                        kullanici_adi = input("Şifresi değiştirilecek kullanıcı adı: ")
                        yeni_sifre = input("Yeni şifre: ")
                        self.update_password(kullanici_adi, yeni_sifre)
                        print("Şifre başarıyla güncellendi!")
                    elif secim == 5:
                        self.view_logs()
                        self.insert_log('admin', 'Loglar görüntülendi')
                    elif secim == 6:
                        self.yazi_tura()
                    elif secim == 7:
                        break
                    else:
                        print("Lütfen geçerli bir seçim yapın. Sayıyı numara ile yazın.")
                except ValueError:
                    print("Lütfen geçerli bir seçim yapın. Sayıyı numara ile yazın.")#Eğer kullanıcı sayı dışında bir harf sembol girerse burda uyardık
        else:
            print("Admin yetkisi bulunmamaktadır.")

    def user_menu(self):#Burda ise standart bir kullanıcı için menü oluşturduk
        print("""
        Seçiminizi Yapın:
        1- Oyun Oyna
        2- Çıkış
        """)

        while True:
            try:
                secim = int(input())#Burada kullanıcan Oyuna girmesiini ya da çıkış yapmasını istedik
                if secim == 1:
                    self.yazi_tura() #Oyunumuzu çağırdık
                elif secim == 2:
                    break
                else:
                    print("Lütfen geçerli bir seçim yapın. Sayıyı numara ile yazın.")
            except ValueError:
                print("Lütfen geçerli bir seçim yapın. Sayıyı numara ile yazın.")

    def main_menu(self): #Uygulamanın giriş menüsünü tasarladık 
        print("""
        1. Giriş Yap
        2. Kaydol
        3. Emeği Geçenler
        4. Çıkış
        """)

        while True:
            try:
                secim = int(input())
                if secim == 1:#Eğer kullanıcı giriş yapmayı seçtiyse kullanıcı adı ve şifre aldık  
                    kullanici_adi = input("Kullanıcı adınız: ")
                    sifre = input("Şifreniz: ")
                    user = self.search_username(kullanici_adi)#Bu kullanıcı adını veri tabanında sorgulattık
                    if user and user[2] == sifre:  # şifrenin üçüncü sütun olduğunu varsayarak kontrol yapılıyor
                        print(f"Hoşgeldin, {kullanici_adi}!")
                        self.insert_log(kullanici_adi, 'Giriş yapıldı')
                        if user[3] == 1:
                            self.admin_menu()#Eğer kullanı admin ise admin menüsünü çağırıyoruz
                        else:#Değilse normal menüyü
                            self.user_menu()
                        break
                    else:
                        print("Kullanıcı adı veya şifre hatalı!")
                elif secim == 2:
                    kullanici_adi = input("Yeni kullanıcı adı: ")#Eğer Kullanıcı Kaydolmayı seçtiyse kullanıcı adi ve şifre alıyoruz 
                    sifre = input("Yeni şifre: ")
                    self.insert_user(kullanici_adi, sifre)#Aldığımız kullanıcı adi ve şifrey veritabanımıza ekliyoruz 
                    print("Kullanıcı başarıyla oluşturuldu!")
                elif secim == 3:
                    print("""
                    Emeği geçenler:
                    - Akın Kökçü
                    - Süleyman Çakır
                    - Mehmet Karahanlı
                    - Can Polat
                    """)
                elif secim == 4:
                    print("Çıkış Yaptınız...")
                    break
                else:
                    print("Lütfen geçerli bir seçim yapın. Sayıyı numara ile yazın.")
            except ValueError:
                print("Lütfen geçerli bir seçim yapın. Sayıyı numara ile yazın.")

if __name__ == "__main__":
    user_db = UserDatabase()
    user_db.main_menu()#UserDatabasesinden main menüyü çağırdık
