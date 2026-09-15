# Kubernetes Gateway API: Roles & Route Attachment

## Konu anlatımı
Gateway API Kubernetes service networking için extensible, role-oriented ve protocol-aware API ailesidir. `GatewayClass` controller/infrastructure sınıfını, `Gateway` listener ve network entry point'i, `HTTPRoute`/`GRPCRoute`/`TCPRoute`/`UDPRoute` ise uygulama routing kurallarını temsil eder.

Temel avantaj ownership separation'dır: platform ekibi shared Gateway'i, uygulama ekipleri kendi Route kaynaklarını yönetebilir. Route'un Gateway'e referans vermesi attachment garantisi değildir; listener `allowedRoutes`, namespace sınırları ve controller status/conditions değerlendirilmelidir.

Gateway API Kubernetes'ten bağımsız sürümlenen bir add-on'dur. v1.6 ile TCPRoute ve UDPRoute Standard channel'a mezun olmuştur. Production'da yalnız API version'a değil controller'ın conformance/feature desteğine bakılmalıdır.

## Mental model
```text
GatewayClass -> Gateway -> listeners
                         ^
                         | allowed attachment
HTTPRoute / GRPCRoute ---+
        |
        v
     Service
```

## Mülakat soruları
- Gateway API neden yalnız yeni Ingress syntax'ı değildir?
- GatewayClass/Gateway/Route ownership'i nasıl ayırır?
- Route attachment neden policy problemidir?
- Shared Gateway multi-tenant riskleri nelerdir?
- Controller conformance neden önemlidir?
- Ingress migration nasıl kademelendirilir?

## Seviye beklentisi
**Mid:** Gateway/Route ilişkisi. **Senior:** listener, attachment, TLS ve controller behavior. **Staff:** multi-team ownership, migration, conformance ve blast radius.

## Mini alıştırma
Platform-owned Gateway ile namespace-owned Route arasında least-privilege attachment policy tasarla.

## Proje fikri
İki namespace için shared Gateway, HTTPRoute, TLS ve weighted-routing laboratuvarı kur.

## Production / failure modes
Accepted/Programmed conditions kontrol edilmeden trafiği hazır varsaymak, controller support'u doğrulamamak, cross-namespace izinleri gevşek bırakmak ve migration'da DNS/TLS/observability parity testini atlamak yaygın hatalardır.

## Kaynaklar
- https://gateway-api.sigs.k8s.io/
- https://kubernetes.io/docs/concepts/services-networking/gateway/
- https://kubernetes.io/blog/2026/08/03/gateway-api-v1-6-release/
