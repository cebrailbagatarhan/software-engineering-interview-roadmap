# WebTransport over HTTP/3: Streams, Datagrams & Delivery Semantics

## Mental model
WebTransport tek ordered connection abstraction'ından ziyade aynı HTTP/3/QUIC connection üzerinde farklı delivery semantics seçmeye izin veren bir toolbox'tır.

```text
Browser
  +-- reliable bidi stream ----> control/chat
  +-- reliable uni stream -----> file/event feed
  +-- unreliable datagrams ----> cursor/telemetry
  |
 HTTP/3 / QUIC
```

Reliable stream retransmission ve stream-içi ordering sağlar. Datagram düşük latency uğruna kaybı kabul edebilir. Bağımsız stream'ler application-level head-of-line coupling'i azaltır; fakat congestion, backpressure ve application semantics hâlâ tasarlanmalıdır.

## Interview katmanları
- Junior: reliable/unreliable, ordering.
- Mid: streams, datagrams ve backpressure.
- Senior: QUIC loss/recovery, congestion, connection lifecycle.
- Staff: browser/edge/proxy compatibility, fallback, observability.
- Principal/CTO: reach, UX latency, operational risk ve platform economics.

## Tasarım soruları
WebTransport ile WebSocket abstraction farkı nedir? Hangi mesajlar datagram olmalıdır? QUIC neden tüm head-of-line problemlerini ortadan kaldırmaz? Fallback ne zaman WebSocket/SSE olmalıdır? Connection-level ve stream-level health nasıl ayrılır?

## Failure modes
Her şeyi datagram yapmak; application retry ile congestion'ı büyütmek; backpressure'ı yok saymak; firewall/proxy/browser fallback planlamamak; connection health ile stream health'i karıştırmak.

## Production bağlantısı
Handshake success, RTT, loss, datagram drop, stream reset, buffered bytes, fallback rate ve p95 interaction latency izlenmelidir.

## Mini proje
Collaborative whiteboard: cursor datagram, state snapshot reliable stream. Packet-loss emülasyonunda interaction latency ve state recovery davranışını ölç.

## Kaynaklar
- https://developer.mozilla.org/en-US/docs/Web/API/WebTransport_API
- https://developer.mozilla.org/en-US/docs/Web/API/WebTransport/WebTransport
- https://datatracker.ietf.org/doc/rfc9297/