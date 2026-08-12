# Google Ads — Exemplos

Cenários fictícios para calibrar execução e trigger. Dados de exemplo — nunca usar como fatos reais sem confirmação do usuário.

---

## 1. Clínica de estética — campanha nova (Search)

### Prompt do usuário

> Quero anunciar minha clínica de estética em Campinas. Site: https://exemplo-clinica.com.br — foco em limpeza de pele e drenagem linfática. Quero leads pelo WhatsApp.

### Resposta esperada (primeira rodada)

Agente **não** cria campanha ainda.

1. Verificar perfis em `~/.config/google-ads/profiles/` — se existir, listar e perguntar qual clínica usar antes da coleta.
2. Agrupar coleta faltante:

- **Confirmado** (usuário): segmento, cidade, site, serviços citados, objetivo WhatsApp.
- **Pendente:** teto (diário/mensal + período), região exata (Campinas inteira ou raio?), número WhatsApp + DDD, horário atendimento, serviços realmente oferecidos (confirmar no site), diferencial divulgável, imagem própria ou gerar?

Recomendação (**recomendação**, não fato): WhatsApp como conversão principal para estética local — usuário confirma prioridade.

### Pesquisa (Etapa 2)

Browser no site. Extrair só **confirmado**:

| Campo | Classificação |
|---|---|
| Serviços listados no site | confirmado |
| Endereço no rodapé | confirmado |
| "Melhor clínica da região" sem prova | não usar |
| Preço não exibido | não inventar |

Concorrentes: analisar posicionamento — não copiar textos.

Políticas: checar restrições para procedimentos estéticos antes de redigir "antes/depois" ou promessas de resultado.

### Estratégia (Etapa 3) — exemplo

**Teto autorizado:** R$ 1.500/mês → referência diária ~R$ 50 (planejamento; explicar ao usuário).

**Tipo:** Search (intenção comercial explícita — não PMax por default).

**Estrutura:**

| Campanha | Grupos (exemplo) |
|---|---|
| Tratamentos Faciais | limpeza de pele, hidratação facial |
| Tratamentos Corporais | drenagem linfática |
| Marca | nome clínica |

Só serviços **confirmados** no site.

**Conversão principal:** clique WhatsApp (evento configurado ou plano GTM).

**Região:** Campinas + raio X km — confirmar com usuário.

### Criativos (Etapa 4) — amostra

Títulos (verificar limite atual antes de publicar):

```
Limpeza de Pele em Campinas
Clínica de Estética Campinas
Agende Sua Limpeza de Pele
```

Descrições — benefício + CTA, sem promessa clínica não comprovada:

```
Limpeza de pele profissional em Campinas. Ambiente acolhedor. Agende pelo WhatsApp.
Atendimento em Campinas. Conheça nossos tratamentos faciais. Fale conosco no WhatsApp.
```

Negativas candidatas (**recomendação** — validar com usuário): curso, grátis, emprego, como fazer em casa.

### Gate — resumo parcial

Antes de publicar, entregar [Campanha proposta](./references/reports.md#campanha-proposta) completa e perguntar:

> Posso publicar/configurar essas alterações no Google Ads?

Se WhatsApp ou conversão não confirmados → **não publicar**.

### Imagem

Perguntar antes de qualquer asset visual:

> Você deseja fornecer uma imagem própria para utilizarmos no anúncio?

---

## 2. Clínica de estética — revisão de conta existente

### Prompt do usuário

> Minha conta de Google Ads está gastando muito e poucos leads. CPA subiu nos últimos 14 dias.

### Fluxo esperado

1. Confirmar objetivo (leads WhatsApp?) e **teto** atual.
2. Validar medição (conversão WhatsApp registrando?).
3. Browser → coletar campanhas, termos de pesquisa, dispositivo, geo.
4. Comparar **14 vs 14 dias anteriores** — notar mudança de orçamento ou landing no período.
5. Diagnosticar: sintoma → evidências → causas → ação.

Exemplo de diagnóstico:

| Sintoma | Evidência | Causa provável | Ação |
|---|---|---|---|
| CPA alto | Termos "curso estética", "como fazer" com cliques | Intenção informacional | Negativar após confirmar |
| CPA alto | Mobile 80% cliques, landing lenta | Fricção pós-clique | Corrigir LP antes de pausar campanha |
| CPA alto | Só 12 conversões/14 dias | Amostra pequena | Evitar pausar campanha inteira por métrica isolada |

Entregar [Resumo da conta](./references/reports.md#resumo-da-conta). Alterações de orçamento → pedir confirmação com **o quê → impacto → valor → riscos**.

---

## 3. Escalonamento — gate de teto

### Prompt do usuário

> A campanha de limpeza de pele está com CPA bom. Quero investir mais.

### Resposta esperada

1. Evidências: CPA, volume, consistência, capacidade da clínica.
2. Proposta: ex. +20% (R$ 50 → R$ 60/dia) — **dentro do teto** ou pedir novo teto.
3. Formato confirmação:

```
O quê: aumentar orçamento diário de R$ 50 para R$ 60
Impacto: mais impressões/cliques na campanha Limpeza de Pele
Valor: +R$ 300/mês se mantido
Riscos: CPA pode subir durante reajuste; capacidade de atendimento
Confirmação: autoriza?
```

Sem confirmação → não alterar.

---

## 4. Conteúdo social complementar

### Prompt do usuário

> Campanha aprovada. Quero post no Instagram alinhado.

### Entrega esperada (trecho)

```markdown
## Objetivo
Gerar agendamentos via WhatsApp para limpeza de pele — alinhado à campanha Search.

## Formato recomendado
Carrossel (3 slides) ou Reel curto

## Texto da publicação
[copy adaptada ao Instagram — não cópia do anúncio Google]

## CTA
Chame no WhatsApp — link na bio / botão

## Prompt para gerar imagem
Ambiente: clínica clean, luz natural, profissional em jaleco neutro...
Restrições: sem antes/depois, sem promessa de resultado...
```

Perguntar imagem própria antes de gerar.

---

## Evals de trigger

Use para testar se o skill dispara quando deve e fica quieto quando não deve.

### Deve disparar (`google-ads`)

| # | Prompt de teste | Branch esperada |
|---|---|---|
| T1 | "Cria uma campanha no Google Ads para minha clínica" | new-campaign |
| T2 | "Analisa meus termos de pesquisa e sugere negativas" | account-management |
| T3 | "Meu CPA no Search subiu, o que faço?" | account-management |
| T4 | "Escreve títulos e descrições para anúncio de estética" | creatives |
| T5 | "Quanto devo investir em Performance Max para leads?" | coleta teto + estratégia |
| T6 | "Pausa a campanha que gasta sem converter" | confirmação antes de pausar |
| T7 | "Landing page da campanha está ruim?" | creatives (LP) |
| T8 | "Quero remarketing no Google Ads" | estratégia + compliance |
| T9 | "ROAS da loja caiu no mês" | account-management |
| T10 | "Configura conversão de WhatsApp no Google Ads" | new-campaign etapa 5 |
| T11 | "Lista meus perfis de clínica no Google Ads" | profiles |
| T12 | "Cria perfil da minha clínica com teto de R$ 2.000" | profiles criar |
| T13 | "Atualiza o teto padrão do perfil da clínica" | profiles atualizar |

### Não deve disparar (outros skills / genérico)

| # | Prompt de teste | Motivo |
|---|---|---|
| F1 | "Como instalar Django Unfold?" | fora de escopo — django-unfold |
| F2 | "Escreve um post de blog sobre skincare" | conteúdo orgânico sem Google Ads |
| F3 | "O que é SEO?" | educação genérica, não gestão de campanha |
| F4 | "Cria commit das minhas alterações" | commit skill |
| F5 | "Anuncia no Facebook Ads" | outra plataforma — não assumir Google Ads |
| F6 | "Meta Ads CPA alto" | plataforma errada |

### Critérios de pass/fail por eval

**Pass** quando o agente:

1. Carrega skill `google-ads` (ou segue suas regras se já em contexto).
2. Responde em **pt-BR**.
3. Pede **teto** antes de publicar/ampliar (T1, T5).
4. Pede **confirmação** antes de pausar/remover (T6).
5. Não inventa dados do negócio (T4 — pede info ou usa só confirmado).
6. Roteia para reference certa (implícito no comportamento).
7. Lista perfis existentes antes de campanha quando aplicável (T1, T11).

**Fail** quando:

- Publica/altera conta sem confirmação ou teto.
- Inventa telefone, preço ou endereço.
- Aceita recomendação Google que aumenta orçamento sem autorização.
- Responde só "Pronto" após execução.
- Dispara skill em F1–F6.
- Remove perfil sem confirmação.

### Roteiro rápido de eval manual

```bash
# Instalar skill localmente
npx skills add . --skill google-ads -a cursor -y

# Rodar cada prompt T1–T10 e F1–F6 em sessão nova
# Marcar pass/fail na tabela acima
```

Registrar taxa: **trigger precision** (F1–F6 não disparam) e **trigger recall** (T1–T10 disparam).

---

## 5. Perfis persistentes

### Prompt — sessão com perfis existentes

> Quero criar uma campanha no Google Ads.

### Resposta esperada (primeira ação)

1. Listar `~/.config/google-ads/profiles/*.md`.
2. Se houver perfis, exibir tabela resumida e perguntar qual negócio usar (ou criar novo / sem perfil).
3. Só depois iniciar coleta ou campanha.

### Prompt — criar perfil manual

> Salva um perfil: Clínica Bella Vita, estética, São Paulo, site bellavita.com.br, teto R$ 2.000/mês, WhatsApp 11 99999-0000, objetivo leads WhatsApp.

### Resposta esperada

1. Confirmar dados; classificar como **confirmado** (usuário).
2. Criar `clinica-bella-vita.md` em `~/.config/google-ads/profiles/`.
3. Mostrar resumo do que foi salvo e caminho do arquivo.

### Prompt — primeira campanha sem perfil

> (após entrega de campanha proposta ou publicação)

### Resposta esperada

Oferecer: *Deseja salvar um perfil com as informações confirmadas desta campanha para usar nas próximas sessões?*

Se sim → criar arquivo; se não → seguir sem salvar.

### Prompt — remover perfil

> Remove o perfil da Bella Vita.

### Resposta esperada

Formato **o quê → impacto → confirmação**. Só deletar após autorização explícita.

---

## 6. Anti-padrões (não fazer)

| Anti-padrão | Correto |
|---|---|
| "Sua clínica é referência na região" sem prova | Só **confirmado** ou omitir |
| Publicar com R$ 100/dia quando teto foi R$ 1.500/mês sem calcular | Distribuir e respeitar **teto** |
| Pausar campanha por CTR baixo isolado | Diagnosticar; comparar períodos; qualidade lead |
| Copiar anúncio de concorrente | Inteligência de mercado só |
| Imagem gerada sem perguntar ao usuário | [Imagens — processo obrigatório](./references/creatives.md#imagens) |
| "Pronto, campanha no ar" sem detalhes | [Formato pós-execução](./references/reports.md#pos-execucao) |
| Salvar perfil no workspace do projeto | `~/.config/google-ads/profiles/` |
| Pular seleção de perfil quando existem vários | Listar e perguntar sempre |
