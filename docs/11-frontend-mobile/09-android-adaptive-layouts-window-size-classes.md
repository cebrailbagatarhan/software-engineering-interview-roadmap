# Android Adaptive Layouts, Window Size Classes & State Preservation

## Neden önemli?
Android UI artık cihaz modeline değil uygulamaya ayrılan gerçek window alanına göre tasarlanmalıdır. Telefon, tablet, foldable, desktop windowing ve multi-window aynı uygulamanın runtime context'leridir.

## Mental model
```text
available window -> metrics -> size class/posture -> layout mode
                                  |
                 compact / medium / expanded
                                  |
                         state must survive change
```

## Responsive vs adaptive
Responsive layout aynı yapıyı mevcut alana göre esnetir. Adaptive layout breakpoint'te yapıyı değiştirebilir. Compact window'da list->detail navigation kullanılırken expanded window'da list ve detail aynı anda gösterilebilir. Material 3 Adaptive, canonical layout building block'ları sağlar.

## Window size class neden device type'tan iyi?
Fiziksel ekran boyutu uygulamanın gerçekten kullanabildiği alan değildir. Split-screen, freeform windowing veya fold state aynı cihazda farklı kullanılabilir alan üretir. Bu nedenle window metrics ve size class layout için daha doğru abstraction'dır.

## State preservation
Resize, rotation ve fold/unfold activity recreation veya composition değişimi yaratabilir. UI state, navigation/selection state ve domain/data state farklı lifetime'lara sahiptir. ViewModel ve saved-state mekanizmaları doğru state türüne uygulanmalıdır. Pane sayısı değişince kullanıcı context'i kaybolmamalıdır.

## Interview depth
- Junior: responsive UI, orientation, lifecycle.
- Mid: window metrics, size classes, state restoration.
- Senior: navigation, performance, testing matrix, recomposition.
- Staff: design-system standardı, canonical layouts, legacy migration.
- Principal/CTO: device reach, accessibility, QA cost ve product economics.

## Failure modes
Device modeline göre layout seçmek; portrait lock'a güvenmek; büyük ekranda telefonu yalnız stretch etmek; breakpoint başına business logic fork etmek; pane transition sırasında selection state kaybetmek.

## Production
Window-class dağılımı, state-restoration failures, crashes, rendering jank, form-factor funnel ve accessibility telemetry izlenir.

## Mini proje
Compose + Material 3 Adaptive ile list/detail uygulaması kur. Window resize, fold/unfold, process recreation, keyboard/mouse ve state restoration testleri ekle.

## Kaynaklar
- https://developer.android.com/develop/adaptive-apps/guides/support-different-display-sizes
- https://developer.android.com/develop/adaptive-apps/guides/app-orientation-aspect-ratio-resizability
- https://developer.android.com/jetpack/androidx/releases/compose-material3-adaptive
- https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/tier-2
