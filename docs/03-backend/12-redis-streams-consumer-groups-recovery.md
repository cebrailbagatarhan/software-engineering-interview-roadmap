# Redis Streams Consumer Groups, PEL & Recovery

## Neden önemli?
Redis Streams consumer groups worker'lar arasında stream işini paylaştırırken pending ownership ve acknowledgement ile at-least-once processing modeli kurar. Mülakatta kritik nokta Redis komutlarını ezberlemek değil, delivery semantics ile business side-effect correctness'ini ayırmaktır.

## Mental model
```text
XADD -> stream -> consumer group -> worker
                              |       |
                              +-> PEL <-+
                                  |
                        XACK / reclaim
```

`XREADGROUP` ile teslim edilen mesaj ACK edilene kadar PEL'de kalır. `XACK` pending kaydını kaldırır. Crash olmuş consumer'ın idle pending entry'leri `XPENDING` ile gözlenip `XCLAIM`/`XAUTOCLAIM` ile başka consumer'a geçirilebilir. Redis 8.4 `XREADGROUP ... CLAIM` ile yeni ve reclaim edilebilir mesajları tek read akışında ele alabilir.

## Correctness
Side-effect sonrası ACK öncesi crash duplicate processing üretebilir. Bu yüzden ödeme, shipment veya DB mutation gibi işlemler event ID/business key ile idempotent olmalıdır. Reclaim ownership transferidir; önceki side-effect'i geri almaz.

## Trade-off'lar
Kısa reclaim idle threshold yavaş ama sağlıklı consumer'dan ownership çalabilir; uzun threshold recovery'yi geciktirir. Poison message sonsuz retry yerine bounded retry/DLQ politikası ister. Consumer silmeden önce pending entry'ler claim veya ACK edilmelidir.

## Production
PEL size/age, stream lag, reclaim rate, delivery count, handler error ve idempotency conflict ölç. Fault injection ile DB commit–ACK arası crash senaryosunu test et.

## Mülakat soruları
- PEL neden vardır?
- `>` ve pending-history read farkı nedir?
- At-least-once neden idempotency gerektirir?
- Reclaim timeout nasıl seçilir?
- Duplicate payment nasıl engellenir?

## Kaynaklar
- https://redis.io/docs/latest/develop/data-types/streams/
- https://redis.io/docs/latest/commands/xreadgroup/
- https://redis.io/docs/latest/commands/xpending/
- https://redis.io/docs/latest/commands/xautoclaim/
- https://redis.io/docs/latest/commands/xack/
