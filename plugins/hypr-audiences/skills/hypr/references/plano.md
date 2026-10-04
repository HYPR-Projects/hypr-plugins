# Plano de audiências (/hypr plano)

O método oficial (fluxo, esquema do deck e regras de marca) é mantido no conector e lido na hora:

1. Chame a ferramenta `get_method` do conector `hypr-audiences` (sem argumentos) e siga o texto devolvido do início ao fim. Em clientes com suporte a prompts, o prompt `metodo_plano` entrega o mesmo conteúdo.
2. Não use versões decoradas ou lembradas do método: a do servidor é a vigente (campo `version`).

Se `get_method` não existir ou falhar (conector antigo ou fora do ar), siga a versão congelada em `plano_fallback.md` e `deck.md` desta pasta e avise em uma linha que usou o fallback.
