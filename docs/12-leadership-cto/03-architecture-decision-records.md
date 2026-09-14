# Architecture Decision Records ve Decision Quality

ADR, önemli architecture kararlarının context, alternatives, decision ve consequences bilgisini version-controlled biçimde saklar. Amaç toplantı tutanağı üretmek değil, gelecekte “neden böyle yaptık?” sorusuna güvenilir cevap bırakmaktır.

## Minimal ADR
```text
Status
Context / problem
Decision drivers
Alternatives
Decision
Positive / negative consequences
Revisit triggers
```

## Decision quality
Staff/Principal/CTO seviyesinde format ikincildir. Asıl sorular:
- Karar reversible mı?
- Blast radius nedir?
- Migration/switching cost nedir?
- Cost of delay nedir?
- Hangi assumption değişirse karar yeniden açılır?

Eski kararı sessizce yeniden yazmak history'yi bozar. Yeni karar önceki ADR'yi supersede edebilir.

## Interview prompts
- ADR ile design doc farkı?
- Hangi karar ADR hak eder?
- Build-vs-buy için hangi driver'lar gerekir?
- Yanlış çıkan karar kötü karar mıdır?
- Governance nasıl bureaucracy olmadan ölçeklenir?

## Failure modes
Karar sonrası justification yazmak, alternatifleri zayıf göstermek, ölçülebilir revisit trigger bırakmamak ve her küçük tercihi ADR'ye çevirmek karar sisteminin sinyal/gürültü oranını düşürür.

## Production / organization bağlantısı
İyi ADR sistemi cross-team memory sağlar; onboarding'i ve migration reasoning'ini kolaylaştırır. Yüksek blast-radius kararlarda accountability yaratırken düşük riskli reversible kararları merkezi approval'a bağlamamalıdır.

## Kaynak
ADR topluluğu ve kaynak kataloğu: https://adr.github.io/
