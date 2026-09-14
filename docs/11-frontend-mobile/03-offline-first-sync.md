# Offline-First, Local Source of Truth & Sync Conflicts

Offline-first yalnızca HTTP cache değildir. Network kullanan repository local ve network data source'u birleştirir; higher layer okumaları canonical local source-of-truth üzerinden yapılır. Network refresh önce local store'u günceller, UI observable local state'i izler.

```text
UI <-observe- Local DB <- Repository -> Network
                    ^         |
                    +-- durable sync queue
```

Writes domain semantiğine göre online-only, queued veya local-first/lazy olabilir. Local-first güçlü UX sağlar fakat reconnect sonrası conflict resolution ister. LWW basittir fakat clock skew/semantic loss yaratabilir; version, field-level merge veya operation-log yaklaşımları daha güçlü fakat karmaşıktır. Idempotency, durable queue, tombstone/deletion, retry ve schema evolution sync protokolünün parçasıdır.

## Interview checkpoints
- Offline-first vs response cache.
- Local source-of-truth neden önemlidir?
- Queued vs local-first writes.
- Multi-device conflict resolution.
- Tombstone ve delete resurrection.
- Idempotent retry.

## Production failure modes
In-memory queue ile veri kaybetmek, blind LWW, duplicate mutation, delete resurrection, unbounded retry, battery/data maliyetini ve schema migration'ı yok saymak.

## Alıştırma / proje
İki cihazın aynı kaydı offline değiştirdiği senaryoda field-level merge, LWW ve operation-log'u karşılaştır. SQLite/Room source-of-truth + durable outbox + reconnect sync içeren `offline-sync-lab` geliştir.

## Kaynak
- https://developer.android.com/topic/architecture/data-layer/offline-first
