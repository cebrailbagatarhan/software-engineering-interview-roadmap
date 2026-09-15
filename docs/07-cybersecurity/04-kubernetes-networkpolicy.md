# Kubernetes NetworkPolicy: Default-Deny & Egress Control

## Model
NetworkPolicy L4 connectivity'yi pod/namespace selectors ve IP blocks ile sınırlar. Policy resource tek başına enforcement değildir; kullanılan network plugin/CNI NetworkPolicy'yi uygulamalıdır.

```text
[frontend] --443--> [api] --5432--> [db]
                       |
                       +--> DNS / approved external dependency
other flows: deny
```

## Default-deny
Önce workload'u ingress/egress için isolate edip yalnız gerekli akışları allow-list etmek blast radius'u küçültür. Production rollout'ta dependency inventory ve connectivity telemetry gerekir; DNS, identity, metrics ve external APIs unutulursa outage oluşabilir.

## Güvenlik sınırı
Network segmentation application authentication/authorization'ın yerine geçmez. Egress control compromised workload'un exfiltration/C2 seçeneklerini azaltabilir fakat node/host networking, external IP değişkenliği ve CNI davranışı ayrıca modellenmelidir.

## Interview checklist
- ingress vs egress
- podSelector / namespaceSelector / ipBlock
- additive allow semantics
- CNI enforcement capability
- default-deny rollout
- DNS/external dependency
- observability ve break-glass

## Kaynak
- https://kubernetes.io/docs/concepts/services-networking/network-policies/
