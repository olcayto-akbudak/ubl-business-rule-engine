# UBL XML İş Kuralı Motoru

**Depo adı:** `ubl-business-rule-engine` · Python 3.12+ · bağımsız çalışır · dış paket gerekmez.

XML okunabilir olsa bile faturanın miktar, para birimi ve toplamlarının çelişmesini saptamak.

## Teknik kapsam

Namespace, Decimal, tutar ve vergi tutarlılığı. Bu depo çalıştırılabilir bir mühendislik laboratuvarıdır. Ağ erişimi, özel hesap veya gerçek müşteri verisi gerektirmez. Örneklerde kasıtlı hatalar da bulunur; BLOCK, REVIEW veya false sonucu bazı senaryolarda beklenen davranıştır.

## Hızlı başlangıç

Depo kökünde:

```bash
python -m unittest -v
python app.py demo
python app.py demo --input scenario.json --output custom-report.json
```

`sample-report.json` gerçekten çalıştırılmış örnek çıktıdır. Yeniden çalıştırma sonucu `report.json` olur. Zamanlama ölçümleri hariç sabit seed ve girdiyle tekrarlanabilir. Kurulum için `pip install` gerekmez.

## Mimari ve kararlar

İşlem hattı: Boyut/DTD koruması → XML ayrıştırma → satır kuralları → toplam kuralları.

Temel varsayım: Basitleştirilmiş pozitif fatura profili, satır iskonto/masrafı ve tek para birimi kullanılır.

Alan motoru ve komut satırı `app.py`, kabul senaryosu `scenario.json`, sınır ve hata testleri `test_core.py` içindedir. Yapılandırma veri sözleşmesi [data-contract.md](data-contract.md), ayrıntılı akış [architecture.md](architecture.md), işletim adımları [runbook.md](runbook.md) içinde açıklanır.

## Doğrulama ve değerlendirme

Testler yalnız örneğin çalışmasını kontrol etmez; projenin davranışına özgü kabul ve ret koşullarını sınar. Örnek senaryoda gözlenen sonuçlar [results.md](results.md) içinde kayıtlıdır. CI Python 3.12/3.13, Ubuntu/Windows için tanımlıdır; yerel doğrulama Python 3.12 üzerinde yapılmıştır. GitHub'da ilk push sonrasında CI ayrıca çalışmalıdır.

## Sınırlar ve üretime geçiş

GİB uygunluk sertifikası veya tam XSD/Schematron doğrulaması değildir; tevkifat, döviz ve özel vergi profilleri ayrıca gerekir.

Bu sürümde otomatik canlı entegrasyon, kullanıcı kimlik doğrulama, izleme altyapısı ve gerçek veriyle performans garantisi yoktur. İş kuralları sentetik kabul senaryolarıyla görünür hale getirilmiştir. Üretime geçmeden örnek sözleşmeyi gerçek alanlarla eşleyin, aşağıdaki deneyleri uygulayın ve sonuçları sürümleyin.

## Zorlaştırma deneyleri

1. Satır iskontosu ve charge tutarlarının sırasını değiştirerek Decimal korunumunu kontrol edin.
2. İade ve tevkifat profillerini ayrı kural grupları halinde tasarlayın.
3. Satır adedi 10.000 olan XML için süre ve bellek ölçün.
4. Resmî XSD/Schematron doğrulamasını ayrı adaptörde sonuçlara ekleyin.

## GitHub'a taşıma

```bash
git init
git add .
git commit -m "Initial working analysis laboratory"
git branch -M main
git remote add origin https://github.com/olcayto-akbudak/ubl-business-rule-engine.git
git push -u origin main
```

Kendi hesabınıza taşırken `olcayto-akbudak` alanını değiştirin. Hesap bilgisi veya erişim anahtarı kaynak koda koymayın. Çalışan kaynak kod, testler ve teknik belgeler bu depoda yayımlanmıştır.

## Depo yerleşimi

GitHub sürümü dosyaları depo kökünde tutar; `app.py` alan motorunu ve CLI girişini içerir. `test_core.py` doğrudan bu modülü test eder. Belgeler ve örnek veriler aynı kökte yer alır.
