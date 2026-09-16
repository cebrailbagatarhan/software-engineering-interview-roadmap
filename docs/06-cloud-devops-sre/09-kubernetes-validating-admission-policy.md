# Kubernetes ValidatingAdmissionPolicy, CEL & Policy Failure Modes

## Konu anlatımı
Kubernetes admission, authentication ve authorization sonrasında fakat object kalıcı hale gelmeden önce policy uygulamak için kritik kontrol noktasıdır. `ValidatingAdmissionPolicy` (VAP), CEL ifadelerini API server içinde değerlendirerek validating webhook'a declarative, in-process bir alternatif sağlar ve Kubernetes v1.30'dan beri stable'dır.

Policy soyut kuralı tanımlar; `ValidatingAdmissionPolicyBinding` policy'yi scope ve parametrelerle somutlaştırır. `Deny`, `Warn` ve `Audit` rollout davranışlarıdır. Param resource aynı policy mantığını farklı tenant limitleriyle kullanmayı sağlar.

## Mental model
```text
request -> authn -> authz -> admission match
                              |
                    policy + binding + params
                              |
                             CEL
                              |
                       Deny/Warn/Audit
                              |
                           persist
```

## İçeride ne oluyor?
VAP CEL'i API server process'i içinde çalıştırır; network hop/webhook availability bağımlılığı yoktur. CEL cost budget, match scope ve failure policy control-plane safety'nin parçasıdır. Binding/param seçimi evaluation sayısını artırabilir. External data veya custom service logic gerektiğinde webhook hâlâ uygundur.

## Mülakat soruları
- Admission authn/authz'dan nasıl ayrılır?
- VAP vs validating webhook trade-off'u?
- Policy ve Binding neden ayrıdır?
- Warn'dan Deny'a güvenli rollout nasıl yapılır?
- failurePolicy availability/security dengesini nasıl etkiler?
- Staff: fleet policy drift ve break-glass nasıl yönetilir?

## Beklenen cevap seviyesi
Mid: admission sırası ve CEL. Senior: binding/params, rollout, failure semantics. Staff: fleet governance, blast radius ve exception lifecycle. Principal/CTO: compliance, developer velocity ve ownership.

## Mini alıştırma
`latest` image tag'ini önce Warn sonra Deny edecek policy rollout'unun scope, exception ve metric planını yaz.

## Proje fikri
`vap-policy-lab`: CEL test corpus'u, warn rollout, namespace parametreleri ve rejection metrics'i olan policy CI sistemi.

## Production bağlantısı / failure modes
Doğrudan Deny rollout; geniş match scope; param yokluğu; pahalı CEL; break-glass eksikliği. Rejection/warn rate, admission latency, policy version, exception count ve failed deploy oranını izle.

## Kaynaklar
- https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/
- https://kubernetes.io/docs/tutorials/cluster-management/admission-policies/
- https://kubernetes.io/docs/concepts/policy/
