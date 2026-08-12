# Perfis de negócio

Perfis persistem dados **confirmados** do negócio entre sessões e reinícios. Um arquivo Markdown por perfil.

## Local de armazenamento (persistente)

Criar pasta se não existir. Nunca salvar só no projeto ou workspace — dados do usuário ficam no home.

| SO | Caminho |
|---|---|
| macOS / Linux | `~/.config/google-ads/profiles/` |
| Windows | `%USERPROFILE%\.config\google-ads\profiles\` |

**Arquivo:** `{slug}.md` — ex.: `clinica-estetica-campinas.md`

**Slug:** minúsculas, sem acentos, hífens, derivado do nome do negócio. Sem espaços ou caracteres especiais.

## Início de cada sessão (obrigatório)

Antes de coleta, campanha, otimização ou relatório:

1. Listar `*.md` na pasta de perfis (shell ou leitura de arquivos).
2. **Se existir perfil:**
   - Exibir tabela resumida: nome, segmento, cidade, teto padrão, objetivo, site.
   - Perguntar: *Para qual negócio/clínica vamos trabalhar?* (escolher existente, criar novo, ou trabalhar sem perfil).
   - Perfil escolhido → carregar arquivo completo; usar dados como base; perguntar só lacunas ou mudanças.
3. **Se não existir perfil:**
   - Informar que não há perfil salvo.
   - Seguir coleta normal.
   - Ao **finalizar** primeira campanha/anúncio bem estruturado (estratégia + criativos entregues, ou após publicação): oferecer salvar perfil com dados **confirmados** coletados.

Nunca assumir perfil ativo sem seleção explícita do usuário.

## Operações do usuário

| Pedido | Ação |
|---|---|
| Criar perfil | Coletar dados mínimos → criar `{slug}.md` com [profile-template.md](profile-template.md) |
| Atualizar perfil | Ler arquivo → mostrar diff mental → aplicar mudanças confirmadas → atualizar `updated` |
| Remover perfil | Mostrar resumo → **o quê → impacto → confirmação** → deletar arquivo |
| Listar perfis | Tabela resumida de todos os arquivos |
| Enriquecer perfil | Após campanha, revisão ou nova info confirmada → merge sem apagar confirmado |

Remoção irreversível — sempre pedir confirmação explícita.

## Campos do perfil

Salvar só **confirmado** (usuário, site oficial, materiais do negócio). Hipótese → seção Notas, nunca em campos principais.

| Grupo | Campos |
|---|---|
| Identificação | nome, segmento, slug |
| Localização | cidade, região/raio, endereço |
| Presença online | site, landing pages, Google Business Profile, Instagram, outras redes |
| Contato | WhatsApp (+ DDD, link), telefone (+ horário), formulário/agendamento (URL), email |
| Oferta | serviços confirmados, diferenciais, promoções/preços divulgáveis |
| Google Ads | teto padrão (valor + diário/mensal + período), objetivo principal, conversão principal, tipo campanha preferido, ID conta Google Ads (se conhecido) |
| Público | descrição, restrições geográficas |
| Criativos | preferência de imagem (própria/gerar), notas de copy/brand |
| Histórico | campanhas criadas (nome, tipo, data), última revisão, observações operacionais |

Campos vazios: omitir ou marcar pendente — não inventar.

## Criar arquivo

1. Definir slug único (se colisão → sufixo `-2`, `-3`…).
2. Copiar estrutura de [profile-template.md](profile-template.md).
3. Preencher front matter YAML + seções.
4. Escrever com ferramenta de arquivo no caminho persistente.

## Atualizar / enriquecer

1. Ler perfil ativo.
2. Novos dados **confirmados** → atualizar campo correspondente.
3. Dado antigo confirmado contradito pelo usuário → substituir; registrar em Notas se relevante.
4. Hipótese confirmada → promover a campo principal.
5. Atualizar `updated` no front matter.
6. Informar usuário o que foi salvo.

Após publicação de campanha, revisão de conta ou coleta longa: perguntar *Deseja atualizar o perfil com as informações confirmadas nesta sessão?*

## Uso na coleta

Perfil ativo preenche [coleta mínima](../SKILL.md#coleta-mínima-perguntar-só-o-que-faltar). Exibir resumo do que já está salvo; perguntar apenas:

- lacunas críticas (teto, contato, objetivo se ausente)
- confirmação se dado antigo pode ter mudado (preço, promoção, serviços)
- foco da sessão (nova campanha, serviço específico, otimização)

Teto da sessão: usar teto do perfil como default; usuário pode alterar para esta campanha — não ultrapassar sem autorização.

## Integração com fluxos

| Fluxo | Perfil |
|---|---|
| [new-campaign.md](new-campaign.md) | Selecionar no início; enriquecer após etapa 3 ou 11 |
| [account-management.md](account-management.md) | Selecionar no início; atualizar após diagnóstico |
| [creatives.md](creatives.md) | Reutilizar serviços, contato, diferenciais confirmados |
| [compliance.md](compliance.md) | Triagem confirmado/hipótese alinhada ao perfil |

## Exibição resumida (lista)

Ao listar perfis para o usuário:

```markdown
| Perfil | Segmento | Cidade | Teto padrão | Objetivo | Site |
|---|---|---|---|---|---|
| Clínica Estética Campinas | estética | Campinas | R$ 1.500/mês | WhatsApp | exemplo.com.br |
```

Incluir opção: *Criar novo perfil* | *Continuar sem perfil*.

## Guardrails de perfil

- Nunca salvar hipótese como confirmado.
- Nunca remover perfil sem confirmação.
- Nunca expor caminhos absolutos com dados sensíveis em relatórios públicos — ok em conversa com o usuário.
- Credenciais de login Google Ads: **não** salvar senhas; só IDs de conta se o usuário fornecer.
