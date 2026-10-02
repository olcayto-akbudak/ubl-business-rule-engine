# Tasarım kararları

## Alan motorunu CLI'dan ayırmak

`run(config)` orkestrasyonu kaynak kodun doğrudan test edilebilmesini sağlar. JSON arayüz taşınabilirliği artırır; bu sürüm kullanıcı arayüzü barındırmaz.

## Seçilen yöntem

Namespace, Decimal, tutar ve vergi tutarlılığı. Basitleştirilmiş pozitif fatura profili, satır iskonto/masrafı ve tek para birimi kullanılır.

## Bilinçli sınır

GİB uygunluk sertifikası veya tam XSD/Schematron doğrulaması değildir; tevkifat, döviz ve özel vergi profilleri ayrıca gerekir.

## Önerilen sonraki doğrulama

Gerçek kullanım hacmiyle testten önce mevcut kabul ve ret örneklerinin alan uzmanı tarafından onaylanması gerekir. Sonraki sürüm performans ölçümleri, dış adaptör sözleşmesi ve üretim gözlemlenebilirliğini ayrı karar kayıtlarında ele almalıdır.
