# ELF, ABI, Linker ve Dynamic Loader

## Neden önemli?
Compiler executable üretim zincirinin yalnız bir parçasıdır. Ayrı object file ve shared library'lerin binary seviyede birlikte çalışması linker, loader ve ABI sözleşmesine bağlıdır.

## Mental model
```text
source -> compiler/assembler -> .o --+
                                     +-> linker -> ELF executable
shared libraries --------------------+                |
                                                      v
                                               execve / kernel
                                                      |
                                                .interp -> ld.so
                                                      |
                                     map + relocate + resolve symbols
                                                      |
                                                    _start -> main
```

**API source-level; ABI binary-level sözleşmedir.**

## Temel kavramlar
- Object file code/data sections, symbols ve unresolved references taşıyabilir.
- Linker symbol reference'larını çözer, section'ları yerleştirir ve executable/shared object üretir.
- Static linking gerekli code'u executable'a dahil eder; dynamic linking shared objects'i runtime'da bağlar.
- ELF `.interp` kullanılacak dynamic loader'ı belirtebilir.
- Loader dependency'leri bulur/map eder; relocation ve symbol resolution yapar.
- ABI calling convention, register/stack kullanımı, binary object formatı ve binary interface kurallarını kapsar.
- API-compatible bir değişiklik ABI-breaking olabilir; mevcut binary yeniden derlenmeden çalışmayabilir.

## Mülakat soruları
1. Compiler ile linker farkı nedir?
2. Static ve dynamic linking trade-off'ları nelerdir?
3. ABI ile API arasındaki fark nedir?
4. Relocation neden gerekir?
5. Shared-library version değişimi ne zaman binary'yi kırar?
6. Loader search path neden security boundary olabilir?
7. Staff: plugin platformunda ABI stability ve rollout nasıl yönetilir?

## Beklenen cevap seviyesi
- **Junior:** source → object → link → executable ve static/dynamic ayrımı.
- **Mid:** ELF sections/segments, symbols, relocations ve loader.
- **Senior:** ABI compatibility, search path, startup cost, versioning ve failure modes.
- **Staff:** plugin/runtime platformu, compatibility policy, supply-chain risk ve rollout governance.

## Mini alıştırma
İki C dosyası üret: biri `add()` tanımlasın, diğeri çağırsın. Ayrı `.o` dosyaları oluştur; `nm`, `readelf -h/-S/-s`, `readelf -l` ve `ldd` ile symbols, interpreter ve dependencies'i incele. Static/dynamic binary size ve startup davranışını karşılaştır.

## Proje fikri
`elf-inspector`: ELF header, program headers, dynamic dependencies ve imported/exported symbols'i özetleyen CLI geliştir. İki shared-library version'ıyla ABI-compatible ve ABI-breaking değişiklikleri CI'da test et.

## Failure modes ve trade-off
- Missing/incompatible shared object veya architecture mismatch startup failure yaratır.
- Library search-path hijacking security riskidir.
- Symbol/version uyuşmazlığı runtime load failure'a dönüşebilir.
- Static linking deployment'ı basitleştirebilir; binary size, duplication ve patch distribution maliyeti getirir.
- Çok sayıda dynamic dependency cold-start maliyetini büyütebilir.

## Production bağlantısı
Startup failure ve loader error oranı, cold-start latency, deployed library versions ve crash signatures izlenmelidir. Platform takımları ABI compatibility policy ve version lifecycle'ını açıkça yönetmelidir.

## Kaynaklar
- Linux man-pages — `ld.so`: https://man7.org/linux/man-pages/man8/ld.so.8.html
- GNU Binutils — `ld`: https://sourceware.org/binutils/docs/ld/
- System V ABI / ELF gABI: https://refspecs.linuxfoundation.org/elf/gabi4+/contents.html
