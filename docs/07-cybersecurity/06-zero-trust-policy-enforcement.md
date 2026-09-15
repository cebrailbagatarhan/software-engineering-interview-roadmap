# Zero Trust, Policy Decision/Enforcement & Identity-Aware Access

## Konu anlatımı
Zero Trust network location veya asset ownership nedeniyle implicit trust verilmemesi ilkesidir. NIST SP 800-207 odağı network segmentinden resource'a taşır. Access decision subject, device, resource ve bağlamsal sinyaller üzerinden explicit policy ile üretilir.

Policy Enforcement Point (PEP) isteği yakalar ve kararı uygular. Policy decision katmanı identity, device posture, resource sensitivity ve threat/context sinyallerini değerlendirir. Authentication ve authorization ayrıdır; human identity kadar workload identity de cloud-native sistemlerde kritiktir.

## Mental model
```text
subject/device -> PEP -> resource
                  | ^
                  v |
               policy decision
              / identity
             / device posture
            / resource + context
```

## Mülakat soruları
- Zero Trust'ın temel invariant'ı nedir?
- VPN neden tek başına Zero Trust değildir?
- PDP ile PEP nasıl ayrılır?
- Device posture freshness neden önemlidir?
- Policy service outage'ında fail-open/fail-closed nasıl seçilir?
- Legacy portfolio'ya migration nasıl fazlanır?

## Beklenen cevap seviyesi
Mid: no implicit trust ve least privilege. Senior: PDP/PEP, device/resource context ve workload identity. Staff: availability, telemetry freshness, break-glass ve migration. CTO: portfolio risk segmentation, governance ve vendor interoperability.

## Mini alıştırma
Payroll sistemi için employee, contractor, managed/unmanaged device ve service account erişim matrisi çıkar; deny ve break-glass davranışlarını belirt.

## Proje fikri
`zero-trust-policy-lab`: reverse proxy + policy engine ile JWT identity, device posture ve resource classification tabanlı karar ver; decision latency ve deny reason ölç.

## Failure modes / production
VPN'i yeni implicit trust boundary yapmak, policy engine'i single point of failure bırakmak, stale posture kabul etmek, service account'lara geniş kalıcı yetki vermek ve break-glass audit'ini ihmal etmek temel risklerdir.

## Kaynaklar
- https://csrc.nist.gov/pubs/sp/800/207/final
- https://www.nist.gov/programs-projects/zero-trust-networks
