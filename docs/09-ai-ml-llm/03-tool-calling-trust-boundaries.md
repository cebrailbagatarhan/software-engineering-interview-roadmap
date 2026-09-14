# LLM Tool Calling, Structured Outputs & Trust Boundaries

Model tool'u doğrudan güvenilir biçimde çalıştıran bir program değildir. Model structured arguments önerir; uygulama validation, authorization ve execution kontrolünü elinde tutar.

```text
User -> Model -> proposed call -> Policy/AuthZ -> Executor -> API
```

Structured Outputs schema uyumunu güçlendirebilir fakat semantik doğruluk veya yetki garantisi değildir. Tool executor argument bounds, caller identity, least privilege, idempotency, timeout, audit ve gerektiğinde human approval uygulamalıdır. Tool output da untrusted input kabul edilmelidir; dış içerik prompt injection taşıyabilir.

## Staff/Principal beklentisi
Schema validation ile security policy'yi ayır; authorization'ı modele bırakma. Side-effecting operasyonlarda idempotency ve approval boundary kur. Credentials'ı minimum scope ile sınırla. Tool sonuçlarını yeni bir trust boundary olarak ele al. Audit trail ve failure isolation tasarla.

## Failure modes
Schema-valid fakat yanlış çağrı, over-privileged credential, duplicate side effect, tool-result injection, authorization'ın prompt'a bırakılması ve yetersiz audit.

## Kaynaklar
- https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api
- https://openai.com/index/introducing-structured-outputs-in-the-api/
