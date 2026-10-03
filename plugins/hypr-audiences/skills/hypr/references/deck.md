# Deck resumo HYPR (padrão ao final de todo /hypr plano)

Depois de entregar o plano no chat, gere SEMPRE o deck .pptx, a menos que o usuário diga que não quer.

## 1. Montar o JSON do plano
Salve um arquivo `plano.json` com:

```json
{
  "brand": "Natura",
  "campaign": "Dia das Mães 2027",
  "objective": "1 a 2 frases do objetivo.",
  "premises": ["Praça: ...", "Flight: ...", "Concorrente: ..."],
  "briefing": {"Marca": "...", "Categoria": "...", "Objetivo": "...", "Público": "...", "Ocasião": "...", "KPI": "..."},
  "layers": [
    {"name": "Core", "description": "momento de compra da categoria",
     "audiences": [{"name": "audience_name", "id": "segment_name", "affinity": 88, "volume": 5126800, "why": "1 frase curta"}]}
  ],
  "solutions": [{"solution": "geoIQ", "priority": "Essencial", "how": "1 frase específica do briefing, até 140 caracteres"}],
  "next_steps": ["até 4 itens curtos"]
}
```

Regras do JSON:
- `affinity` e `volume` vêm exatamente do `rank_audiences`. Nunca invente.
- `solutions` deve ter geoIQ, adsIQ, revIQ e askIQ; inclua Demandshift só se for Essencial ou Recomendado. Nunca inclua pilares internos.
- `why` com no máximo 120 caracteres; `how` com no máximo 140.
- Campos opcionais para personalizar títulos (use *asteriscos* para destacar em azul): `campaign_title`, `subtitle`, `briefing_title`, `summary_title`, `layers_title`, `platform_title`, `platform_note`, `measurement`, `measurement_title`, `closing_title`, `closing_subtitle`, `date`.
- Siga `../planejamento-audiencias/references/marca.md` em todo texto.

## 2. Gerar
O script fica na pasta `scripts/` desta skill (mesmo diretório base do SKILL.md):

```bash
pip install python-pptx 2>/dev/null || pip install --break-system-packages python-pptx
python3 <diretório-desta-skill>/scripts/hypr_deck.py plano.json "Plano HYPR - <Marca> - <Campanha>.pptx"
```

## 3. Entregar
Entregue o .pptx ao usuário como arquivo. Diga em uma linha que o deck usa a fonte Montserrat (se ela não estiver instalada, o PowerPoint substitui por outra; instalação gratuita em fonts.google.com).

Se o ambiente não permitir rodar Python (ex.: navegador), não gere o deck e ofereça entregar o JSON ou o plano em tabela.
