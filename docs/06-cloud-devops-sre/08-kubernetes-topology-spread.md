# Kubernetes Topology Spread Constraints

Replica sayısı tek başına availability garantisi değildir; replica'lar aynı failure domain'e yığılabilir.

```text
zone-a: pod1 pod3
zone-b: pod2 pod4
```

`topologyKey` failure domain'i, `maxSkew` dağılım farkını, `whenUnsatisfiable` ise kural karşılanamadığında scheduler davranışını tanımlar. `DoNotSchedule` sert; `ScheduleAnyway` tercih niteliğindedir.

Senior seviyede topology spread kapasite, autoscaling, rollout ve Pending Pod riskiyle birlikte düşünülmelidir. Staff seviyesinde replica count, PDB, topology ve multi-zone capacity tek availability tasarımının parçalarıdır.

## Failure modes
Eksik topology label, yetersiz zone capacity, aşırı sert constraint, autoscaler uyumsuzluğu ve replica sayısını HA sanmak.

## Kaynak
- https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/
