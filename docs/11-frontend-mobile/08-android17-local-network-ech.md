# Android 17 Local Network Permission & Encrypted Client Hello

Android 17 / API 37 hedefleyen uygulamalarda LAN erişimi `ACCESS_LOCAL_NETWORK` runtime permission ile korunur. Uygulama, uygun senaryoda sistem aracılı privacy-preserving picker kullanarak doğrudan geniş LAN capability istemekten kaçınabilir.

Android 17 ayrıca destekleyen networking stack ve server kombinasyonlarında TLS Encrypted Client Hello kullanır. ECH, ClientHello içindeki hostname/SNI metadata'sının görünürlüğünü azaltır; hedef IP veya tüm DNS metadata'sını tek başına görünmez yapmaz.

```text
App -> capability policy -> LAN
App -> HTTPS/TLS -> ECH negotiation -> Internet
```

## Threat model
LAN permission local discovery/connect capability'sini kullanıcı kontrolüne taşır. ECH farklı bir problem olan passive network metadata observation'ı azaltır. Bu iki kontrol birbirinin yerine geçmez.

## Migration
Target SDK yükseltmeden önce discovery, picker/permission, denial, reconnect ve networking-library ECH support yolları test edilmelidir. Permission denial ile gerçek network timeout/error sınıfları ayrılmalıdır.

## Mülakat derinliği
Junior: runtime permission ve TLS. Mid: discovery/fallback. Senior: threat model ve telemetry. Staff: rollout/OEM-network variance. Principal/CTO: privacy, compatibility ve product impact.

## Failure modes
Context olmadan permission istemek; denial ile network failure'ı karıştırmak; ECH'nin IP/DNS'i tamamen gizlediğini varsaymak; library/server support kontrol etmemek; privacy telemetry'sinde gereksiz identifier toplamak.

## Kaynaklar
- https://developer.android.com/about/versions/17/behavior-changes-17
- https://developer.android.com/about/versions/17
