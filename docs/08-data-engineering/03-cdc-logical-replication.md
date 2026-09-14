# CDC ve PostgreSQL Logical Replication

## Mental model
`DB write -> WAL -> logical decoding -> replication slot -> consumer -> read model`

CDC, tam tablo polling yerine değişiklik akışını tüketir. PostgreSQL logical replication publication/subscription modelidir; WAL logical decoding ile satır değişikliklerine çevrilir ve subscriber transactional order içinde uygular. UPDATE/DELETE için replica identity gerekir; çoğunlukla primary key kullanılır.

## Tasarım soruları
- Initial snapshot ile live stream arasındaki sınır nasıl güvenli kurulur?
- Consumer lag ve replication slot WAL retention nasıl izlenir?
- At-least-once replay durumunda downstream nasıl idempotent olur?
- Schema rollout producer/subscriber arasında hangi sırada yapılır?

## Failure modes
Consumer'ın uzun süre geride kalması WAL birikimine; DDL uyumsuzluğu replication stop'a; yetersiz replica identity pahalı row lookup'a; replay ise duplicate side-effect'e yol açabilir.

## Habitat bağlantısı
Storage control-plane metadata değişiklikleri CDC ile inventory, search veya analytics read model'larına taşınabilir. Böylece request path içinde dual-write yapmak yerine database commit'i source of truth kalır.

## Kaynaklar
- https://www.postgresql.org/docs/18/logical-replication.html
- https://www.postgresql.org/docs/18/logical-replication-architecture.html
- https://www.postgresql.org/docs/18/logical-replication-restrictions.html
