# Çalıştırılmış kabul sonuçları

Python 3.12.14, sentetik `scenario.json`; yerel test sayısı **8**, tümü başarılı. Ham test günlüğü `test-log.txt`.

valid: geçerli; bad-total: 1 bulgu

Sonuçlar yalnız bu örneğe aittir; üretim doğruluğu veya performans garantisi olarak yorumlanmamalıdır. Ölçülen iş sonucunu kontrol edin; örnek negatif vaka içeriyorsa ret beklenir. Tam çıktı `sample-report.json`.

## Sınanan davranışlar

| Test | Kontrol |
|---|---|
| `test_valid` | valid |
| `test_total` | total |
| `test_dtd` | dtd |
| `test_size` | size |
| `test_namespace` | namespace |
| `test_decimal` | decimal |
| `test_date` | date |
| `test_root_tax` | root tax |

## Gelişmiş deney planı

1. Satır iskontosu ve charge tutarlarının sırasını değiştirerek Decimal korunumunu kontrol edin.
2. İade ve tevkifat profillerini ayrı kural grupları halinde tasarlayın.
3. Satır adedi 10.000 olan XML için süre ve bellek ölçün.
4. Resmî XSD/Schematron doğrulamasını ayrı adaptörde sonuçlara ekleyin.
