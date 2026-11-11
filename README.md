# Admin Panel & Türkçe Web Wordlist (TR + EN)

Web uygulamalarında admin paneli, dizin, dosya, subdomain ve parametre keşfi için
**Türkçe odaklı** wordlist koleksiyonu. Türk geliştiricilerin gerçekte kullandığı
terimlere dayanır — GitHub'daki global listelerde (SecLists vb.) bu kapsam yok.

## İçerik

| Dosya | Giriş | Açıklama |
|---|---|---|
| `admin-panels.txt` | ~1.6K | Admin/yönetim paneli path'leri (TR + EN, orijinal liste) |
| `turkce/turkce-dizinler.txt` | ~65K | Dizin/klasör isimleri (tek ve iki seviyeli) |
| `turkce/turkce-dosyalar.txt` | ~86K | Dosya + yedek/sızıntı (.php.bak, .env, yedek.sql...) |
| `turkce/turkce-subdomainler.txt` | ~11K | Subdomain (ortam önek/sonekli) |
| `turkce/turkce-kullanicilar.txt` | ~1.2K | Kullanıcı adı denemeleri |
| `turkce/turkce-parametreler.txt` | ~900 | URL parametre isimleri (fuzzing) |
| `turkce/turkce-web-icerik.txt` | ~151K | Dizin + dosya birleşik büyük liste |

Her liste hem küçük hem BÜYÜK harf varyantlarını içerir (`admin` ve `ADMIN`).
Türkçe karakterli (`yönetim`, `şifre`) ve ASCII karşılıkları (`yonetim`, `sifre`) birlikte.

Toplam: **~315.000 benzersiz giriş**.

## Kullanım

```bash
# gobuster — dizin/dosya keşfi
gobuster dir -u https://hedef.com -w turkce/turkce-web-icerik.txt

# ffuf — parametre fuzzing
ffuf -u "https://hedef.com/sayfa?FUZZ=1" -w turkce/turkce-parametreler.txt

# subdomain
ffuf -u "https://FUZZ.hedef.com" -w turkce/turkce-subdomainler.txt
```

## Listeleri büyütme

`turkce/gen_wordlist.py` üreticidir. İçindeki kök kelime havuzuna (`KOKLER`, `ING`)
terim ekleyip çalıştırınca listeler yeniden ve daha büyük üretilir:

```bash
python3 turkce/gen_wordlist.py
```

## Uyarı

Yalnızca **yetkili** olduğunuz sistemlerde ve yasal güvenlik testlerinde kullanın.
İzinsiz tarama yapmak yasa dışıdır.
