# CodeQL Data Flow, Taint Tracking & Query Precision

## Neden önemli?
Static analysis'te temel mental model `source → propagation → sink → sanitizer/barrier` zinciridir. Güvenlik analizi yalnız pattern matching değildir; verinin fonksiyonlar, alanlar ve framework abstraction'ları boyunca nasıl aktığını modellemek gerekir.

## Mental model
```text
untrusted input -> SOURCE -> propagation -> [sanitizer?] -> SINK
                                      | yes
                                      +---------> safe path
```

Source saldırgan kontrollü veri; sink SQL/command/template/path gibi riskli operasyon; sanitizer belirli context altında güvenli dönüşümdür. Interprocedural analysis fonksiyon sınırlarını, framework modeling runtime semantics'i kapsar.

## Güncel production bağlantısı
CodeQL 2.26.4 (3 Eylül 2026), Spring R2DBC `DatabaseClient` ve R2DBC SPI için SQL-injection sink modelleri ekledi ve Rust data-flow alert location'larını hassaslaştırdı. 2.27.0 (9 Eylül) Linux ARM64 ve ek query/framework iyileştirmeleri getirdi. Analyzer doğruluğu query kadar model coverage'a bağlıdır.

## Mülakat soruları
- Static ve dynamic analysis nasıl ayrılır?
- Source/sink/sanitizer nedir?
- False positive ve false negative neden oluşur?
- Parameterized SQL neden escaping'den güçlüdür?
- Framework model eksikliği neye yol açar?
- Custom query pack rollout'u nasıl yönetilir?

## Seviyeye göre derinlik
Junior/Mid: injection ve source-sink. Senior: interprocedural flow, precision/recall. Staff: custom modeling, baseline ve CI governance. Leadership: remediation SLA, developer friction ve risk reduction.

## Mini alıştırma
HTTP handler → service → repository akışında user input'un raw SQL'e ulaştığı path'i çiz; parameterized query ile güvenli boundary'yi göster.

## Proje
`mini-taint-lab`: intentionally vulnerable web corpus'u, custom queries ve regression CI.

## Failure modes / trade-off
Context-independent sanitizer varsayımı, framework flow'unu kaçırmak, alert churn'ü regression sanmak, yalnız alert count ölçmek. Production'da exploitable path, fix latency, recurring pattern, coverage ve suppression age izlenir.

## Kaynaklar
- https://github.blog/changelog/2026-09-03-codeql-2-26-4-improves-github-actions-security-detections/
- https://github.blog/changelog/2026-09-09-codeql-2-27-0-adds-support-for-linux-arm64/
- https://codeql.github.com/docs/writing-codeql-queries/about-data-flow-analysis/
