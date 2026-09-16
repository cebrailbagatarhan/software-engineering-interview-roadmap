# Build Provenance, Artifact Attestations & Deployment Policy

## Konu anlatımı
Registry'deki artifact'ın hash'inin doğru olması kaynağının güvenilir olduğunu tek başına kanıtlamaz. Build provenance, artifact digest'ini repository, commit, CI workflow ve build identity ile doğrulanabilir biçimde ilişkilendirir. GitHub Actions artifact attestations OIDC ve Sigstore tabanlı provenance üretebilir.

```text
source -> trusted CI -> artifact digest
            |              |
            +--- OIDC -----+
                  |
           signed attestation
                  |
             verifier
                  |
          deployment policy
```

## Mental model
**Integrity:** byte'lar değişti mi? **Provenance:** nerede/nasıl üretildi? **Policy:** bu provenance kabul edilebilir mi? **SBOM:** içinde ne var?

## İçeride ne oluyor?
Artifact digest subject olarak attestation'a bağlanır. Workflow identity claim'i imzalı provenance üretir. Consumer verifier ile expected repository/workflow gibi trust kriterlerini doğrular. Kubernetes admission katmanı verification'ı deploy-time enforcement'a dönüştürebilir. Attestation güvenlik açığı olmadığını garanti etmez; trusted workflow compromise edilmişse güvenilir görünen kötü artifact üretilebilir.

## Mülakat soruları
- Signing ile provenance farkı nedir?
- Digest neden tek başına trust değildir?
- OIDC hangi secret-management problemini azaltır?
- Provenance ile SBOM farkı nedir?
- Verify edilmeyen attestation neden az değer sağlar?
- Senior: trusted CI compromise edilirse sınır nedir?
- Staff: admission enforcement rollout'u nasıl yapılır?
- Principal/CTO: organization-wide trust policy nasıl yönetilir?

## Beklenen cevap seviyesi
Junior hash/signature; Mid provenance/OIDC/SBOM; Senior trust root ve CI compromise; Staff admission, break-glass ve rollout; Principal/CTO governance, audit ve supply-chain economics.

## Mini alıştırma
Yalnız protected branch'ten trusted workflow ile üretilen `org/payments` image digest'lerinin production'a girebildiği policy tasarla. Verification failure ve break-glass akışını ekle.

## Proje fikri
GitHub Actions ile container build + attestation üret; CLI ile verify et; test Kubernetes cluster'ında unsigned/untrusted image'i admission policy ile reddet.

## Failure modes / trade-off / production
Attestation'ı vulnerability scanner sanmak, mutable tag'e güvenmek, verification yapmamak, geniş workflow permissions, compromised trusted workflow ve audit edilmeyen break-glass temel risklerdir. Verification failures, rejected deploys, exceptions, unattested artifact rate ve identity drift izlenmelidir.

## Kaynaklar
- https://docs.github.com/en/actions/concepts/security/artifact-attestations
- https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
- https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/enforce-artifact-attestations
