# SSR, Hydration & Streaming

## Mental model
Server-side rendering ilk HTML'i server'da üretir. Hydration client React'ın bu HTML'e logic ve event davranışını bağlamasıdır.

```text
server React -> HTML -> browser paint
                  +---- JS load/execute -> hydrate -> interactive
```

`hydrateRoot` server ve client başlangıç çıktısının eşleşmesini bekler; mismatch bug olarak ele alınmalıdır. SSR erken görünürlük sağlayabilir fakat JS download/parse/execute ve hydration maliyetini ortadan kaldırmaz.

Streaming server rendering shell ve hazır parçaların daha erken gönderilmesini sağlar. Suspense boundary'leri progressive delivery için kullanılabilir. `renderToString` streaming veya data bekleme desteği sağlamaz; modern stream API'leri farklı latency profili sunar.

## Mülakat derinliği
Mid: CSR/SSR/hydration ayrımı. Senior: mismatch, bundle/hydration cost, Suspense ve streaming. Staff: CDN/cache, server compute, partial failure, telemetry ve rendering boundary'leri.

## Failure modes
Server/client nondeterminism, browser API'lerini server render sırasında çağırmak, SSR'ı otomatik performans zaferi sanmak, aşırı JS ile hydration bottleneck'i ve mismatch telemetry eksikliği.

## Kaynaklar
- https://react.dev/reference/react-dom/client/hydrateRoot
- https://react.dev/reference/react-dom/server
- https://react.dev/reference/react-dom/server/renderToPipeableStream
