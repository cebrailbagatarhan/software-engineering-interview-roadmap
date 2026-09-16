# Post-Quantum Crypto Migration, Inventory & Algorithm Agility

## Problem
PQC migration bir algoritma swap'i değil, enterprise dependency migration programıdır. NIST'in FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) ve FIPS 205 (SLH-DSA) standartları finalize edilmiştir ve NIST kuruluşların geçişe başlamasını önerir.

```text
inventory -> lifetime/risk -> compatibility lab
   |                              |
vendors/protocols -> canary/hybrid -> migrate
                                  |
                           telemetry + rollback
```

## Crypto inventory
TLS termination, PKI, service identity, code signing, firmware, KMS/HSM, backup encryption, third-party SaaS ve uzun ömürlü veride public-key kullanım noktaları çıkarılmalıdır. Veri ömrü, harvest-now-decrypt-later riskinin önceliğini değiştirir.

## Algorithm agility
Business logic'in belirli primitive'e bağlanması yerine versioned crypto policy/provider boundary kullanmak migration ve rollback'i kolaylaştırır. Agility, algoritmayı rastgele runtime'da seçmek değil; kontrollü, test edilebilir ve audit edilebilir değişim kapasitesidir.

## Mülakat derinliği
Junior: encryption/signature/public-key. Mid: KEM, PKI, lifecycle. Senior: protocol compatibility, performance, HSM/KMS, rollback. Staff: inventory, vendor matrix, staged migration. Principal/CTO: multi-year risk, procurement, compliance ve bütçe.

## Failure modes
- Yalnız internet-facing TLS'i migrate etmek.
- Code signing, backups, firmware ve embedded sistemleri unutmak.
- Büyük key/certificate/message boyutlarının network etkisini test etmemek.
- Vendor readiness varsaymak.
- Rollback yolunu erkenden kaldırmak.
- Tek implementation/algorithm'a sıkı bağlanmak.

## Production bağlantısı
Handshake latency/failure, CPU, certificate/message size, algorithm-version adoption, compatibility matrix ve kalan legacy inventory izlenmelidir. Migration canary, hybrid veya protocol-specific staged rollout gerektirebilir.

## Alıştırma / proje
SaaS sistemi için crypto inventory çıkar ve data lifetime/migration priority ekle. `crypto-agility-inventory` isimli read-only scanner ile config/repo içindeki algorithm/certificate/key kullanım noktalarını owner ve policy ile eşleştir.

## Kaynaklar
- https://www.nist.gov/pqc
- https://www.nist.gov/cybersecurity-and-privacy/what-post-quantum-cryptography
- https://csrc.nist.gov/pubs/fips/203/final
- https://csrc.nist.gov/pubs/fips/204/final
- https://csrc.nist.gov/pubs/fips/205/final
