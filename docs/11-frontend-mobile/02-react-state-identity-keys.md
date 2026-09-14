# React State Identity, Keys ve Render Tree

React state'i JSX tag'inin icinde degil, render tree'deki component identity ile iliskilendirir. Ayni component ayni pozisyon ve identity ile render edilmeye devam ettiginde state korunabilir; identity degistiginde subtree resetlenebilir.

## Mental model
```text
position + component type + key
             |
             v
      component identity
        /          \
      same        changed
       |             |
 preserve       reset/remount
```

## Key neden semantiktir?
`key` yalnizca liste optimizasyonu degildir. React'in sibling'leri ayirt etmesine yardim eden identity bilgisidir. Stable domain ID genellikle dogru secimdir. Reorder edilebilen listede array index'i key yapmak state'in yanlis item ile eslesmesine neden olabilir. Rastgele key ise her render'da remount ve state kaybi yaratabilir.

Key degistirmek bazen bilincli olarak yararlidir: ornegin recipient degistiginde chat formunu veya entity degistiginde edit formunu tamamen resetlemek.

## State locality
State'i ihtiyac duyulan en yakin ortak owner'da tutmak coupling'i azaltir. Her local UI state'ini global store'a tasimak debugging ve invalidation yuzeyini buyutur. Buna karsilik birden cok sibling'in ayni source-of-truth'a ihtiyaci varsa state lifting mantiklidir.

## Mulakat sorulari
- State ne zaman korunur veya resetlenir?
- Stable key neden gerekir?
- Index key hangi durumda guvenlidir/tehlikelidir?
- Parent render olunca child remount olur mu?
- Controlled formu nasil bilincli resetlersin?
- Local ve global state sinirini nasil secersin?

## Production failure modes
Unstable key, index+reorder, nested component definition nedeniyle accidental reset, duplicated derived state, gereksiz state lifting ve buyuk subtree remount. Bunlar kaybolan form girdisi, yanlis row state'i ve gereksiz render maliyeti olarak gorunebilir.

## Kaynaklar
- React — Preserving and Resetting State: https://react.dev/learn/preserving-and-resetting-state
- React — useState: https://react.dev/reference/react/useState
