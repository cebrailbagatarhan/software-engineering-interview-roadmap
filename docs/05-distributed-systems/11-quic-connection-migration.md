# QUIC Connection Migration, Connection IDs & Path Validation

## Konu anlatımı
QUIC connection identity'yi yalnız IP/port tuple'ına bağlamaz. Connection ID (CID), handshake sonrasında network path değişse bile logical connection'ın devam etmesini sağlar. Mobil Wi-Fi → LTE geçişi bunun klasik production örneğidir.

## Mental model
```text
old path + CID A
      |
network change
      v
new path + CID B
      |
PATH_CHALLENGE / PATH_RESPONSE
      v
validated path
```

## İçeride ne oluyor?
Endpoint birden fazla CID sağlayabilir; migration sırasında uygun yeni CID kullanılır ve eskiler retire edilir. Path validation return-routability kontrolü yapar ve amplification riskini azaltır. Migration congestion-control state'ini etkileyebilir. RFC 9002 congestion control'u path-level property olarak ele alır; loss detection packet-number space'lere göre ayrılır. CID havuzu tükenmesi migration/probing'i engelleyebilir.

## Mülakat soruları
- CID neden IP/port tuple'ından ayrıdır?
- Path validation neyi korur?
- NEW_CONNECTION_ID ve RETIRE_CONNECTION_ID ne yapar?
- CID rotation privacy'yi nasıl etkiler?
- Migration congestion control'u neden etkiler?
- Staff: load balancer CID routing nasıl tasarlanır?

## Beklenen cevap seviyesi
Junior: connection/path. Mid: CID ve validation. Senior: migration, NAT, congestion. Staff: routing, lifecycle, privacy. Principal/CTO: UX/reliability ile complexity trade-off'u.

## Mini alıştırma
Wi-Fi'dan LTE'ye geçen client için CID seçimi, path validation ve congestion state adımlarını sırala.

## Proje fikri
QUIC client/server kurup interface değişimiyle migration üret; RTT, loss, PTO ve survival ölç.

## Failure modes / production
CID'ye stable user identity gömmek; validation öncesi amplification; CID exhaustion; per-path telemetry eksikliği. Migration success, validation latency, RTT delta, PTO/loss ve reconnect fallback izlenir.

## Kaynaklar
- RFC 9000: https://www.rfc-editor.org/rfc/rfc9000.html
- RFC 9002: https://www.rfc-editor.org/rfc/rfc9002.html
