#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Turkce pentest wordlist uretici - kok havuz + sistematik turetme."""
import os, sys

OUT = os.path.expanduser("~/Desktop/turkce-wordlists")
os.makedirs(OUT, exist_ok=True)

# ---- GENIS TURKCE KOK HAVUZU (web gelistiricilerin gercekte kullandigi terimler) ----
KOKLER = """
yonetim yonetici admin panel kontrol gosterge konsol dashboard
uye uyelik kullanici musteri bayi abone ziyaretci personel calisan
yukle yukleme indir dosya belge evrak resim gorsel foto fotograf medya galeri video ses
yedek arsiv eski gecici gizli ozel sistem ayar yapilandirma kurulum bakim
giris cikis kayit oturum hesap profil sifre parola kimlik dogrulama yetki rol izin
sepet siparis odeme fatura tahsilat kasa muhasebe finans gelir gider butce
rapor istatistik analiz ozet grafik tablo liste kayitlar gunluk log
haber duyuru makale yazi blog icerik sayfa menu kategori etiket marka urun stok depo
yorum mesaj bildirim eposta posta iletisim sohbet forum destek yardim talep sikayet
kampanya indirim firsat promosyon kupon hediye puan odul referans davet
tema sablon tasarim modul eklenti bilesen arac widget secenek tercih
api servis entegrasyon baglanti veritabani veri sorgu islem kuyruk onbellek
guvenlik sertifika lisans anahtar jeton cerez izleme denetim
egitim akademi kurs ders sinav soru cevap katilimci ogrenci ogretmen
etkinlik takvim randevu rezervasyon bilet koltuk salon program plan gorev proje
sehir bolge ulke adres konum harita magaza sube lokasyon
sozlesme gizlilik politika kosul hukuk yasal hakkimizda kurumsal
gecmis durum takip kargo teslimat iade degisim garanti onarim
anket oylama form basvuru katilim abonelik
""".split()

# Cok kelimeli yaygin dizinler (tire ve alt cizgi varyantli)
BILESIK = [
    ("yonetim","paneli"), ("kontrol","paneli"), ("admin","panel"),
    ("uye","girisi"), ("uye","islemleri"), ("musteri","hizmetleri"),
    ("insan","kaynaklari"), ("teknik","destek"), ("canli","destek"),
    ("sifremi","unuttum"), ("yeni","kayit"), ("eski","site"),
    ("mobil","uygulama"), ("api","anahtari"), ("veri","tabani"),
]

EKLENTILER = ["php","asp","aspx","html","htm","jsp","do","action","cgi","pl","py","json"]
# Gercek sayfa uzantilari (aktif dosyalar)
SAYFA_UZANTI = ["php","asp","aspx","html","htm","jsp","cgi"]
# Yedek/arsiv/sizinti olarak gorulen duz uzantilar
ARSIV_UZANTI = ["sql","zip","rar","tar.gz","7z","bak","old","txt","log","xml","json","ini","conf","inc"]
# Kaynak dosyaya eklenen yedek/sizinti sonekleri (sadece sayfa uzantilari icin)
YEDEK_SONEK = [".bak", ".old", "~", ".save", ".orig", ".swp", ".yedek", ".backup"]

# ---- Turk sitelerinin de yaygin kullandigi INGILIZCE dev terimleri ----
ING = """admin administrator login logout signin signout dashboard panel control console
user users member members customer customers client clients account accounts profile profiles
upload uploads download downloads file files document documents image images img photo photos
media gallery galleries video videos audio assets static public private secure manage manager
settings config configuration setup install backup backups archive old temp tmp cache data
database db sql query report reports log logs access error stats statistics analytics
order orders payment payments invoice invoices cart checkout product products category categories
news blog posts post article articles comment comments message messages notification notifications
api apiv1 apiv2 rest graphql service services webhook callback auth oauth token session cookie
test testing dev develop development staging demo beta prod production live sandbox
mail email smtp newsletter subscribe support help faq contact about terms privacy
module modules plugin plugins component components widget theme themes template templates
search index home main dashboard monitor health status ping version info debug trace""".split()

def tr_ascii(s):
    tbl = str.maketrans("çğıöşüÇĞİÖŞÜ","cgiosuCGIOSU")
    return s.translate(tbl)

ONEK = ["eski-","yeni-","test-","dev-","v1-","v2-","alt-","ust-","ana-","yedek-","gizli-","ozel-"]
SONEK = ["1","2","3","01","02","2023","2024","2025","2026","_v1","_v2","_eski","_yeni","_yedek",
         "_old","_new","_bak","_test","_dev","-prod","-dev","-test","s","lar","ler","-paneli","-islemleri"]

def varyantlar(k):
    """Bir kok icin yazim/cogul/numara/onek/sonek varyantlari."""
    v = set([k])
    for s in SONEK:
        v.add(k + s)
    for p in ONEK:
        v.add(p + k)
    return v

# Ikinci seviye yol parcalari (yonetim/giris gibi)
EYLEM = """giris cikis login logout ekle sil duzenle guncelle liste listele ara arama kaydet
goruntule detay goster yeni olustur index ayar ayarlar panel yonetim rapor raporlar
onay bekleyenler aktif pasif tumu export import yedek indir yukle onizleme add edit delete
update view new create save list search export import settings profile""".split()
# Iki seviyeli yol uretilecek ust-dizinler
UST_DIZIN = """admin yonetim yonetici panel kontrol uye uyeler kullanici kullanicilar musteri
musteriler bayi bayiler urun urunler siparis siparisler odeme fatura rapor raporlar ayar
sistem dosya resim galeri api modul uygulama hesap profil guvenlik stok kategori icerik
blog haber sayfa menu kampanya personel muhasebe depo kargo user users member order""".split()

dizinler, dosyalar = set(), set()

# Tek seviye: TR kokler + ING terimler, buyuk/kucuk, / varyanti, onek/sonek
TUM_KOK = list(dict.fromkeys(KOKLER + ING))
for k in TUM_KOK:
    for b in [k, k.capitalize(), k.upper()]:
        dizinler.add(b)
        dizinler.add(b + "/")
    for vv in varyantlar(k):
        dizinler.add(vv)
        dizinler.add(vv + "/")

# Dosyalar: her kok icin gercekci uzanti/yedek kaliplari
for k in TUM_KOK:
    for ext in SAYFA_UZANTI:                 # aktif sayfalar: yonetim.php
        dosyalar.add(f"{k}.{ext}")
        for sfx in YEDEK_SONEK:              # kaynak sizintisi: yonetim.php.bak
            dosyalar.add(f"{k}.{ext}{sfx}")
    for ext in ARSIV_UZANTI:                 # yedek/arsiv: yedek.sql, veritabani.zip
        dosyalar.add(f"{k}.{ext}")

# Iki seviyeli yollar: ust-dizin / eylem
for ust in UST_DIZIN:
    for ey in EYLEM:
        dizinler.add(f"{ust}/{ey}")
        dizinler.add(f"{ust}/{ey}/")
        for ext in SAYFA_UZANTI:
            dosyalar.add(f"{ust}/{ey}.{ext}")

for a,b in BILESIK:
    for sep in ["-","_",""]:
        d = f"{a}{sep}{b}"
        dizinler.add(d); dizinler.add(d+"/")
        for ext in EKLENTILER:
            dosyalar.add(f"{d}.{ext}")

# Yaygin hassas/config dosyalari (sabit liste)
HASSAS = """.env .env.local .env.bak .env.prod config.php config.php.bak config.inc.php
ayar.php ayarlar.php database.php db.php baglanti.php connection.php wp-config.php
wp-config.php.bak web.config web.config.bak .htaccess .htpasswd robots.txt sitemap.xml
yedek.sql yedek.zip yedek.rar backup.sql dump.sql veritabani.sql database.sql db.sql
site.zip site.rar www.zip public_html.zip htdocs.zip yedek.tar.gz backup.tar.gz
sifre.txt sifreler.txt parola.txt parolalar.txt kullanicilar.txt admin.txt users.txt
phpinfo.php info.php test.php deneme.php bilgi.php debug.php shell.php cmd.php
error.log hata.log access.log giris.log kayit.log composer.json package.json
.git/config .git/HEAD .svn/entries .DS_Store id_rsa id_rsa.pub .bash_history""".split()
for h in HASSAS:
    dosyalar.add(h)

# Turkce karakterli varyantlar (bazi siteler path'te Turkce karakter kullaniyor)
TR_DIZIN = ["yönetim","üye","üyeler","şifre","şifreler","görsel","görseller","belgeler",
            "düzenle","güncelle","ödeme","öneri","çıkış","giriş","başvuru","çalışanlar",
            "müşteri","müşteriler","sözleşme","gizlilik","iletişim","fatura","galeri"]
for t in TR_DIZIN:
    dizinler.add(t); dizinler.add(t + "/")
    dizinler.add(tr_ascii(t))  # ascii karsiligi da

# ---- SUBDOMAIN ----
SUB_BASE = """www mail webmail posta eposta panel yonetim admin yonetici portal uye uyelik
giris bayi bayiler musteri destek yardim api api2 servis test test2 deneme dev gelistirme
beta staging demo canli eski yeni yeni-site mobil m app uygulama blog haber haberler duyuru
forum magaza shop market alisveris odeme fatura muhasebe finans crm erp intranet iletisim
vpn ftp ftp2 sftp dosya db veritabani sql mysql mssql cpanel plesk webmin whm directadmin
ns1 ns2 ns3 dns smtp pop pop3 imap mx mx1 mx2 cdn static statik resim img gorsel medya
upload yukle download indir arsiv yedek backup egitim akademi kampanya promosyon kurumsal
ik insan-kaynaklari satis raporlar analiz izleme monitor durum status sunucu server proxy
gateway gw vpn2 secure guvenli login giris2 panel2 admin2 yonetim2 eski-panel test-panel
odeme2 pay ödeme api-test dev-api demo-panel staging-api""".split()
subdomainler = set()
for s in SUB_BASE:
    subdomainler.add(s)
    subdomainler.add(tr_ascii(s))
# ortam onek/sonekleri - genis kombinasyon
SUB_ORTAM_PRE = ["dev-","test-","staging-","beta-","eski-","yeni-","demo-","yedek-","canli-",
                 "ic-","dis-","mobil-","web-","yeni","eski","api-","panel-","secure-","vpn-"]
SUB_ORTAM_POST = ["-dev","-test","-staging","-beta","-eski","-yeni","-demo","-prod","-canli",
                  "-api","-panel","-mobil","-web","-secure","-yedek","1","2","3","01","02","-01","-02"]
for s in list(subdomainler):
    for pre in SUB_ORTAM_PRE:
        subdomainler.add(pre+s)
    for post in SUB_ORTAM_POST:
        subdomainler.add(s+post)
# ING terimlerini de subdomain olarak ekle
for s in ING:
    subdomainler.add(s)

# ---- KULLANICI ADLARI ----
KULL = """admin administrator yonetici yonetim root toor kullanici user uye test deneme
misafir guest demo webmaster web site bilgi info iletisim destek support bayi musteri
patron mudur genelmudur sistem sistemyoneticisi operator moderator mod editor yazar
personel calisan muhasebe finans satis pazarlama teknik teknikdestek server sunucu
sysadmin adminuser superadmin yetkili sahibi sefim ahmet mehmet mustafa ayse fatma""".split()
kullanicilar = set()
for u in KULL:
    kullanicilar.add(u)
    for n in ["","1","12","123","1234","2024","2025","2026","!",".","_"]:
        kullanicilar.add(u+n)

# ---- PARAMETRELER ----
PAR = """id sayfa page kategori kat kategori_id urun urun_id uye uye_id kullanici kullanici_id
musteri_id ara arama q sorgu anahtar kelime siparis siparis_id sepet odeme fatura fatura_id
dosya dosya_id resim resim_id img yukle sil duzenle guncelle ekle kaydet islem islem_id
tip tur durum aktif pasif yil ay gun tarih baslangic bitis siralama sira sirala limit sayi
adet fiyat min max minfiyat maxfiyat bolge il ilce sehir ulke dil lang token oturum session
hash kod ref yonlendir url link geri hedef dondur callback redirect next donus sonuc
kullaniciadi parola sifre eposta email telefon tc tckn vergi_no iban hesap_no""".split()
parametreler = set(PAR) | set(tr_ascii(p) for p in PAR)
# parametre varyantlari: _id, _adi, [], vs.
PAR_SONEK = ["", "_id", "_adi", "_no", "_kodu", "_tarihi", "Id", "ID", "[]", "_list", "_sayi"]
PAR_KOK = """urun uye kullanici musteri bayi siparis fatura odeme kategori marka dosya resim
sayfa haber yorum mesaj kampanya il ilce sehir hesap kart sepet islem rapor stok depo
personel sube proje gorev etkinlik kurs ders sinav""".split()
for p in PAR_KOK:
    for sfx in PAR_SONEK:
        parametreler.add(p+sfx)
# ING parametreleri
for p in """id page limit offset sort order filter search q query type status date start end
user_id product_id order_id category_id token key hash ref callback redirect url next lang
format fields include exclude count size price min max active""".split():
    parametreler.add(p)

def yaz(ad, kume, baslik=True):
    yol = os.path.join(OUT, ad)
    satirlar = sorted(x for x in kume if x.strip())
    with open(yol, "w", encoding="utf-8") as f:
        f.write("\n".join(satirlar) + "\n")
    return len(satirlar)

sonuc = {}
sonuc["turkce-dizinler.txt"]     = yaz("turkce-dizinler.txt", dizinler)
sonuc["turkce-dosyalar.txt"]     = yaz("turkce-dosyalar.txt", dosyalar)
sonuc["turkce-subdomainler.txt"] = yaz("turkce-subdomainler.txt", subdomainler)
sonuc["turkce-kullanicilar.txt"] = yaz("turkce-kullanicilar.txt", kullanicilar)
sonuc["turkce-parametreler.txt"] = yaz("turkce-parametreler.txt", parametreler)

# Birlesik buyuk liste (dizin + dosya)
hepsi = dizinler | dosyalar
sonuc["turkce-web-icerik.txt"]   = yaz("turkce-web-icerik.txt", hepsi)

toplam = 0
for k,v in sonuc.items():
    print(f"{v:>7}  {k}")
    toplam += v
print(f"{'='*25}")
print(f"{sum(sonuc.values()):>7}  TOPLAM (dosya bazli)")
