# Consumer-Driven Contract Testing

## Neden önemli?
Unit tests tek bileşeni, end-to-end tests tüm zinciri sınar. Dağıtık sistemlerde sık görülen ayrı risk, iki servisin aynı API/message sözleşmesini farklı yorumlamasıdır. Contract testing bu compatibility sınırını hedefler.

## Mental model
```text
Consumer CI
real API client -> mock provider -> contract artifact
                                  |
                                  v
                            contract broker
                                  |
                                  v
Provider CI              replay interactions
provider state --------> real provider
                                  |
                             verification
                                  |
                         deploy compatibility
```

## Temel kavramlar
- Consumer gerçek API client kodunu mock provider'a karşı çalıştırır ve ihtiyaç duyduğu interaction'ları contract'a yazar.
- Provider verification contract request'lerini gerçek provider implementation'ına replay eder.
- Provider states deterministic fixture/setup sağlar.
- Consumer-driven contract, yalnız schema validation değildir: gerçek consumer beklentilerini executable examples ile temsil eder.
- Contract + consumer/provider version metadata deploy compatibility graph'i oluşturabilir.
- Matcher'lar yalnız consumer'ın gerçekten bağımlı olduğu alanları doğrulamalıdır; aşırı strict contract coupling yaratır.
- Contract tests functional/business correctness veya gerçek infrastructure davranışının tamamının yerine geçmez.

## Mülakat soruları
1. Unit, contract, integration ve E2E hangi farklı riskleri yakalar?
2. Consumer-driven contract neden yalnız OpenAPI validation değildir?
3. Provider verification nasıl çalışır?
4. Provider state neden gerekir?
5. Mobile client gibi uzun yaşayan consumer versions nasıl korunur?
6. Staff: onlarca serviste broker ve deploy gate nasıl ölçeklenir?
7. Principal: independent deployability ile compatibility governance nasıl dengelenir?

## Beklenen cevap seviyesi
- **Mid:** consumer/provider, artifact ve verification akışı.
- **Senior:** provider states, matchers, versioning, async messaging ve false-confidence sınırları.
- **Staff:** CI/CD gates, broker topology, backward compatibility ve ownership.
- **Principal:** API evolution policy, deployment graph, platform cost ve developer velocity.

## Mini alıştırma
`orders-ui -> orders-api` consumer'ı yalnız `id`, `status`, `total` kullansın. Provider `warehouseId` eklesin, `total` tipini number'dan string'e değiştirsin ve bir `status` değerini yeniden adlandırsın. Hangi değişikliklerin contract'ı kırması gerektiğini gerekçelendir.

## Proje fikri
`contract-ci-lab`: consumer + provider iki küçük servis kur. Consumer contract üretsin ve broker/artifact store'a yayınlasın; provider CI verify etsin. Additive-compatible ve field/type-breaking değişikliklerde deploy gate davranışını göster.

## Failure modes ve trade-off
- Implementation detail'e aşırı bağlanan contract brittle olur.
- Yalnız happy-path interaction false confidence yaratır.
- Stale contract/version metadata yanlış deploy compatibility sinyali verir.
- Contract tests auth/network policy, data migration ve gerçek infrastructure failure'larını tek başına doğrulamaz.
- Her interaction'ı contract'a taşımak bakım maliyetini artırır; consumer'ın gerçekten kullandığı davranış korunmalıdır.

## Production bağlantısı
Contract verification failures, incompatible deploy rollback'leri, API error-rate, schema/version adoption ve E2E incident'ları birlikte izlenmelidir. Contract verification CI'da erken compatibility feedback; production telemetry ise gerçek davranışın doğrulamasıdır.

## Kaynaklar
- Pact — Introduction: https://docs.pact.io/
- Pact — Consumer tests: https://docs.pact.io/consumer
- Pact — Provider verification: https://docs.pact.io/getting_started/verifying_pacts
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
