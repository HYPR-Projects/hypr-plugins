# HYPR Audiences

Plugin do catálogo de audiências de localização da HYPR.

## O que vem nele

- **Conector HYPR Audiences** (MCP remoto, sem autenticação): `https://hypr-audiences-mcp.netlify.app/mcp`. Ferramentas `search_audiences` e `list_categories`, mais prompts prontos.
- **/hypr `<termo>`**: busca rápida com volumetria. **/hypr plano `<marca/campanha>`**: plano de audiências em camadas (Core, Afinidade, Conquista, Expansão). **/hypr** sozinho lista as categorias.
- **Agente Planejador HYPR**: roda o `/hypr plano` do início ao fim em contexto próprio (briefing, ranking, camadas, plataforma, revisão de marca e deck).
- **Planejamento de audiências**: skill de conhecimento que ensina o Claude a buscar e apresentar audiências no padrão HYPR, com a taxonomia completa.

## Fonte dos dados

Google Sheets "Knowledge-audiences-HYPR". Alterações na planilha aparecem no conector em até 1 minuto.
