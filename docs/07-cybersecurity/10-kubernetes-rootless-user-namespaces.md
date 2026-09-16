# Kubernetes Rootless Nodes, User Namespaces & Privilege Boundaries

## Neden önemli?
Kubernetes v1.37'de `KubeletInUserNamespace` Beta'ya geçti. Kubelet, CRI/OCI runtime, CNI plugin'leri ve kube-proxy host üzerinde root olmayan kullanıcı olarak Linux user namespace içinde çalışabilir.

## Mental model
Rootless node ile pod user namespace farklı katmanlardır. `hostUsers: false` pod'un UID/GID mapping'ini değiştirir; rootless node ise node component'lerinin host privilege boundary'sini değiştirir.

```text
host unprivileged UID
  -> node user namespace
      -> kubelet / runtime / networking
          -> optional pod user namespace
```

Namespace içindeki UID 0 host UID 0 olmak zorunda değildir. Bu compromise blast radius'unu azaltabilir, fakat VM/sandbox isolation ile eşdeğer değildir.

## Production trade-off'ları
Networking, storage, device access, observability ve debugging araçları root privilege varsayabilir. Rootless adoption workload classification, CNI/CSI compatibility tests, canary node pools ve explicit exception governance gerektirir.

İzlenecek sinyaller: privileged workload count, scheduling failures, CNI/CSI errors, denied operations, exception inventory ve privilege/escape audit events.

## Mülakat ekseni
Senior aday namespace/capability ve compatibility yüzeyini; Staff aday fleet rollout ve exception governance'ı; Principal/CTO threat-model, compliance ve platform cost dengesini açıklayabilmelidir.

## Kaynaklar
- https://kubernetes.io/blog/2026/09/04/kubernetes-v1-37-rootless-beta/
- https://kubernetes.io/docs/concepts/workloads/pods/user-namespaces/
- https://www.kernel.org/doc/html/latest/admin-guide/namespaces/index.html
