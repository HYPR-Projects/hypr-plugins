# Plano de audiências (/hypr plano)

Argumento: marca e/ou campanha, com objetivo se houver (ex.: `Natura dia das mães`, `banco digital aquisição classe B`).

## 1. Extrair o briefing
Extraia: marca, categoria do produto, produto/linha, objetivo (awareness, consideração, conversão, vendas, conquista de concorrente, lançamento), público-alvo, concorrentes, ocasiões, praça, período, verba e KPIs. Use o que estiver no argumento e na conversa.
Se faltar marca E categoria, pergunte em uma linha antes de seguir. Se faltar só o objetivo, assuma awareness + consideração e declare a premissa.

## 2. Ranquear
Chame `rank_audiences` com os campos do briefing: `brand`, `category`, `product`, `objective`, `target_audience`, `keywords` (concorrentes, ocasiões, lugares) e `notes` (praça, período, verba, KPIs). Use `limit` 25 e `include_description` true.
Se precisar de mais opções num ângulo específico, complemente com `search_audiences`, mas só inclua no plano audiências que tenham `brand_affinity` vindo do `rank_audiences`.

## 3. Montar as camadas
Distribua as audiências ranqueadas em camadas, 2 a 6 por camada:
- **Core**: afinidade Alta (75%+) ligada à categoria do produto.
- **Conquista**: audiências de marcas concorrentes (campo `brand` preenchido e diferente do anunciante), quando o objetivo permitir.
- **Afinidade**: afinidade Média (50 a 74%), hábitos e lugares que indicam o perfil.
- **Expansão** (opcional): afinidade Complementar com volume alto, para escala.

## 4. Entregar
Formato fixo:

**Plano de audiências HYPR: <Marca/Campanha>**
Objetivo e premissas em 1 a 2 linhas.

Para cada camada, uma tabela: Audiência | ID (`segment_name`) | Brand Affinity | Volume | Por que entra (1 frase baseada na descrição).

**Resumo**: nº de audiências, afinidade média ponderada pelo volume, soma bruta de volume (avisar que há sobreposição).

**Plataforma HYPR para este plano**: abra com 1 a 2 frases do `platform_note` adaptadas ao briefing (o circuito onde, com o quê, quanto, por quê). Depois uma tabela a partir de `hypr_solutions`: Pilar | Powered by | Responde | Prioridade | Como ajuda neste caso (1 frase específica do briefing). Inclua os quatro IQs, mesmo os de prioridade Opcional, porque operam juntos; inclua Demandshift só se for Essencial ou Recomendado.

**Como vamos medir**: 1 a 2 frases sobre grupo exposto vs. controle no revIQ, com incremento no SKU e na categoria do anunciante.

**Próximos passos**: 3 itens curtos e concretos (ex.: validar praças no geoIQ, definir SKUs e categoria para leitura no revIQ, escolher formatos e canais do adsIQ).

Antes de entregar, revise o texto contra `../../planejamento-audiencias/references/marca.md`: nada de "programático", nada de bidIQ, HYPR em caixa alta, pilares em camelCase.

Ao final, ofereça em uma linha exportar o plano como planilha ou deck.
