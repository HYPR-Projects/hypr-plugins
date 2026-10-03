---
name: audiencias
description: Busca rápida no catálogo de audiências HYPR. Use when the user types "/audiencias <termo>" or asks "tem audiência de X na HYPR?", "volume de visitantes de Y", "lista as audiências de Z".
---

# /audiencias

Argumento: termo de busca livre (ex.: `pet`, `postos`, `Financial Services`, `Natura`). Sem argumento, chame `list_categories` e mostre as categorias com nº de audiências e volume, depois sugira 3 buscas.

1. Chame `search_audiences` com `query` = termo, `limit` 15, `include_description` false.
2. Se o termo for exatamente uma categoria ou subcategoria da taxonomia (ver skill planejamento-audiencias), use o filtro correspondente em vez de `query`, com `sort: volume_desc`.
3. Se vier vazio, tente um sinônimo (PT↔EN) ou termo mais curto antes de responder que não existe.
4. Responda com:
   - Uma linha: "N audiências encontradas para <termo>".
   - Tabela: Audiência | ID (`segment_name` em código) | Subcategoria | Volume (ex.: 12,4 mi) | Endereços.
   - Se `total_matches` > retornadas, diga quantas ficaram de fora e como refinar.
5. Ofereça em uma linha ver a descrição de alguma audiência ou montar um plano com `/plano-midia`.
