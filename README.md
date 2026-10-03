# HYPR Audiences para Claude

Consulte o catálogo de audiências da **HYPR** direto no Claude: busque audiências, veja volumes e monte planos para qualquer marca em segundos.

---

## Como instalar (2 minutos, uma vez só)

**1. Abra o Claude** no computador (app desktop).

**2. Vá em Plugins** e escolha **Adicionar marketplace**.

**3. Cole este endereço** e confirme:

```
HYPR-Projects/hypr-plugins
```

**4. Instale o plugin.** Na lista, clique em **HYPR Audiences** e depois em **Instalar**. Se o Claude pedir para ativar o conector "hypr-audiences", aceite. Não precisa de login.

Pronto. Novas versões chegam automaticamente.

> Usa o Claude Code no terminal? Rode:
> ```
> /plugin marketplace add HYPR-Projects/hypr-plugins
> /plugin install hypr-audiences@hypr
> ```

---

## Como usar

Abra um **chat novo** e digite um destes comandos:

| Você quer | Digite | Exemplo |
|---|---|---|
| Ver todas as categorias | `/hypr` | `/hypr` |
| Buscar audiências | `/hypr <tema>` | `/hypr postos` |
| Montar um plano para uma marca | `/hypr plano <marca e campanha>` | `/hypr plano Natura dia das mães` |

Também dá para perguntar normalmente, sem comando:

- *"Quais audiências da HYPR servem para uma marca de ração premium?"*
- *"Qual o volume de visitantes de agências bancárias?"*
- *"Monta um plano de audiências para um banco digital focado em aquisição."*

---

## O que você recebe

**Na busca:** uma tabela com o nome da audiência, o ID para ativação, a categoria e o volume.

**No plano:**

- **Audiências em camadas:** Core, Conquista (clientes da concorrência), Afinidade e Expansão.
- **Brand Affinity** de 0 a 100% em cada audiência, indicando o quanto ela combina com o seu briefing.
- **Plataforma HYPR recomendada:** como geoIQ (onde), adsIQ (com o quê), revIQ (quanto) e askIQ (por quê) trabalham juntos no seu caso.
- **Como medir:** comparação entre quem foi exposto e um grupo de controle, para mostrar o incremento de vendas na loja.

---

## Dicas para um plano melhor

Quanto mais contexto, melhor o resultado. Inclua no pedido:

- **Marca e produto:** *"ração premium para gatos"*
- **Objetivo:** awareness, vendas, lançamento ou conquistar clientes da concorrência
- **Concorrentes:** *"vs. Royal Canin"*
- **Público e praça:** *"classe AB, São Paulo"*

Exemplo completo:

```
/hypr plano Premier Pet, ração premium para gatos, lançamento em SP, público classe AB, concorrente Royal Canin
```

---

## Perguntas frequentes

**O comando `/hypr` não aparece.**
Feche e abra o Claude, ou comece um chat novo.

**Os dados estão atualizados?**
Sim. O catálogo é atualizado pela HYPR e as mudanças aparecem em até 1 minuto, sem reinstalar nada.

**O que é Brand Affinity?**
Uma estimativa de quanto cada audiência combina com o seu briefing, calculada a partir do perfil de cada audiência no catálogo. Use para priorizar; o time HYPR valida o plano final.

**Preciso pagar ou criar conta?**
Não para consultar. Para ativar uma campanha, fale com a HYPR.

---

**HYPR** · Do bolso à rua · [hyprgrid.ai](https://hyprgrid.ai)
