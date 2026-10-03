# Deck resumo HYPR (padrão ao final de todo /hypr plano)

Depois de entregar o plano no chat, gere SEMPRE o deck .pptx, a menos que o usuário diga que não quer.

## 1. Montar o JSON do plano
O deck segue a estrutura "Audience Discovery" da HYPR: capa, sumário, seção Contexto, seção Audiências (visão das camadas, 1 slide por audiência, ranking), seção Plataforma (4 IQs, mensuração) e próximos passos.

Salve `plano.json` com:

```json
{
  "brand": "Natura",
  "campaign": "Dia das Mães 2027",
  "subtitle": "1 frase de capa (jornadas e audiências para ...).",
  "vertical": "Beleza", "region": "Nacional",
  "objective": "1 a 2 frases do objetivo (vai na seção Contexto).",
  "premises": ["Praça: ...", "Flight: ...", "Concorrente: ..."],
  "where": "Onde e quando ativar (1 frase).",
  "who": "Para quem (1 frase).",
  "how": "Como provar (1 frase, revIQ).",
  "layers": [
    {"name": "Core", "headline": "Quem já compra a categoria", "description": "1 frase do papel da camada",
     "audiences": [{
       "name": "audience_name", "id": "segment_name", "affinity": 88, "volume": 5126800, "addresses": 2300,
       "main_category": "Retail", "sub_category": "Cosmetics & Beauty", "brand": "Natura",
       "tags": ["até 3 tags curtas, ex: Datas comemorativas"],
       "why": "1 frase (até 150 caracteres) do porquê entra, baseada na descrição",
       "networks": ["opcional: até 4 redes/marcas mapeadas"],
       "image": "opcional: caminho de foto local"
     }]}
  ],
  "solutions": [{"solution": "geoIQ", "priority": "Essencial", "how": "1 frase específica do briefing, até 140 caracteres"}],
  "next_steps": ["até 4 itens curtos"],
  "max_audience_cards": 8
}
```

Regras do JSON:
- `affinity`, `volume`, `addresses`, `main_category`, `sub_category`, `brand` e `id` vêm exatamente do `rank_audiences` (`brand_affinity`, `audience_volume`, `addresses_count`, `segment_name`). Nunca invente números.
- `tags`: tire de `use_cases` ou do briefing (ocasião, comportamento). Curtas, 2 a 4 palavras.
- `networks`: use o `brand` da audiência e, se o briefing citar, marcas concorrentes relacionadas. Se não houver, omita.
- `solutions` deve ter geoIQ, adsIQ, revIQ e askIQ; inclua Demandshift só se Essencial ou Recomendado. Nunca inclua pilares internos.
- As primeiras `max_audience_cards` audiências por affinity ganham slide próprio; todas entram no ranking.
- Títulos opcionais (use *asteriscos* para a palavra em azul): `cover_title`, `cover_meta`, `context_title`, `layers_title`, `layers_sub`, `ranking_title`, `platform_title`, `platform_note`, `measurement_title`, `measurement`, `closing_title`, `closing_subtitle`, `audiences_sub`, `platform_sub`, `context_sub`.
- Siga `../planejamento-audiencias/references/marca.md` em todo texto.

## 2. Gerar
O script fica na pasta `scripts/` desta skill (mesmo diretório base do SKILL.md):

```bash
pip install python-pptx 2>/dev/null || pip install --break-system-packages python-pptx
python3 <diretório-desta-skill>/scripts/hypr_deck.py plano.json "Plano HYPR - <Marca> - <Campanha>.pptx"
```

## 3. Entregar
Entregue o .pptx ao usuário como arquivo. Diga em uma linha que o deck usa as fontes Montserrat e IBM Plex Mono (gratuitas em fonts.google.com; sem elas o PowerPoint substitui por outras).

Se o ambiente não permitir rodar Python (ex.: navegador), não gere o deck e ofereça entregar o JSON ou o plano em tabela.
