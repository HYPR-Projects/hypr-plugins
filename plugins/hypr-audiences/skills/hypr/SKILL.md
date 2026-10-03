---
name: hypr
description: Comando único do catálogo de audiências HYPR. Use when the user types "/hypr", "/hypr seguido de um tema" or "/hypr plano seguido da marca ou campanha", or asks "tem audiência de X na HYPR?", "volume de visitantes de Y", "monta um plano de audiências HYPR para Z".
---

# /hypr

Decida o modo pelo argumento:

- **Sem argumento**: chame `list_categories`, mostre as categorias com nº de audiências e volume, e sugira 3 exemplos de uso: `/hypr pet`, `/hypr Financial Services`, `/hypr plano Natura dia das mães`.
- **Começa com "plano"** (ou pede plano, proposta, recomendação para uma marca/campanha): delegue ao agente `planejador-hypr` com o resto do argumento como briefing. Ele roda o fluxo inteiro (`references/plano.md` e `references/deck.md`) e devolve plano + deck. Se o agente não estiver disponível, siga `references/plano.md` você mesmo.
- **Qualquer outro termo**: busca rápida, abaixo.

## Busca rápida

1. Chame `search_audiences` com `query` = termo, `limit` 15, `include_description` false.
2. Se o termo for exatamente uma categoria ou subcategoria da taxonomia (ver skill planejamento-audiencias), use o filtro correspondente em vez de `query`, com `sort: volume_desc`.
3. Se vier vazio, tente um sinônimo (PT↔EN) ou termo mais curto antes de dizer que não existe.
4. Responda com:
   - Uma linha: "N audiências encontradas para <termo>".
   - Tabela: Audiência | ID (`segment_name` em código) | Subcategoria | Volume (ex.: 12,4 mi) | Endereços.
   - Se `total_matches` > retornadas, diga quantas ficaram de fora e como refinar.
5. Ofereça em uma linha ver a descrição de alguma audiência ou montar um plano com `/hypr plano <marca>`.
