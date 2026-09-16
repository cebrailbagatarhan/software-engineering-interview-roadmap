# Post-Quantum Cryptography Migration & Crypto Agility

## Konu anlatımı
PQC migration bir algorithm swap değil; cryptographic inventory, data-lifetime risk, protocol interoperability ve staged rollout problemidir. NIST'in finalized standartları FIPS 203 ML-KEM, FIPS 204 ML-DSA ve FIPS 205 SLH-DSA'dır. NIST organizasyonların migration'a başlamasını öneriyor; NIST IR 8547 transition planında quantum-vulnerable algoritmaların standartlardan 2035'e kadar kaldırılması hedeflenir ve yüksek riskli sistemler daha erken ele alınmalıdır.

Önce TLS, PKI, service identity, VPN, code signing, key wrapping, long-lived archives, HSM/KMS ve vendor appliance'larda RSA/ECC/DH kullanımını keşfet. Data lifetime ve exposure risk ile önceliklendir. Crypto agility algorithm/version'ın protocol veya schema'ya sert kodlanmaması, dual/hybrid rollout, telemetry ve rollback yeteneğidir.

## Mental model
```text
inventory -> risk/lifetime -> target standard
     |              |
 protocol/vendor ---+
        |
 dual/hybrid rollout -> interop/perf -> deprecate legacy
```

## İçeride ne oluyor?
ML-KEM shared secret establish eden bir KEM'dir; bulk encryption değildir. ML-DSA ve SLH-DSA signature standartlarıdır. Migration key/ciphertext/signature size, certificate/profile, HSM/KMS/library support ve protocol negotiation testleri gerektirir. NIST'in 2026 PIV çalışma taslakları classical credential'ları koruyup PQC objects ekleyen dual-stack yaklaşımını incremental deployment örneği olarak gösterir.

## Mülakat soruları
- KEM ve encryption primitive farkı nedir?
- ML-KEM/ML-DSA/SLH-DSA rolleri nedir?
- Harvest-now-decrypt-later hangi data için önemlidir?
- Crypto inventory nasıl çıkarılır?
- Dual/hybrid migration neden gerekir?
- Staff/CTO: 2035 hedefini roadmap'e nasıl çevirirsin?

## Beklenen cevap seviyesi
Mid: asymmetric/symmetric ve KEM/signature. Senior: inventory/interoperability. Staff: crypto agility, vendor dependencies ve rollback. CTO: risk, compliance ve yatırım sıralaması.

## Mini alıştırma
TLS edge, mTLS, code signing ve 10 yıllık encrypted backup için confidentiality lifetime, dependency readiness ve rollback zorluğuna göre priority matrix oluştur.

## Proje fikri
Repo/config/certificate metadata'sından crypto inventory ve PQC readiness raporu üreten scanner.

## Production bağlantısı / failure modes
Yalnız TLS edge'i taramak, PQC'yi bulk cipher sanmak, HSM/vendor dependency'lerini atlamak, size/performance etkisini ölçmemek ve rollback olmadan big-bang migration yapmak başlıca risklerdir.

## Kaynaklar
- https://www.nist.gov/pqc
- https://csrc.nist.gov/projects/post-quantum-cryptography
- https://csrc.nist.gov/pubs/fips/203/final
- https://csrc.nist.gov/News/2026/pqc-updates-to-piv-standards-working-drafts
