# Go 1.27 Generic Methods, API Design & Migration

Go 1.27 ile generic method desteği geldi. Method-local type parameter, receiver'ın type parameter'ından bağımsız bir dönüşüm/işlem tipini ifade etmek gerektiğinde API yüzeyini sadeleştirebilir.

```text
receiver[T] -> Method[U](input U) -> result
```

## Tasarım sezgisi
Generic method; concrete method çoğaltmasını azaltabilir, fakat interface polymorphism'in otomatik ikamesi değildir. Constraint mümkün olan en küçük davranış/type set'ini ifade etmeli; public API'de inference ergonomics, compatibility ve caller readability test edilmelidir.

## Mülakat derinliği
Junior: type parameter. Mid: constraint/inference. Senior: API migration ve compatibility. Staff: monorepo/toolchain rollout. Principal/CTO: ecosystem ve support policy.

## Failure modes
Over-generalization, gereksiz karmaşık constraint, eski public method'ları ani kaldırma, toolchain drift ve benchmark yapmadan performans varsayımı.

## Production bağlantısı
SDK'lar, shared platform libraries ve domain collection API'lerinde daha küçük public surface mümkün olabilir. Migration canary, compile/test matrix ve dependency inventory ile yürütülmelidir.

## Kaynaklar
- https://go.dev/blog/go1.27
- https://go.dev/doc/devel/release
