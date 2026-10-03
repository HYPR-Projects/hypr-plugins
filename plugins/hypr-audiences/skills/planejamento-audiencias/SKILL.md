---
name: planejamento-audiencias
description: This skill should be used when the user asks about HYPR audiences, audience volumes, or which audiences fit a brand, campaign or media plan, e.g. "quais audiências da HYPR servem para uma marca de ração", "qual o volume de visitantes de postos", "monta um plano de audiências", "audiências para campanha de dia das mães", "HYPR audience for banking". Teaches how to query the HYPR Audiences connector and present results the HYPR way.
---

# Planejamento de audiências HYPR

A HYPR é uma empresa brasileira de adtech e inteligência espacial. O catálogo tem cerca de 500 audiências de localização: grupos de pessoas que visitaram um conjunto de lugares físicos (redes de varejo, agências bancárias, postos, universidades etc.). A HYPR é privacy by design e não trabalha com dados pessoais identificáveis (PII). Nunca descrever a HYPR como "data provider".

## Ferramentas do conector `hypr-audiences`

- `search_audiences`: busca por palavras em nome, marca, categoria, keywords e descrição. Filtros: `main_category`, `sub_category`, `type`, `min_volume`. Ordenação: `relevance`, `volume_desc`, `volume_asc`. Use `include_description: false` para listas longas.
- `rank_audiences`: recebe o briefing (brand, category, product, objective, target_audience, keywords, notes) e devolve audiências ranqueadas com `brand_affinity` (0 a 100%) e faixa Alta/Média/Complementar, mais `hypr_solutions` com as soluções HYPR recomendadas. Use sempre que houver uma marca ou campanha.
- `list_categories`: categorias, subcategorias, nº de audiências e volume somado.

A taxonomia completa está em `references/taxonomia.md`. Use os nomes exatos dela nos filtros.

## Como buscar bem

1. Quebre o briefing em 3 a 6 ângulos de comportamento físico. Ex.: marca de ração premium → pet shops, clínicas veterinárias, redes pet específicas, bairros de renda alta (supermercados premium), parques.
2. Rode uma busca por ângulo com termos curtos (1 a 2 palavras). A busca exige todas as palavras, então "banco premium" é mais restritivo que "banco".
3. Se vier resultado demais, filtre por `main_category`/`sub_category` ou `min_volume`. Se vier vazio, tente sinônimo em inglês ou o nome da marca.
4. Prefira audiências de marca (coluna `brand`) quando o anunciante quer conquistar clientes da concorrência ou de redes parceiras.

## Brand Affinity

- É uma afinidade ESTIMADA pelo cruzamento do briefing com o catálogo, não uma medição de comportamento. Chame de "Brand Affinity" e, se perguntarem, explique assim.
- Mostrar como porcentagem inteira (ex.: 87%). Faixas: Alta 75%+, Média 50 a 74%, Complementar abaixo de 50%.
- Quanto mais completo o briefing (concorrentes, ocasiões, público), melhor o ranking. Se o resultado parecer genérico, peça 1 ou 2 dados que faltam.

## Soluções HYPR

Recomendar a partir de `hypr_solutions`, sempre conectando ao briefing:
- **geoIQ**: inteligência de localização, ativa e analisa audiências a partir de visitas a lugares físicos.
- **revIQ**: medição de resultado, conecta exposição a impacto em vendas e receita.
- **bidIQ**: otimização da compra de mídia e dos lances para o melhor custo por resultado.
- **adIQ**: inteligência de anúncios, mensagem e criativo por audiência.
- **Groundflow**: infraestrutura de dados transacionais via notas fiscais, com mais de R$ 3,16 trilhões em GMV processado.
- **Demandshift**: IA de análise de demanda, 350 milhões de notas fiscais e transações, mais de 500 categorias (FMCG, Auto, Real Estate, Upscale Retailers).

Nunca usar a palavra "programática" (nem "programático"). Não citar parceiros, plataformas ou integrações de mídia pelo nome.

## Regras de apresentação

- Volume em formato brasileiro abreviado: 12,4 mi, 850 mil.
- Sempre mostrar o nome legível (`audience_name`) e o ID técnico (`segment_name`) em fonte de código, pois o ID é o que vai para a plataforma de mídia.
- Não somar volumes como se fosse alcance único: as audiências se sobrepõem. Ao totalizar, dizer "soma bruta (há sobreposição)".
- Não inventar audiências, volumes ou dados que o conector não retornou. Se algo não existir no catálogo, dizer e sugerir a mais próxima.
- Tom direto, sem jargão vazio, sem travessão.

## Formato padrão de resposta para consultas simples

Tabela com: Audiência | ID | Categoria | Volume | Endereços. Depois, uma linha de leitura com o principal insight.
