---
name: redacao-tecnica-ste
description: Define e aplica um padrão de redação técnica controlada em português brasileiro, adaptado do ASD-STE100 (Simplified Technical English, usado na aviação). Cobre vocabulário controlado, voz ativa, limite de palavras por frase, procedimentos, descrições, avisos de segurança e pontuação, com um verificador automático. Use ao criar, revisar ou reescrever documentação, README, manual, guia, procedimento, runbook, tutorial, relatório técnico, especificação, notas de versão ou qualquer documento técnico em português.
---

# Redação técnica STE em português brasileiro

Esta skill define o padrão de redação para documentos técnicos em português brasileiro. O padrão usa o ASD-STE100 como referência e adapta as regras à gramática do português. O objetivo é um texto claro, curto e com uma só interpretação.

Se o idioma do documento é o inglês, aplique o ASD-STE100 original.

## Fluxo de trabalho

Copie esta lista e marque cada etapa:

```
- [ ] 1. Identificar o tipo de cada trecho (procedimento ou descrição)
- [ ] 2. Carregar o glossário do projeto
- [ ] 3. Escrever com as regras essenciais
- [ ] 4. Verificar o texto
- [ ] 5. Corrigir e verificar de novo
- [ ] 6. Entregar
```

**1. Tipo do trecho.** Um procedimento diz ao leitor o que fazer. Uma descrição informa como algo é ou funciona. Um documento pode ter os dois tipos. Aplique o limite de palavras de cada tipo ao trecho correspondente.

**2. Glossário do projeto.** Procure um glossário no projeto (por exemplo, `GLOSSARIO.md`, `GLOSSARY.md`, `CONTEXT.md` ou uma seção de termos). Os termos do projeto têm prioridade sobre o [DICIONARIO.md](DICIONARIO.md). Se não existir glossário, use só o dicionário.

**3. Escrita.** Aplique as regras essenciais a seguir. Consulte [REGRAS.md](REGRAS.md) quando tiver dúvida sobre uma regra. Use [MODELOS.md](MODELOS.md) para a estrutura do documento.

**4. Verificação.** Se o ambiente executa Python 3, execute o verificador:

```bash
python3 <pasta-da-skill>/scripts/verificar_ste.py caminho/do/documento.md
```

Se não for possível executar o script, revise o texto com a lista de verificação final.

**5. Correção.** Corrija todos os itens `ERRO`. Analise cada `AVISO` e corrija quando a regra se aplica. Execute o verificador de novo até não haver `ERRO`.

**6. Entrega.** Entregue o documento. Se o pedido foi uma revisão de texto existente, inclua também uma tabela de alterações. A tabela mostra o trecho original, a regra (por exemplo, `R3.1`) e o texto novo.

## Regras essenciais

As regras completas e os exemplos estão em [REGRAS.md](REGRAS.md).

**Palavras**

- Use as palavras aprovadas do [DICIONARIO.md](DICIONARIO.md) ou do glossário do projeto.
- Use cada palavra com um só significado. Use sempre o mesmo termo para o mesmo conceito.
- Prefira a palavra simples: "usar", e não "utilizar". "Ter", e não "possuir".
- Não use estrangeirismos informais como "deletar", "setar" ou "startar".
- Defina cada sigla na primeira vez que ela aparece.

**Frases**

- Escreva no máximo **20 palavras** por frase em procedimentos e **25 palavras** em descrições.
- Escreva um só tópico por frase. Use a ordem direta: sujeito, verbo e complemento.
- Use a voz ativa: "O sistema grava o log", e não "O log é gravado pelo sistema".
- Use o presente do indicativo como tempo padrão. Não use gerúndio para ligar ações.
- Use o verbo direto, sem nominalização: "Valide o campo", e não "Faça a validação do campo".
- Não encadeie mais de três substantivos com "de", "do" ou "da".
- Não omita artigos nem preposições para encurtar a frase.

**Procedimentos**

- Escreva cada passo no imperativo: "Abra", "Execute", "Clique".
- Escreva uma só ação por passo. Numere os passos.
- Escreva a condição antes da ação: "Se o erro aparecer, clique em **Voltar**."
- Coloque os pré-requisitos antes do primeiro passo.
- Coloque o aviso de segurança antes do passo a que ele se aplica.

**Descrições**

- Escreva a informação principal primeiro.
- Escreva um só tópico por parágrafo, com no máximo seis frases.

**Avisos de segurança**

- Use `ATENÇÃO` para risco a pessoas, à segurança da informação ou de perda de dados sem recuperação.
- Use `CUIDADO` para risco de dano ao sistema, de indisponibilidade ou de perda de dados com recuperação.
- Use `NOTA` para informação útil sem risco.
- Comece o aviso com uma instrução curta. Depois, diga o risco.

**Pontuação**

- Não use ponto e vírgula. Divida a frase ou use uma lista.
- Não use reticências, exclamação nem "e/ou".
- Use negrito só para rótulos da interface e palavras de aviso.

## O que não alterar

Não reescreva estes conteúdos, mesmo se eles não seguem o padrão:

- código, comandos, saídas de terminal e mensagens de log
- rótulos da interface (escreva-os exatamente como aparecem na tela)
- citações literais, textos legais e nomes próprios

## Lista de verificação final

- [ ] Nenhuma frase de procedimento tem mais de 20 palavras.
- [ ] Nenhuma frase de descrição tem mais de 25 palavras.
- [ ] Cada passo tem uma só ação, no imperativo.
- [ ] Os termos são os mesmos do início ao fim do documento.
- [ ] Não há termos não aprovados do dicionário.
- [ ] Não há voz passiva sem necessidade, gerúndio encadeado nem nominalização.
- [ ] Os avisos estão antes do passo e têm instrução e risco.
- [ ] Não há ponto e vírgula.
- [ ] Todas as siglas estão definidas.

## Arquivos de referência

- [REGRAS.md](REGRAS.md): todas as regras, com identificador e exemplos.
- [DICIONARIO.md](DICIONARIO.md): palavras aprovadas, verbos com significado único e termos não aprovados.
- [MODELOS.md](MODELOS.md): modelos de procedimento, descrição, solução de problemas e notas de versão.
- [EXEMPLOS.md](EXEMPLOS.md): textos antes e depois da aplicação do padrão.
- `scripts/verificar_ste.py`: verificador automático. Use `--help` para ver as opções.

## Compatibilidade com outros agentes

Esta skill usa o formato aberto de Agent Skills (pasta com `SKILL.md` e arquivos de apoio). O script usa só a biblioteca padrão do Python 3.8 ou superior. Se o agente não lê skills, copie o conteúdo deste arquivo para as instruções do agente (por exemplo, `AGENTS.md`). Depois, informe o caminho dos arquivos de referência.
