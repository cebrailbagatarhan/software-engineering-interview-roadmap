# Scroll Anchoring, Dynamic Layout Stability & overflow-anchor

## Neden önemli?
Infinite feed, lazy image, reklam ve yorum gibi içerikler viewport'un üstünde sonradan yer kapladığında layout akışı kullanıcının okuduğu içeriği aşağı iter. Scroll anchoring, scroll container içinde bir anchor node seçip layout değişikliğinin bu node'u ne kadar oynattığını ölçerek scroll offset'i telafi eder. Safari 27.0, 17 Eylül 2026'da Scroll Anchoring desteğini ekledi; `overflow-anchor` Eylül 2026 itibarıyla güncel tarayıcılarda Baseline 2026 olarak listeleniyor.

## Mental model
```text
Önce                         Lazy image yüklenir
+------------------+         +------------------+
| üst içerik       |         | +300px yeni alan |
|------------------|         | üst içerik       |
| [ANCHOR] makale  |   =>    |------------------|
| okunan satır     |         | [ANCHOR] makale  |
+------------------+         +------------------+
 scrollY = y                 scrollY = y + 300
```
DOM büyür; kullanıcıyı DOM koordinatına değil, gördüğü içeriğe sabitle.

## İçeride ne oluyor?
- Browser scroll container descendant'ları arasından anchor candidate seçer.
- Anchor layout shift ile hareket ederse scroll position'a compensation uygulanır.
- `overflow-anchor:auto` varsayılandır; `none` subtree'yi anchor seçiminden çıkarır.
- Opt-out ancestor altında descendant `auto` ile yeniden opt-in olamaz; boundary seçimi önemlidir.
- Suppression triggers nedeniyle anchoring her mutation'da zorla uygulanmaz.
- Scroll snap ile birlikte adjustment yeniden snap'in izin verdiği aralıkla sınırlıdır.
- Anchoring layout shift'in nedenini çözmez; image dimensions/aspect-ratio ve stable skeleton hâlâ gereklidir.

## Mülakat soruları
1. Scroll anchoring hangi UX problemini çözer?
2. `overflow-anchor:none` ne zaman gerekir?
3. Scroll anchoring CLS'nin yerine geçer mi?
4. Mid: anchor selection ve compensation modelini anlat.
5. Senior: prepend pagination'da native anchoring ile manual restoration nasıl çatışır?
6. Staff: cross-browser layout-stability regression test'i nasıl kurarsın?

## Beklenen cevap derinliği
- **Junior:** layout shift, scroll container, `overflow-anchor`.
- **Mid:** candidate selection, compensation, opt-out boundary.
- **Senior:** suppression, scroll snap, programmatic scroll, virtualization.
- **Staff:** compatibility, telemetry, accessibility, progressive enhancement.

## Mini alıştırma
`scrollY=1200` iken viewport üstündeki image 280px büyüyor. Anchor +280px hareket ederse ideal compensated `scrollY` nedir? Chat prepend'de framework manual compensation + browser anchoring birlikte çalışırsa double-adjustment'ı açıkla.

## Proje fikri
`scroll-anchor-lab`: lazy images, prepend chat, ads ve virtualized list. Native anchoring açık/kapalı ve manual restoration varyantlarında visual jump, CLS, scroll delta ve interaction latency ölç; Playwright regression test'i ekle.

## Failure modes / trade-off / production
Tüm sayfada `overflow-anchor:none`, anchoring'i CLS çözümü sanmak, image dimensions ayırmamak, virtualization compensation ile browser compensation'ı çakıştırmak ve navigation/scroll restore test etmemek tipik hatalardır. Production'da CLS, unexpected scroll delta, restoration failures, browser/version segmentleri ve kullanıcı jump raporları izlenmelidir.

## Kaynaklar
- WebKit, 17 Eylül 2026 — Safari 27.0 / Scroll Anchoring: https://webkit.org/blog/18325/webkit-features-for-safari-27-0/
- MDN — `overflow-anchor`, Baseline 2026: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/overflow-anchor
- MDN — Scroll anchoring overview: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll_anchoring/Overview
