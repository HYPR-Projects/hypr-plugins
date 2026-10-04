# Deck resumo HYPR

O esquema do `plano.json` e as regras do deck estão na seção B do método servido pelo conector (`get_method` com `section: "deck"`, ou o método completo). O deck é gerado por `build_deck` (ou `POST https://hypr-audiences-mcp.netlify.app/deck`), sempre com o layout vigente do servidor.

Fallback sem conector: `deck_fallback.md` + `scripts/hypr_deck.py plano.json saida.pptx` (requer python-pptx).
