
# Plano de audiências (/hypr plano)

Argumento: marca e/ou campanha, com objetivo se houver (ex.: `Natura dia das mães`, `banco digital aquisição classe B`).

## 1. Entender o briefing
Extraia do argumento e da conversa: anunciante, categoria do produto, objetivo (awareness, consideração, conversão, conquista de concorrente), público-alvo e praça. Se faltar só o objetivo, assuma awareness + consideração e diga isso no plano. Não pare para perguntar se der para inferir.

## 2. Montar a estratégia em camadas
Defina 3 a 4 camadas, cada uma com 2 a 5 audiências:
- **Core**: quem já está no momento de compra da categoria (ex.: visitantes de lojas da categoria, concorrentes).
- **Afinidade**: hábitos e lugares que indicam o perfil (ex.: academias, pet shops, universidades).
- **Conquista**: clientes de marcas concorrentes, quando fizer sentido.
- **Expansão** (opcional): audiências de alto volume para escala.

Busque cada ideia com `search_audiences` (termos curtos, um ângulo por chamada; use `include_description: true` nas finalistas para justificar). Use apenas audiências que o conector retornou.

## 3. Entregar
Formato fixo:

**Plano de audiências HYPR: <Marca/Campanha>**
Objetivo e premissas em 1 a 2 linhas.

Para cada camada, uma tabela: Audiência | ID (`segment_name`) | Volume | Por que entra (1 frase, baseada na descrição).

**Resumo**: nº de audiências, soma bruta de volume (avisar que há sobreposição), e 2 a 3 recomendações de ativação (ex.: geofence de concorrentes em período promocional, priorizar Core no início do flight).

**Próximos passos**: lista curta (validar praças, cruzar com dados Groundflow/Demandshift se o cliente quiser leitura de demanda, definir janela de lookback).

Volumes no padrão brasileiro abreviado (12,4 mi). Sem travessão. Sem inventar números.

Ao final, ofereça em uma linha exportar o plano como planilha ou deck.
