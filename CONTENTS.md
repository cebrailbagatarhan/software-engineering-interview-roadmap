# İçindekiler

Bu dosya repodaki **kalıcı kitap bölümlerini, soru bankalarını ve lab'leri** hızlı bulmak için tutulur.

## Başlangıç

- [Roadmap](ROADMAP.md)
- [Seviye beklentileri](LEVELS.md)

## Bölüm I — Computer Systems Foundations

1. [CPU, Cache ve Memory Hierarchy](docs/01-foundations/01-cpu-memory-hierarchy.md)
2. [Process, Thread, Virtual Memory ve Concurrency](docs/01-foundations/02-process-thread-virtual-memory.md)

Önerilen sıra:

```text
CPU/cache
   ↓
process/thread
   ↓
virtual memory
   ↓
concurrency
   ↓
networking
```

## Bölüm II — Networking

1. [TCP, DNS, HTTP ve Request Yolculuğu](docs/02-networking/01-tcp-dns-http.md)

## Bölüm III — Backend Engineering

1. [Cache, Rate Limiting, Idempotency ve Retry](docs/03-backend/01-cache-rate-limit-idempotency.md)

## Bölüm V — Distributed Systems

1. [Storage Platforms — Habitat Case Study](docs/05-distributed-systems/01-storage-platforms-habitat.md)

## Soru Bankası

- [Foundations + Networking + Backend — 40 high-yield soru](questions/high-yield/01-foundations-networking-backend.md)

## Lab'ler

- [Build a Production-Minded Rate Limiter](labs/build-a-rate-limiter/README.md)

## Görseller

- [CPU / Memory Hierarchy SVG](assets/cpu-memory-hierarchy.svg)

---

# Çalışma önerisi

Bir bölümü şu sırayla çalış:

```text
20-30 dk konu
→ 5 interview question
→ whiteboard açıklaması
→ 30-60 dk mini lab
→ failure mode yaz
→ trade-off yaz
```

Senior+ seviyede her bölümün sonunda şu dört soruya cevap vermeye çalış:

1. Bu sistem nerede bottleneck olur?
2. Dependency çökerse ne olur?
3. Blast radius nasıl küçültülür?
4. Ölçmek için hangi metric/trace gerekir?

CTO/EM seviyesinde iki soru daha ekle:

5. Bu complexity gerçekten gerekli mi?
6. Build etmek mi, satın almak mı, managed service kullanmak mı daha mantıklı?
