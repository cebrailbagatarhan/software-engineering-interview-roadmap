# WebAuthn, Passkeys & Replay Resistance

## Neden var?
WebAuthn güçlü authentication için RP-scoped public-key credentials kullanır. Private key authenticator'da kalır; relying party doğrulama için public key/credential kaydı tutar.

## Registration ve authentication
Registration'da RP taze challenge/options üretir, authenticator credential oluşturur ve RP doğrulanabilir credential bilgisini kaydeder. Authentication'da RP yeni challenge üretir; authenticator assertion imzalar; RP challenge, RP/origin bağlamı ve signature gibi kontrolleri uygular.

```text
RP -- fresh challenge --> authenticator
RP <-- signed assertion --+
 | verify context + signature
 v
session / deny
```

Challenge server-side güvenilir ortamda rastgele üretilmeli ve replay'i önleyecek şekilde tek ceremony ile ilişkilendirilmelidir.

## Passkey lifecycle
Passkey discoverable WebAuthn credential'dır. Production tasarımında enrollment, multiple credentials, revocation, recovery, synced/device-bound özellikleri ve fallback kanalları birlikte ele alınır. Recovery akışı ana authentication'dan belirgin biçimde zayıfsa saldırgan güçlü login'i bypass edebilir.

## Mülakat derinliği
Senior aday protocol flow ve validation'ı; Staff aday credential lifecycle, assurance, recovery ve migration blast radius'unu; Principal/CTO ise organization-wide authentication policy ve risk modelini tartışmalıdır.

## Failure modes
Challenge reuse/düşük entropy, origin/RP validation hatası, zayıf recovery, tek credential lockout, gereksiz authenticator fingerprinting ve migration boyunca korunmuş zayıf password fallback.

## Kaynaklar
- https://www.w3.org/TR/webauthn-3/
- https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/
