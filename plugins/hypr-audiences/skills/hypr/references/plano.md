# Plano de audiências (/hypr plano)

Argumento: marca e/ou campanha, com objetivo se houver (ex.: `Natura dia das mães`, `banco digital aquisição classe B`).

## 1. Extrair o briefing
Extraia: marca, categoria do produto, produto/linha, objetivo (awareness, consideração, conversão, vendas, conquista de concorrente, lançamento), público-alvo, concorrentes, ocasiões, praça, período, verba e KPIs. Use o que estiver no argumento e na conversa.
Se faltar marca E categoria, pergunte em uma linha antes de seguir. Se faltar só o objetivo, assuma awareness + consideração e declare a premissa.

## 2. Ranquear
Chame `rank_audiences` com os campos do briefing: `brand`, `category`, `product`, `objective`, `target_audience`, `keywords` (concorrentes, ocasiões, lugares) e `notes` (praça, período, verba, KPIs). Use `limit` 25 e `include_description` true.
Se precisar de mais opções num ângulo específico, complemente com `search_audiences`, mas só inclua no plano audiências que tenham `brand_affinity` vindo do `rank_audiences`.

A resposta traz três coisas além do ranking:
- `vertical`: a vertical que o conector inferiu para o briefing. Se estiver errada ou nula, repita a chamada com `category` mais explícita.
- `library_evidence` em cada audiência: em quantos planos reais da HYPR Library ela já entrou (`planos`, `planos_na_vertical`, `clientes`). É a prova de que o time de planejamento já validou a audiência nesse tipo de cliente. Use na coluna "Por que entra" sempre que existir (ex.: "já usada em 13 planos de bancos: Itaú, Nubank, BTG").
- `expansion`: audiências que costumam aparecer junto das rankeadas em planos reais (co-ocorrência), cada uma com o motivo em `why`. Elas alimentam a camada Expansão.

## 3. Montar as camadas
Distribua as audiências ranqueadas em camadas, 2 a 6 por camada:
- **Core**: afinidade Alta (75%+) ligada à categoria do produto.
- **Conquista**: audiências de marcas concorrentes (campo `brand` preenchido e diferente do anunciante), quando o objetivo permitir.
- **Afinidade**: afinidade Média (50 a 74%), hábitos e lugares que indicam o perfil.
- **Expansão**: 2 a 4 itens de `expansion` (co-ocorrência em planos reais), com o `why` resumido na justificativa ("quem planejou X também usou Y em N planos"). Se `expansion` vier vazia, use afinidade Complementar com volume alto.

## 4. Entregar
Formato fixo:

**Plano de audiências HYPR: <Marca/Campanha>**
Objetivo e premissas em 1 a 2 linhas.

Para cada camada, uma tabela: Audiência | ID (`segment_name`) | Brand Affinity | Volume | Por que entra (1 frase baseada na descrição; quando houver `library_evidence`, cite nº de planos e 2 a 3 clientes). Na camada Expansão a coluna Brand Affinity vira "Base" e recebe o motivo de co-ocorrência.

**Resumo**: nº de audiências, afinidade média ponderada pelo volume, soma bruta de volume (avisar que há sobreposição), e quantas das audiências do plano já foram validadas em planos anteriores da HYPR (contagem de itens com `library_evidence`).

**Plataforma HYPR para este plano**: abra com 1 a 2 frases do `platform_note` adaptadas ao briefing (o circuito onde, com o quê, quanto, por quê). Depois uma tabela a partir de `hypr_solutions`: Pilar | Powered by | Responde | Prioridade | Como ajuda neste caso (1 frase específica do briefing). Inclua os quatro IQs, mesmo os de prioridade Opcional, porque operam juntos; inclua Demandshift só se for Essencial ou Recomendado.

**Como vamos medir**: 1 a 2 frases sobre grupo exposto vs. controle no revIQ, com incremento no SKU e na categoria do anunciante.

**Próximos passos**: 3 itens curtos e concretos (ex.: validar praças no geoIQ, definir SKUs e categoria para leitura no revIQ, escolher formatos e canais do adsIQ).

Antes de entregar, revise o texto contra `../../planejamento-audiencias/references/marca.md`: nada de "programático", nada de bidIQ, HYPR em caixa alta, pilares em camelCase.

## 5. Deck
Ao final, gere o deck resumo seguindo `deck.md` (padrão, sem perguntar).
