# Admin Panel Wordlist

Web uygulamalarında admin / yönetim paneli keşfi için derlenmiş path wordlist'i.
Türkçe yönetim terimleri ile yaygın İngilizce admin path'lerinin birleştirilmiş ve tekilleştirilmiş halidir.

- **Toplam giriş:** 1615 (benzersiz)
- **Dosya:** `admin-panels.txt`

## Kullanım

```bash
# gobuster
gobuster dir -u https://hedef.com -w admin-panels.txt

# ffuf
ffuf -u https://hedef.com/FUZZ -w admin-panels.txt
```

## Uyarı

Yalnızca **yetkili** olduğunuz sistemlerde ve yasal güvenlik testlerinde kullanın.
İzinsiz tarama yapmak yasa dışıdır.
