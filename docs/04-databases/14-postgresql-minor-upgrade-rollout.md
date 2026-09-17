# PostgreSQL Minor Upgrades, Security Fixes & Regression-Safe Rollout

## Mental model
Database patching iki riski dengeler: eski sürümde kalmanın security/data-integrity riski ve yeni patch'in regression riski.

```text
release -> triage -> release-note actions -> staging/replay
                                      -> canary/replica -> expand or abort
```

## Temel yaklaşım
PostgreSQL minor release'leri bug, security, low-risk ve data-corruption fix'leri taşır; proje current minor release'i kullanmayı önerir. Buna rağmen `minor = risksiz` değildir. Şubat 2026 update'inde regressions görüldüğü için out-of-cycle düzeltme planlandı. 13 Ağustos 2026'da PostgreSQL 18.6 yayımlandı; 18.5 post-wrap regression nedeniyle yayımlanmadı. 18.6 duyurusu security ve bug fix'lerinin yanında bazı kurulumlarda configuration/data cleanup/reindex aksiyonları gerektiğini belirtti.

## Rollout runbook
1. Security severity + exploitability + workload exposure triage.
2. Release notes'taki migration/reindex/configuration aksiyonlarını çıkar.
3. Extension/driver compatibility test et.
4. Representative query replay ve staging.
5. Replica veya küçük cohort canary.
6. Connection error, crash, replica lag, p95/p99 ve integrity kontrolleri.
7. Promote/abort; rollback binary/data compatibility'sini önceden kanıtla.

## Mülakat soruları
- Major/minor upgrade riskleri nasıl ayrılır?
- Security patch neden ertelenebilir veya hızlandırılabilir?
- Replica-first rollout neyi korur?
- Rollback ne zaman failover'dan daha tehlikelidir?
- Staff/EM: risk-based patch SLA nasıl kurulur?
- CTO: patch governance compliance ve availability ile nasıl bağlanır?

## Seviye beklentisi
Junior backup/versioning; Mid staging/release notes; Senior canary, integrity ve rollback; Staff/EM fleet waves ve exception process; Principal/CTO security exposure, downtime economics ve ownership.

## Alıştırma / proje
500 instance'ı P0/P1/P2 cohort'larına ayırıp critical fix için 24 saatlik rollout planı yaz. `pg-patch-gate` prototipinde release-note checklist, query replay, replica health, extension check ve promote/abort policy üret.

## Failure modes / production
Release notes'u atlamak; yalnız smoke test; restore süresini ölçmemek; extension veya query-plan regression'ını kaçırmak. Connection errors, replica lag, query p95/p99, crash/restart, integrity checks ve failover/rollback time izlenmelidir.

## Kaynaklar
- https://www.postgresql.org/support/versioning/
- https://www.postgresql.org/docs/release/18.6/
- https://www.postgresql.org/about/news/postgresql-186-1711-1615-1519-1424-and-19-beta-3-released-3365/
- https://www.postgresql.org/about/news/out-of-cycle-release-scheduled-for-february-26-2026-3241/
