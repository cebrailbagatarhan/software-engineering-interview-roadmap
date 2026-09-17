# HTTP 103 Early Hints, Preload & Speculative Latency Reduction

## Konu anlatımı
HTTP `103 Early Hints`, origin final response'u üretirken istemciye bazı header alanlarını erkenden ileten informational response'dur. RFC 8297'nin temel örneği `Link: ...; rel=preload`: istemci final `200` ve HTML'i beklerken kritik resource fetch'ini başlatabilir.

103 final response değildir. Hint'ler yalnız performance optimization amacıyla değerlendirilir; final response semantics'inin yerine geçmez. Kazanç, server think time ile kritik resource fetch'inin overlap edilmesinden gelir.

## Mental model
```text
without 103:
request -> [server think] -> 200/HTML -> [critical resource] -> render

with 103:
request -> 103 preload -> [critical resource]
          [server think] -> 200/HTML -> render
```

## İçeride ne oluyor?
Origin, final response hazır olmadan önce muhtemel kritik `Link` header'larını yollar. Browser desteklediği hint'leri spekülatif değerlendirir. CDN/proxy zinciri informational response'u doğru taşımalıdır. Yanlış preload bandwidth contention ve unused work yaratabilir.

## Mülakat soruları
- 1xx informational response nedir?
- 103 ile 200 arasındaki fark nedir?
- `preload` ve normal HTML discovery nasıl ayrılır?
- Early Hints hangi critical-path bölümünü azaltır?
- Yanlış preload neden performansı kötüleştirebilir?
- Senior: CDN/proxy/browser zincirinde rollout'u nasıl ölçersin?
- Staff: RUM ile gerçek kullanıcı faydasını nasıl kanıtlarsın?

## Beklenen cevap seviyesi
Junior: HTTP request/response ve preload. Mid: critical path ve speculative fetch. Senior: CDN/cache, bandwidth contention ve measurement. Staff: compatibility, rollout ve RUM. Principal/CTO: latency-to-business KPI ve complexity economics.

## Mini alıştırma
Server think time 400 ms, kritik CSS fetch'i 180 ms. İdeal overlap altında teorik critical-path kazancını hesapla; gerçek kazancı azaltacak üç faktör yaz.

## Proje fikri
`early-hints-lab`: 103 kapalı/açık iki endpoint; yapay server delay, waterfall, LCP, transfer bytes ve unused preload ölçümü. Bir CDN/proxy katmanından da geçir.

## Failure modes / trade-off / production
Her asset'i preload etmek; final semantics'i 103'e bağlamak; intermediary desteğini varsaymak; bandwidth-constrained kullanıcıları unutmak. Production'da LCP/TTFB, resource start time, unused preload, bytes, browser/CDN breakdown ve task success izlenmelidir.

## Kaynaklar
- https://www.rfc-editor.org/rfc/rfc8297
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/103
