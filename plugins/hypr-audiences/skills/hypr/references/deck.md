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
       "eixo": "Comportamento | Afinidade | Proximidade | Censitária | Mobilidade | Lifestyle",
       "cluster": "rótulo curto em ciano, ex: Presentes & datas (default: sub_category)",
       "praca": "Nacional",
       "places": [{"n": 3360, "l": "Perfumarias"}, {"n": 604, "l": "Shopping centers"}, {"n": 1412, "l": "Chocolaterias"}],
       "hooks": ["exatamente 2 ganchos curtos, ex: Datas comemorativas", "Ticket alto em presente"],
       "why": "texto curto, 2 linhas no máximo (até 150 caracteres)",
       "profile": "AB · 25–54 · Nacional",
       "networks": ["até 4 redes mapeadas", {"name": "Rede ainda não confirmada", "off": true}],
       "image": "opcional: caminho de foto local",
       "image_caption": "opcional: legenda mono do espaço reservado, ex: [ perfumaria · pdv ]"
     }]}
  ],
  "solutions": [{"solution": "geoIQ", "priority": "Essencial", "how": "1 frase específica do briefing, até 140 caracteres"}],
  "next_steps": ["até 4 itens curtos"],
  "max_audience_cards": 8
}
```

Regras do JSON:
- `affinity`, `volume`, `addresses`, `main_category`, `sub_category`, `brand` e `id` vêm exatamente do `rank_audiences` (`brand_affinity`, `audience_volume`, `addresses_count`, `segment_name`). Nunca invente números.
- Quando a audiência tiver `library_evidence`, use um dos `hooks` para isso ("Validada em 13 planos de bancos" ou "Já usada com Itaú, Nubank e BTG"). Audiências vindas de `expansion` não têm affinity: use `affinity: null` e coloque o `why` de co-ocorrência no campo `why`.
- O card de audiência segue o contrato do HYPR Design System (8 slots fixos). Se um dado não existir, o slot fica vazio; nunca troque por outra coisa.
- `eixo` é enum fechado: Comportamento, Afinidade, Proximidade, Censitária, Mobilidade, Lifestyle. Se omitir, o script deriva da camada (Core/Conquista → Comportamento, Afinidade → Afinidade, Expansão → Lifestyle).
- `places`: 3 contagens de endereços por tipo de lugar, só se você tiver os números (ex.: do briefing ou do cliente). Nunca invente. Sem `places`, o script mostra endereços mapeados, Brand Affinity e posição no ranking.
- `hooks`: exatamente 2, começando sem "+" (o script adiciona). Tire de `use_cases` ou do briefing.
- `profile`: linha de perfil no padrão `AB · 25–54 · SP & RJ`. Só com dados do briefing; senão omita (o script mostra o ID).
- `networks`: o `brand` da audiência e, se o briefing citar, redes relacionadas. Marque `"off": true` para inventário ainda não confirmado. Se não houver, omita.
- O deck mostra 4 cards de audiência (`max_audience_cards`, padrão 4, como manda o DS) e todas as demais no ranking.
- O rodapé direito é uma única string praça · período, igual em todos os slides (`footer_right`, default `<region> · <ano>`). Nunca mude no meio do deck.
- Títulos em sentence case, com UMA palavra em ciano e ponto final. Sem exclamação, sem emoji, sem Title Case.
- Sem `image`, o slide reserva o espaço da foto como manda o DS: moldura hairline, raio 20 e legenda mono. Nunca peça para preencher com decoração; quem tem a foto aprovada coloca depois.
- Cores de dado: verde só para boa notícia, rosa só para má notícia (favorabilidade, não direção). O ranking usa só ciano e neutros.
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
Entregue o .pptx ao usuário como arquivo. Diga em uma linha que o deck usa as fontes Urbanist e IBM Plex Mono (as duas do HYPR Design System, gratuitas em fonts.google.com; sem elas o PowerPoint substitui por outras).

Se o ambiente não permitir rodar Python (ex.: navegador), não gere o deck e ofereça entregar o JSON ou o plano em tabela.
