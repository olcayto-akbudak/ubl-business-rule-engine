# Girdi ve çıktı sözleşmesi

UTF-8 JSON nesnesi; örnek dosya alanların tam iç içe yapısını gösterir. Zamanlar bu laboratuvarda sayısal sanal zaman/gün değeridir; saat dilimi dönüşümü yapılmaz.

| Üst alan | Tür | Örnek |
|---|---|---|
| `documents` | `list` | [{'id': 'valid', 'xml': '<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonB |

## Semantik

Basitleştirilmiş pozitif fatura profili, satır iskonto/masrafı ve tek para birimi kullanılır.

Alan motorunun doğrulamaları `app.py` içinde açıkça bulunur. Eksik zorunlu anahtarlar hata verir. Satır bazında karantina/bulgu üreten motorlar rapora yazar; yapısal konfigürasyon hataları işlemi keser. Tam JSON Schema dosyası bu sürümün kapsamında değildir.

## Çıktı

Gerçek çıktı şeması ve örnek değerler `sample-report.json` içinde yer alır. Örnek işleme özgü sonuçlar `results.md` içinde açıklanır. Dış tüketici alan adlarını ve birimleri değiştirmeden sözleşmeyi sürümlemelidir.
