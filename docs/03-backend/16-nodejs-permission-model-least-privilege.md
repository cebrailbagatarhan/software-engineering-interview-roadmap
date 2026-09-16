# Node.js Permission Model, Least Privilege & Sandbox Boundaries

## Konu anlatımı
Node.js Permission Model process içindeki belirli kaynak erişimlerini default-deny yaklaşımıyla sınırlar. `--permission` etkinleştirildiğinde izin verilmeyen erişimler `ERR_ACCESS_DENIED` üretir. Model Stable durumdadır; enforce ve audit modları rollout için farklı araçlar sağlar.

## Mental model
```text
request -> Node process -> permission check -> resource
                         | allow
                         +-------------------->
                         | deny
                         +--> ERR_ACCESS_DENIED

container / OS sandbox = ayrı dış katman
```

## İçeride ne oluyor?
Filesystem izinleri allowlist edilebilir. Audit mode, enforce öncesi gerçek erişim profilini çıkarmak için kullanışlıdır. Permission Model container/OS isolation'ın yerine geçmez ve defense-in-depth gerekir. 29 Temmuz 2026 güvenlik sürümünde permission model bypass'larına yönelik düzeltmeler yayımlandı; patch hygiene güvenlik modelinin parçasıdır.

## Mülakat soruları
- Permission model ile OS/container sandbox farkı nedir?
- Default deny neden önemlidir?
- Audit -> enforce migration nasıl yapılır?
- Path normalization/symlink edge case'leri nelerdir?
- Dependency compromise'da model neyi azaltır?
- Staff: fleet-wide policy standardizasyonu nasıl yapılır?

## Beklenen cevap seviyesi
Junior: least privilege. Mid: resource/path izinleri. Senior: bypass surface ve defense-in-depth. Staff: fleet policy/telemetry. Principal/CTO: supply-chain risk ve developer friction.

## Mini alıştırma
Image worker için minimum read/write allowlist çıkar; audit ve enforce rollout'u tasarla.

## Proje fikri
`node-permission-lab`: permission model + read-only container filesystem + denied-access telemetry.

## Production bağlantısı / failure modes
Wildcard allowlist, permission model'i sandbox sanmak, audit bulgularını temizlemeden enforce etmek ve eski patch seviyesinde kalmak başlıca risklerdir. Denied events, policy drift, patch compliance ve startup failures izlenir.

## Kaynaklar
- https://nodejs.org/api/permissions.html
- https://nodejs.org/en/blog/release/v24.18.1/
- https://nodejs.org/en/blog/vulnerability/july-2026-security-releases
