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

**Soluções HYPR recomendadas**: tabela a partir de `hypr_solutions`, só com prioridade Essencial e Recomendado, mais Opcional se o briefing pedir algo que só ele atende: Solução | Prioridade | Como ajuda neste caso (1 frase específica do briefing, partindo de `what_it_does` e `why`).

**Próximos passos**: 3 itens curtos e concretos.

Ao final, ofereça em uma linha exportar o plano como planilha ou deck.
