# Model Registry Aliases, Promotion & Rollback Discipline

## Konu anlatımı
Model registry yalnız artifact storage değildir; model version, lineage, metadata ve deployment intent'i yöneten lifecycle control plane'dir. MLflow Model Registry registered model altında version'lar, tags ve mutable aliases sunar. `champion` alias belirli model version'ına işaret ederek serving code'u sabit version numarasından ayırabilir.

## Mental model
```text
run -> v17 --+
run -> v18 --+--> registry
              |
 champion ---> v17
 challenger -> v18
              |
          canary/eval
              |
 champion ---> v18

regression: champion -> v17
```

Alias mutable pointer; version reproducible deployment identity olarak düşünülmelidir.

## Promotion pipeline
Offline eval ve validation sonrası challenger canary'ye alınır. Model signature/schema, integration test, latency/error, prediction-quality proxy ve business guardrail'leri geçerse champion alias yeni version'a taşınır. Regression'da alias known-good version'a geri alınabilir.

Alias update tek başına rollout değildir: serving process model'i cache'liyorsa yeni alias anında yüklenmeyebilir. Deployment convergence, artifact availability, feature contract ve rollback verification ayrıca ölçülmelidir.

## Mülakat soruları
- Registry artifact store'dan nasıl ayrılır?
- Version ve alias farkı nedir?
- Alias deployment code'unu nasıl decouple eder?
- Alias rollback hangi durumda yeterli değildir?
- Model signature neden promotion gate'idir?
- Staff: dev/staging/prod permission ve approval akışını nasıl kurarsın?

## Seviyeye göre cevap derinliği
Mid: experiment, model version, deployment. Senior: alias, lineage, schema, canary, rollback. Staff: environment isolation, RBAC, auditability, reproducibility. EM/CTO: risk tiering, release governance ve rollback SLO.

## Mini alıştırma
v17 production, v18 challenger; v18 offline metric'te iyi fakat p99 latency %35 yüksek. Promotion gate, canary oranı, rollback trigger ve alias geçiş sırasını tasarla.

## Proje fikri
`model-registry-release-lab`: MLflow champion/challenger aliases, version tags ve signatures. CI smoke/eval gate sonrası promotion; synthetic regression sonrası rollback.

## Failure modes / production
`latest` version'ı kör deploy etmek; alias değişimini rollout tamamlandı sanmak; feature schema drift; rollback artifact'ını silmek; geniş registry write yetkisi; yalnız offline metric ile promotion. Deployed version/alias, latency/error, quality proxy, feature drift ve rollback time izlenmelidir.

## Kaynaklar
- https://mlflow.org/docs/latest/ml/model-registry/
- https://mlflow.org/docs/latest/ml/model-registry/workflow/
- https://mlflow.org/docs/latest/ml/model-registry/tutorial/
