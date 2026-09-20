# Filesystem Internals: inode, Page Cache, `fsync` ve Crash Consistency

## Mental model
```text
process -> fd -> dentry/inode -> address_space -> page/folio cache -> writeback -> filesystem -> block/device cache -> media
```

## Temel fikir
`write()` başarısı ile power-loss sonrası durability aynı garanti değildir. VFS ortak object/operation katmanını sağlar; inode identity/metadata'yı, dentry pathname çözümünü, `address_space` ise file-backed page/folio cache'i ve Dirty/Writeback state'ini bağlar. Buffered I/O page cache üzerinden ilerleyebilir; dirty data daha sonra writeback ile storage'a gönderilir. Durability gereken yerde `fsync()` ve update ordering açıkça tasarlanmalıdır.

## İçeride ne oluyor?
- Buffered read cache hit olabilir; miss filesystem I/O ve readahead başlatabilir.
- Buffered write dirty cache state üretip storage persistence'dan önce dönebilir.
- `mmap` file-backed sayfaları process address space'e bağlar; writeback yaşam döngüsü devam eder.
- Journaling recovery/order guarantees'i güçlendirir fakat her successful write'ı durable transaction yapmaz.
- Volatile device write-back cache'lerinde filesystem/block layer flush veya FUA kullanarak persistence boundary talep edebilir.
- Crash-safe replacement tasarımında file content, rename ve directory metadata durability ayrı adımlar olarak düşünülmelidir.

## Mülakat soruları
1. fd, dentry ve inode rollerini ayır.
2. Page cache neden vardır?
3. `write()` döndüğünde veri durable mıdır?
4. Buffered ve direct I/O trade-off'u nedir?
5. `fsync()` neden p99 latency spike yaratabilir?
6. Atomic rename ile durable rename neden aynı şey değildir?
7. DB buffer pool + OS page cache double caching ne zaman maliyetlidir?

## Seviye beklentisi
Junior kavramları ayırır; Mid dirty/writeback/readahead/fsync'i açıklar; Senior crash windows, journaling ve device cache'i tartışır; Staff storage-engine I/O policy, tail latency ve failure-domain tasarımını bağlar.

## Alıştırma ve proje
Temporary file -> fsync -> rename -> directory durability timeline'ı çiz. Ardından checksum'lı append-only KV store geliştir; fsync-per-write ve group commit modlarında throughput/p99 latency ile recovery sonucunu karşılaştır.

## Failure modes / production
`write()==len` sonucunu durability sanmak, page cache ile device cache'i karıştırmak, her write'ta fsync ile throughput'u gereksiz düşürmek veya hiç persistence boundary kurmamak temel hatalardır. Dirty/writeback pressure, fsync latency, I/O queue latency, ENOSPC, inode exhaustion ve recovery time izlenmelidir.

## Kaynaklar
- Linux VFS: https://docs.kernel.org/filesystems/vfs.html
- FUSE I/O modes: https://docs.kernel.org/filesystems/fuse/fuse-io.html
- Write-back cache control: https://docs.kernel.org/block/writeback_cache_control.html
- fsync(2): https://man7.org/linux/man-pages/man2/fsync.2.html
