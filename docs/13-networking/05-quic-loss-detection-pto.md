# QUIC Loss Detection, PTO & Congestion Control

## Konu anlatımı
QUIC güvenilirliği UDP üzerinde kurar; retransmission aynı packet number'ı yeniden kullanmaz. Gerekli frame yeni packet number ile tekrar gönderilir. Loss detection packet threshold ve time threshold sinyallerini; liveness için PTO probe'larını kullanır. PTO expiration tek başına loss kanıtı değildir. Congestion control loss/ECN gibi path sinyallerini bytes-in-flight ve congestion window'a bağlar.

## Mental model
```text
packets -> ACK ranges -> threshold loss
                    \-> no progress -> PTO -> probe
loss/ECN -> congestion window
persistent congestion -> minimum window
```

## Mülakat soruları
- QUIC retransmission neden yeni packet number kullanır?
- PTO neden loss declaration değildir?
- Reordering ile loss detection arasında hangi trade-off vardır?
- Loss detection ile congestion control nasıl ayrılır?

## Beklenen cevap seviyesi
Mid: ACK/RTT/loss. Senior: packet-number spaces, threshold loss, PTO ve congestion window. Staff: ECN, reordering, persistent congestion, path migration ve observability.

## Mini alıştırma
#10–#14 gönderildiğinde #14 ACK alıp #11 eksikse packet/time threshold için gereken sinyalleri yaz.

## Proje fikri
Packet send/ACK/loss/reordering event'lerinden RTT, PTO ve congestion-window grafiği üreten simulator.

## Failure modes / production
PTO'yu loss sanmak, reordering'i agresif biçimde loss ilan etmek ve yalnız application latency izlemek. RTT distribution, loss events, PTO count ve bytes-in-flight birlikte gözlenmelidir.

## Kaynaklar
- RFC 9002: https://www.rfc-editor.org/rfc/rfc9002.html
- RFC 9000: https://www.rfc-editor.org/rfc/rfc9000.html
