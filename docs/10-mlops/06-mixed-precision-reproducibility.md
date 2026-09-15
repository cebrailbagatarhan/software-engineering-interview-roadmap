# Mixed Precision Training, Gradient Scaling & Reproducibility

## Konu anlatımı
PyTorch AMP'de `autocast`, operation'ları numerik ve performans özelliklerine göre uygun precision'da çalıştırır. FP16 gradient underflow riskine karşı `GradScaler` loss/gradient ölçekleme lifecycle'ını yönetir; optimizer step öncesi unscale eder ve non-finite gradient durumunda step atlanabilir.

Reproducibility ayrı bir eksendir. Aynı seed farklı PyTorch release/platform veya CPU/GPU arasında tam aynı sonucu garanti etmez. `torch.use_deterministic_algorithms(True)` desteklenen operation'larda deterministic implementation seçebilir fakat tek başına tüm pipeline'ı reproducible yapmaz ve performans maliyeti olabilir. Production provenance; code, framework/CUDA/container version, dataset snapshot, preprocessing, hyperparameters, RNG state ve checkpoint bilgilerini kapsamalıdır.

## Mental model
```text
forward -> autocast -> loss -> scale -> backward
                                  |
                               unscale
                                  |
                           finite? -> step/update

reproducibility = code + data + environment + RNG + algorithms
```

## Mülakat soruları
- Mixed precision neden tüm op'ları FP16 yapmak değildir?
- Gradient scaling neyi çözer?
- Inference'ta GradScaler neden gerekmez?
- Seed neden tek başına reproducibility sağlamaz?
- Determinism ile throughput trade-off'u nedir?

## Beklenen cevap seviyesi
Mid: dtype/autocast/underflow. Senior: scaler lifecycle, clipping, NaN/Inf. Staff: distributed provenance, determinism policy ve training economics.

## Mini alıştırma
`autocast -> scale -> backward -> unscale/clip -> step -> update` sırasını açıklayın.

## Proje fikri
`amp-repro-lab`: FP32 ve AMP training'i time/memory/quality/run variance eksenlerinde karşılaştır.

## Production bağlantısı ve failure modes
Clipping öncesi unscale etmemek; non-finite step skip'lerini izlememek; seed'i provenance sanmak; determinism'i benchmark etmeden zorunlu kılmak.

## Kaynaklar
- https://docs.pytorch.org/docs/main/notes/amp_examples.html
- https://docs.pytorch.org/docs/stable/notes/randomness.html
- https://docs.pytorch.org/docs/main/generated/torch.use_deterministic_algorithms.html
