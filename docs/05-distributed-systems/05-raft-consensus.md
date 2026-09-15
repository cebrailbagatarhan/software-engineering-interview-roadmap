# Raft Consensus: Election, Replication & Safety

## Mental model
Raft problemi leader election, log replication ve safety olarak böler. Node follower, candidate veya leader durumundadır; seçimler monoton artan term'ler içinde yürür.

```text
followers -- majority votes --> leader
clients --> leader --> AppendEntries --> followers
                    \-- majority + safety --> commit
```

## Temel mekanizma
Follower heartbeat alamayınca randomized election timeout sonrası candidate olur, term'i artırır ve oy ister. Majority alan candidate leader olur. Leader client command'larını log'a ekleyip follower'lara replicate eder. Term, log matching ve leader completeness gibi kurallar committed history'nin çelişkili loglar tarafından ezilmesini engeller.

Network partition'da majority taraf uygun seçim sonrası ilerleyebilir; minority taraf güvenli biçimde yeni committed entry oluşturamaz. Consensus replication'dan daha güçlü bir problemdir: node'ların hangi history üzerinde anlaşacağını belirler.

## Mülakat derinliği
Senior: election, AppendEntries, conflict repair, commit safety. Staff/Principal: membership changes, durability assumptions, cross-region quorum latency ve client-side deduplication.

## Failure modes
Replication=consensus sanmak, minority write kabul etmek, fsync varsayımını unutmak, Raft'ın application exactly-once sağladığını düşünmek ve quorum latency'yi hesaba katmamak.

## Kaynaklar
- https://raft.github.io/
- https://raft.github.io/raft.pdf
