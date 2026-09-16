# Python 3.14 t-strings: Structured Templates & Safe Processing

## Mental model
f-string doğrudan final string üretir; t-string ise literal ve interpolation parçalarını taşıyan immutable bir `Template` üretir. Böylece render öncesi policy uygulanabilir.

```text
t"Hello {user}" -> Template(strings, interpolations) -> processor -> output
                                                        |
                                              validate / escape / bind
```

## Neden önemli?
Python 3.14 template string literals ile custom string processing için dil seviyesinde structured representation sunar. `Template.strings` statik parçaları, `interpolations` dinamik parçaları, `values` ise interpolation değerlerini taşır. Processor HTML escaping, SQL parameter binding, structured logging veya domain-specific rendering yapabilir.

Bu özellik tek başına sanitizer değildir. SQL processor interpolation değerlerini driver parameter binding'e dönüştürmeli; HTML processor context-sensitive escaping uygulamalıdır. HTML, URL, JavaScript ve SQL aynı escaping kuralını paylaşmaz.

## Mülakat ekseni
- t-string ve f-string semantiği
- immutable structured template avantajı
- interpolation metadata
- context-sensitive escaping
- SQL parameterization
- safe-by-default framework API tasarımı

Junior/Mid düzeyinde representation farkı; Senior'da injection boundary ve processor tasarımı; Staff/Principal düzeyinde platform standardı, bypass yüzeyi ve migration tartışılır.

## Production failure modes
T-string'i otomatik güvenlik özelliği sanmak; raw string bypass bırakmak; interpolation içine secret/PII koyup telemetry'ye taşımak; bütün output context'lerine tek escape policy uygulamak; processor'ın conversion/format semantics'ini yanlış yorumlaması.

## Mini proje
HTML ve DB-API SQL processor yaz. Aynı template representation'dan HTML için escaped output, SQL için `(statement, params)` üret. Property-based test ile injection payload'larını dene.

## Kaynaklar
- https://docs.python.org/3.14/library/string.templatelib.html
- https://docs.python.org/3.14/reference/lexical_analysis.html#t-strings
- https://docs.python.org/3.14/whatsnew/3.14.html
- https://peps.python.org/pep-0750/
