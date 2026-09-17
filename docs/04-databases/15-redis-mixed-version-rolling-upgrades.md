# Redis Rolling Upgrades: Mixed-Version Protocol Boundaries & Availability

## Konu anlatımı
Rolling upgrade, cluster'ın tamamını aynı anda durdurmadan version değiştirmeyi amaçlar; mixed-version durumunun otomatik olarak güvenli olduğunu garanti etmez. Redis Software'ın Eylül 2026 release notes'u, Redis Search için 8.4 boundary'sini geçen mixed-version cluster'larda belirli parallel shard upgrade konfigürasyonunda query failure ve geçici downtime oluşabileceğini belgeliyor.

## Mental model
```text
old shard <--- internal protocol ---> new shard
    |                                  |
old capability                    new capability
    +--------- mixed fleet ------------+
                  |
       compatibility invariant
                  |
            availability
```

Rolling upgrade geçici bir heterogeneous protocol deployment'tır. Wire/internal protocol, persisted format, module API, command semantics ve feature negotiation için backward/forward compatibility düşünülmelidir. Runbook allowed-version skew, capability matrix, health gates ve rollback/roll-forward kararlarını içermelidir.

## Mülakat derinliği
Junior: rolling vs stop-the-world. Mid: version skew ve compatibility. Senior: canary shard, drain, rollback/roll-forward. Staff: protocol invariants, preflight ve fleet policy. CTO/EM: support window, availability ve change economics.

## Failure modes
`rolling = zero downtime` varsayımı; mixed-version query test etmemek; module/feature preflight yapmamak; rollback format compatibility'sini doğrulamamak.

## Alıştırma / proje
6 shard'lı bir cluster için eski -> yeni rollout state machine'i çiz. Her transition için promotion gate, abort condition ve rollback feasibility belirle; iki protocol version'ı simüle eden test harness'i oluştur.

## Kaynaklar
- https://redis.io/docs/latest/operate/rs/release-notes/rs-8-0-releases/rs-8-0-20-108/
- https://redis.io/docs/latest/operate/oss_and_stack/install/version-mgmt/
- https://redis.io/docs/latest/operate/rc/databases/version-management/
