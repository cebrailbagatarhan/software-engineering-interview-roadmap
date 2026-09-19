# HTTP Message Signatures, Digest Fields & Replay-Safe Verification

## Neden önemli?
TLS kanal güvenliği sağlar; RFC 9421 ise seçilmiş HTTP semantik bileşenlerini application-layer signature contract'ına bağlar. Webhook, gateway ve cross-domain API tasarımlarında interview açısından asıl konu kriptografi primitive'inden çok coverage, canonicalization, replay ve key lifecycle reasoning'idir.

## Mental model
```mermaid
flowchart LR
 C[Client] --> D[Content-Digest]
 D --> B[Signature base]
 M[@method / @authority / @target-uri] --> B
 B --> S[Signature-Input + Signature]
 S --> V[Verifier policy]
 V --> A[Application]
```
**Invariant:** signature yalnız covered components'i kanıtlar; verifier signer trust, coverage ve freshness policy'sini ayrıca enforce eder.

## Temel kavramlar
- RFC 9421 raw bytes yerine HTTP components'ten deterministic signature base kurar.
- `Signature-Input` covered components ve metadata'yı; `Signature` cryptographic value'yu taşır.
- `created` önerilir; `expires`, maximum age ve clock skew uygulama policy'sidir.
- RFC 9530 `Content-Digest` message content, `Repr-Digest` representation data integrity'sini tanımlar.
- Digest authentication değildir; body integrity için digest alanını signature coverage'a almak güçlü bir pattern'dir.
- HTTP signatures TLS confidentiality/transport security'nin yerine geçmez.

## Replay-safe verifier checklist
1. Beklenen signature label/tag/signer var mı?
2. Key id trusted ve algorithm policy'ye uygun mu?
3. Zorunlu components gerçekten covered mı?
4. Signature cryptographically valid mi?
5. `created`/`expires` ve local max-age/skew policy geçiyor mu?
6. Nonce/idempotency identifier daha önce tüketilmiş mi?
7. Yalnız doğrulanmış/covered alanlar security decision'da kullanılıyor mu?

## Mülakat soruları
1. TLS varken neden HTTP Message Signature kullanırsın?
2. Raw HTTP bytes imzalamak proxy ortamında neden kırılgandır?
3. `Content-Digest` ve `Repr-Digest` farkı nedir?
4. Valid signature neden yine de insecure request olabilir?
5. `created` replay'i neden tek başına çözmez?
6. Senior: webhook coverage profile'ını tasarla.
7. Staff: key rotation ve multi-signer rollout tasarla.
8. Principal: crypto agility, trust domain ve replay-store standardını belirle.

## Seviye beklentisi
- **Mid:** digest/signature/TLS farkını kurar.
- **Senior:** coverage, replay, skew ve key rotation failure mode'larını açıklar.
- **Staff:** gateway policy, rollout, telemetry ve compatibility tasarlar.
- **Principal:** organization-wide signing profile ve key lifecycle standardı kurar.

## Mini alıştırma
`POST /payments/{id}` webhook'u için `Content-Digest`, `@method`, `@authority`, `@target-uri` ve idempotency identifier içeren verifier akışı çiz. 5 dakikalık replay window ve 30 saniyelik skew için reject koşullarını yaz.

## Proje
`http-signature-gateway-lab`: signer + proxy + verifier. Header rewrite, body mutation, expired signature, wrong key, duplicate nonce ve unsigned routing-header fault injection ekle. Verify latency, failure reason, replay hit ve unknown-key metriği üret.

## Failure modes / trade-off / production
Kritik alanı cover etmemek, digest'i authentication sanmak, invalid-signature negative test yapmamak, clock skew'i yok saymak ve replay cache'i limitsiz büyütmek tipik hatalardır. Production'da verify failure reason, signature age/skew, replay detection, unknown key id, algorithm distribution ve p95 verification cost izlenir.

## Kaynaklar
- IETF RFC 9421 — HTTP Message Signatures: https://www.rfc-editor.org/rfc/rfc9421.html
- IETF RFC 9530 — Digest Fields: https://www.rfc-editor.org/rfc/rfc9530.html
