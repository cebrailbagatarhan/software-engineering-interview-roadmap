# Dependabot Private Registry Auth, Least Privilege & Credential Elimination

## Konu anlatımı
Private registry automation klasik olarak uzun ömürlü PAT veya registry secret kullanabilir. Static credential'lar rotation, scope ve exfiltration yüzeyi yaratır. 8 Eylül 2026 itibarıyla Dependabot, GitHub-hosted private registry'lerde repository/package access grant'lerini kullanarak `GITHUB_TOKEN` ile `packages: read` isteyebilir; explicit registry credentials ve normal routing önceliğini korurken bu kimlik fallback authentication olarak kullanılabilir.

```text
Dependabot job
   |
ephemeral token -- packages:read --> package access grant --> registry

fewer static secrets != no governance
```

## Mental model
Authentication kim olduğunuzu, authorization hangi package ve operation'a erişebildiğinizi belirler. Ephemeral identity shared PAT'e göre blast radius'u azaltabilir; fakat overbroad veya stale access grants privilege creep yaratır.

## Mülakat soruları
- Static PAT ve ephemeral token trade-off'u nedir?
- Least privilege neden yalnız token scope değildir?
- Dependency confusion private registry tasarımını nasıl etkiler?
- Staff seviyesinde yüzlerce repo/package için grant lifecycle nasıl yönetilir?

## Production bağlantısı
Auth failures, package access denials, static-secret count, grant age, dependency-update success ve audit anomalies izlenmelidir. Shared credentials, stale grants, routing ambiguity ve token logging temel failure mode'lardır.

## Kaynaklar
- https://github.blog/changelog/2026-09-08-automatic-dependabot-access-to-github-hosted-registries/
- https://docs.github.com/code-security/dependabot/working-with-dependabot/configuring-access-to-private-registries-for-dependabot
- https://docs.github.com/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility
