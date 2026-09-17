# PyTorch Distributed Checkpointing, Async Save & Recovery Economics

## Mental model
Distributed checkpointing, model/optimizer state'ini rank'ler arasında paralel kaydedip yükleyerek büyük training job'larında recovery maliyetini yönetir. PyTorch DCP load-time resharding desteklediği için checkpoint farklı bir world-size/topology ile restore edilebilir.

```text
GPU shards -> CPU staging -> durable storage
     |             |
     +-- training resumes during async persistence
```

Async checkpoint serialization işini ortadan kaldırmaz; GPU-visible pause'u azaltıp I/O işinin bir bölümünü critical path dışına taşır. Bunun karşılığında CPU memory, host bandwidth ve storage contention önem kazanır.

## Interview depth
- Junior/Mid: checkpoint, rank, shard, save/load.
- Senior: async staging, atomic completion, bandwidth ve restore testing.
- Staff: topology değişimi, object storage, failure domains ve capacity.
- Principal/CTO: GPU-hour kaybı, checkpoint frequency, storage cost ve recovery SLO.

## Failure modes
Incomplete checkpoint restore; CPU staging OOM; storage saturation; correlated failure domain; restore yolunun test edilmemesi; checkpoint interval'ının yalnız save süresine göre seçilmesi.

## Production metrics
Visible pause, background completion time, bytes/checkpoint, storage throughput, failed checkpoint count, restore duration ve lost training steps.

## Kaynaklar
- https://docs.pytorch.org/docs/main/distributed.checkpoint.html
- https://pytorch.org/blog/6x-faster-async-checkpointing/
- https://pytorch.org/blog/reducing-checkpointing-times/
- https://pytorch.org/blog/pytorch-2-8/
