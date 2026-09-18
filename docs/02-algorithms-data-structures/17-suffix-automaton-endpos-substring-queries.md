# Suffix Automaton, Endpos Classes & Substring Queries

**Seviye:** Junior → Staff  
**Alan:** Algorithms & Data Structures / String Processing

## Konu anlatımı
Suffix automaton (SAM), bir string'in bütün substring'lerini tanıyan minimal deterministic finite automaton'dur. Yalnız suffix'leri değil, kaynak string'in substring dilini kompakt biçimde temsil eder. Uzunluğu `n` olan string için yapı lineer boyuttadır ve online olarak soldan sağa kurulabilir.

Her state `len` ve suffix link taşır. Aynı state'teki substring'ler aynı `endpos` kümesine sahiptir. Yeni karakter eklenirken normal state oluşturulur; determinism/minimality boundary'si gerektiğinde clone state üretilir. Clone yeni occurrence değildir; mevcut equivalence class'ı doğru uzunluk sınırında böler.

## Mental model
```text
text: a b a b a
      | | | | |
start -> states via character transitions
          |
          +-- suffix link --> shorter endpos class

state v represents lengths:
len(link(v)) + 1 ... len(v)
```

**Invariant:** state aynı end-position kümesini paylaşan substring sınıfıdır; suffix link uygun en uzun strict suffix sınıfına gider.

## İçeride ne oluyor?
- Yeni karakter için `cur`, `len[cur]=len[last]+1`.
- Suffix-link zincirinde eksik transition'lar `cur`'a bağlanır.
- Doğrudan link koşulu bozulursa `clone` oluşturulur.
- Clone transition ve link'i kopyalar; `len` gerekli boundary'ye çekilir.
- Distinct substring sayısı `sum(len[v]-len[link[v]])` olur.
- Occurrence bilgisi `len` azalan sırada suffix link boyunca aggregate edilebilir.

## Mülakat soruları
1. Suffix automaton neyi temsil eder?
2. `len` ve suffix link ne anlama gelir?
3. Clone neden gerekir?
4. Pattern substring membership nasıl test edilir?
5. Distinct substring formülü nereden gelir?
6. Senior: occurrence count ve longest common substring nasıl çözülür?
7. Staff: suffix array/tree/SAM arasında nasıl seçim yaparsın?

## Beklenen cevap seviyesi
- **Junior:** automaton ve membership yürüyüşünü açıklar.
- **Mid:** suffix link, len aralığı ve clone mekanizmasını kurar.
- **Senior:** endpos equivalence ve türetilmiş query'leri açıklar.
- **Staff:** alternatif index yapılarıyla memory/query trade-off'u yapar.

## Mini alıştırma
`ababa` için state'lerin `len`, `link` ve transition'larını çıkar; `bab`, `baa`, `aba` query'lerini yürüt ve distinct substring sayısını hesapla.

## Proje fikri
`suffix-automaton-lab`: substring existence, occurrence count, distinct substring ve longest common substring sunan CLI. Küçük input'larda brute-force oracle ile property-based test ekle.

## Failure modes / trade-off / production bağlantısı
Clone occurrence'ını yanlış saymak, propagation sırasını bozmak, Unicode byte/code-point semantiğini tanımlamamak ve büyük alphabet'te dense transition table kullanmak tipik hatalardır. Online corpus/string analytics için güçlüdür; immutable corpus'ta suffix array daha cache-friendly olabilir. State/transition count, bytes/state, build throughput ve query latency ölçülür.

## Kaynaklar
- Blumer et al. — The Smallest Automaton Recognizing the Subwords of a Text (1985): https://doi.org/10.1016/0304-0208(85)90010-6
- Crochemore — Transducers and repetitions (1986): https://doi.org/10.1016/0304-3975(86)90141-1
- cp-algorithms — Suffix Automaton: https://cp-algorithms.com/string/suffix-automaton.html
