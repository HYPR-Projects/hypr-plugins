# HYPR plugins para Claude (hypr-plugins)

> Mapa do projeto, no modelo de README da HYPR. O guia de instalação e uso para o time e para clientes está em [docs/README_ANTERIOR.md](docs/README_ANTERIOR.md).
> Objetivo: uma pessoa nova, ou o assistente de IA, roda e ajusta o projeto sem perguntar a ninguém.

## O que é
Marketplace de plugins da HYPR para o Claude (app desktop e Claude Code). Hoje tem um plugin, **HYPR Audiences**: consulta o catálogo de audiências de localização da HYPR, mostra volumes e monta planos de audiência com deck para qualquer marca.
Pilar: **geoIQ**.

O plugin é fino. A lógica e os dados ficam no conector MCP `hypr-audiences` (repo `HYPR-Projects/hypr-audiences-mcp`). Aqui ficam o comando `/hypr`, o agente `planejador-hypr` e a skill de conhecimento.

> **Repositório público.** Tudo o que entrar aqui fica visível na internet. Não coloque nomes de clientes, links de planilha nem segredos.

## Quem mantém
Levantado de `git shortlog` dos últimos 90 dias.
- Responsável: Cesar Moura (cesar@hypr.mobi; também commita como `Cesar` e `cesarmour`) (a confirmar)
- Time: a definir
- Substituto: a definir

## Como rodar
Instalar no app do Claude: Plugins → Adicionar marketplace → `HYPR-Projects/hypr-plugins` → instalar **HYPR Audiences**. No Claude Code:

```text
/plugin marketplace add HYPR-Projects/hypr-plugins
/plugin install hypr-audiences@hypr
```

Testar uma mudança local antes do push:

```text
/plugin marketplace add /caminho/para/o/clone/hypr-plugins
/plugin install hypr-audiences@hypr
```

- Uso: `/hypr` (categorias), `/hypr <tema>` (busca), `/hypr plano <marca e campanha>` (plano + deck).
- Fallback do deck sem o conector: [hypr_deck.py](plugins/hypr-audiences/skills/hypr/scripts/hypr_deck.py) (`python3 hypr_deck.py plano.json saida.pptx`, precisa de `python-pptx`).

## Onde está no ar
| Ambiente | Onde | URL | Como publica |
|---|---|---|---|
| produção | Marketplace `hypr` (este repo, branch `main`) | `HYPR-Projects/hypr-plugins` | push na `main` + subir o `version` em [plugin.json](plugins/hypr-audiences/.claude-plugin/plugin.json) e no [marketplace.json](.claude-plugin/marketplace.json) |
| conector | Servidor MCP `hypr-audiences` (repo `hypr-audiences-mcp`, Vercel) | `https://mcp.hyprgrid.ai/mcp` | pelo repo do servidor, não por este |

- Versão atual do plugin: `1.0.0`. O servidor MCP tem versão própria (`1.10.0` em 03/11/2026).
- **Nome repetido:** o marketplace do repo `claude-analise-campanhas` também se chama `hypr`. Quem tem os dois pode ter conflito de nome (a confirmar qual prevalece).

## Quais bases usa
Este repo não lê base nenhuma: tudo passa pelo conector MCP.

| Base | Tabela | Lê / grava |
|---|---|---|
| Google Sheets | planilha "Knowledge-audiences-HYPR" (catálogo; mudanças aparecem em até 1 min) | o conector lê |
| BigQuery | HYPR Library (tags dos slides dos decks), compilada no servidor MCP | o conector lê |

Detalhe das fontes: no repo `hypr-audiences-mcp`.

## Segredos
Nenhum. O conector é chamado sem login (`.mcp.json` só tem a URL). Os segredos do servidor moram no projeto Vercel do `hypr-audiences-mcp`.

## Ajustes comuns
- **Trocar o endereço do conector:** [.mcp.json](plugins/hypr-audiences/.mcp.json) e a URL em [deck.md](plugins/hypr-audiences/skills/hypr/references/deck.md).
- **Comando `/hypr` (busca, categorias, plano):** [skills/hypr/SKILL.md](plugins/hypr-audiences/skills/hypr/SKILL.md).
- **Fluxo do plano:** [agents/planejador-hypr.md](plugins/hypr-audiences/agents/planejador-hypr.md). O método vigente vem do conector (`get_method`); os arquivos `*_fallback.md` em [references/](plugins/hypr-audiences/skills/hypr/references/) só valem sem ele.
- **Regras de marca e taxonomia:** [planejamento-audiencias/references/](plugins/hypr-audiences/skills/planejamento-audiencias/references/).
- **Publicar:** suba o `version` nos dois manifestos; sem isso, quem já instalou não recebe.

## Integrações
- **HYPR Audiences MCP** (`mcp.hyprgrid.ai`): busca, ranking, plano, avaliação e deck (`search_audiences`, `list_categories`, `get_method`, `build_deck` e outras).
- **App do ChatGPT:** o mesmo conector está sendo preparado como app do ChatGPT (a confirmar se já está publicado).
- **Claude:** app desktop (Plugins) e Claude Code (`/plugin`).
