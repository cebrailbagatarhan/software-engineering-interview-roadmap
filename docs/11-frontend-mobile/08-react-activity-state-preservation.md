# React 19.2 Activity: State Preservation & Hidden Work

## Konu anlatımı
React 19.2 `<Activity>` UI alt ağaçlarını `visible` ve `hidden` lifecycle'larıyla yönetir. Hidden activity görünmez, Effect'leri unmount edilir ve güncellemeleri düşük önceliğe alınır; component state korunabildiği için conditional unmount'tan farklıdır.

## Mental model
```text
visible -> hidden: state korunur, effects cleanup, work deprioritized
hidden -> visible: state geri kullanılır, effects remount
```

## Internals / trade-off
Activity bir data cache değildir; UI lifecycle ve scheduling primitive'idir. State preservation UX'i hızlandırabilir fakat hidden subtree memory, background rendering ve olası data-fetch maliyeti taşır. Effect cleanup correctness kritiktir.

## Mülakat odağı
- Conditional rendering ve CSS hiding farkı
- State vs Effect lifecycle
- Pre-render ve back-navigation
- Memory/CPU/network budget
- Fleet/device-class rollout metrics

## Alıştırma / proje
Üç tab'lı editörde state'i koruyup yalnız visible tab'ın websocket subscription'ını açık tut. Conditional render ve Activity sürümlerini navigation latency, memory ve effect-count ile benchmark et.

## Failure modes / production
Activity'yi ücretsiz cache sanmak, cleanup sızıntısı, aşırı pre-render, düşük güçlü cihazları atlamak. Navigation latency, memory, long task, background request ve state-loss metriği izle.

## Kaynaklar
- https://react.dev/blog/2025/10/01/react-19-2
- https://react.dev/blog/2025/04/23/react-labs-view-transitions-activity-and-more
