# WebAuthn Level 3, Passkeys & Account Recovery

## Konu anlatımı
WebAuthn, Relying Party'ye scoped public-key credentials ile challenge-response authentication sağlar. Private key authenticator'da kalır; RP public key ile assertion imzasını doğrular. W3C WebAuthn Level 3, 25 Ağustos 2026'da Recommendation oldu. Passkey güvenliği değerlendirilirken recovery ve fallback kanalları primary authentication kadar güçlü tasarlanmalıdır.

## Mental model
```text
RP challenge -> authenticator signs -> RP verifies
                   ^
             RP/origin scoped
security floor = min(primary, recovery, fallback)
```

## Mülakat soruları
- WebAuthn password'tan nasıl ayrılır?
- RP binding phishing resistance'a nasıl katkı verir?
- Synced/device-bound passkey farkı nedir?
- UP ve UV nasıl ayrılır?
- Attestation ne sağlar?
- Recovery neden threat model'in parçasıdır?

## Beklenen cevap seviyesi
Mid public-key challenge-response; Senior authenticator/UV/recovery; Staff/CTO assurance tiers, enterprise policy, migration ve support fraud riskini bağlamalıdır.

## Mini alıştırma
Password+SMS SaaS için passkey enrollment, lost-device recovery ve high-risk re-auth akışını çiz.

## Proje fikri
WebAuthn RP demosu kur ve phishing proxy, lost device, stolen session ve recovery senaryolarını threat-model et.

## Production bağlantısı
Zayıf password/SMS/help-desk fallback güçlü passkey primary auth'u bypass edebilir. Session security ve recovery governance ayrı kontrol alanlarıdır.

## Kaynaklar
- https://www.w3.org/TR/2026/REC-webauthn-3-20260825/
- https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/
- https://fidoalliance.org/passkeys/
