# Regras de redação técnica STE em português brasileiro

Cada regra tem um identificador (por exemplo, `R4.2`). Use o identificador em relatórios de revisão. As seções seguem a ordem das seções do ASD-STE100. As regras marcadas com **(adaptação)** não existem no ASD-STE100 e tratam de características do português.

## Sumário

1. Palavras
2. Sintagmas nominais
3. Verbos
4. Frases
5. Procedimentos
6. Descrições
7. Avisos de segurança
8. Pontuação e contagem de palavras
9. Práticas de redação

---

## 1. Palavras

**R1.1 Use palavras aprovadas.** Use as palavras do [DICIONARIO.md](DICIONARIO.md), do glossário do projeto ou um nome técnico (R1.4). Se uma palavra não está aprovada, use a alternativa do dicionário.

**R1.2 Use cada palavra com um só significado.** Uma palavra aprovada tem um significado aprovado. Não use a palavra com outro significado.

| Não use | Use |
|---|---|
| Suba a aplicação no servidor. (implantar) | Implante a aplicação no servidor. |
| Suba o serviço. (iniciar) | Inicie o serviço. |

**R1.3 Não crie verbos a partir de nomes técnicos ou estrangeirismos.** Use um verbo aprovado e o nome técnico.

| Não use | Use |
|---|---|
| Commite as alterações. | Faça o commit das alterações. |
| Deploye a versão 2.1. | Implante a versão 2.1. |

**R1.4 Use nomes técnicos quando necessário.** São nomes técnicos:

- nomes de produtos, sistemas, componentes e serviços
- comandos, arquivos, campos, parâmetros e variáveis
- rótulos da interface e mensagens do sistema
- unidades de medida, códigos de erro e conceitos do glossário do projeto

Escreva identificadores de código com crase (`config.yaml`). Escreva rótulos da interface em negrito e exatamente como aparecem na tela (**Salvar**).

**R1.5 Use a palavra mais simples.** Se duas palavras têm o mesmo significado, use a mais curta e mais comum: "usar", e não "utilizar".

**R1.6 Use o mesmo termo para o mesmo conceito.** Não use sinônimos para variar o estilo. Se o documento diz "servidor", não diga "máquina" ou "host" para o mesmo item.

**R1.7 Use o termo consagrado em português.** Mantenha o termo em inglês só se ele é o nome técnico consagrado na área (por exemplo, "commit", "pipeline", "token") ou um nome próprio. Não use adaptações informais como "deletar", "setar" ou "logar". **(adaptação)**

**R1.8 Defina as siglas.** Na primeira ocorrência, escreva o nome completo e a sigla entre parênteses: "Lei Geral de Proteção de Dados (LGPD)". Depois, use só a sigla. Escreva o plural sem apóstrofo: "APIs".

**R1.9 Escreva números e unidades de forma padronizada.** **(adaptação)**

- Use algarismos para quantidades com unidade e para valores técnicos: "3 servidores", "10 MB".
- Coloque um espaço entre o número e a unidade: "30 s", "512 MB". Exceção: "%" fica junto do número ("80%").
- Use vírgula decimal no texto: "2,5 GB". Mantenha o formato literal em código e em valores de configuração.
- Escreva datas no formato DD/MM/AAAA no texto e ISO 8601 (AAAA-MM-DD) em dados técnicos.
- Escreva horas no formato de 24 horas: "14h30".
- Escreva valores monetários com o símbolo e um espaço: "R$ 1.250,00".

---

## 2. Sintagmas nominais

**R2.1 Não encadeie mais de três substantivos.** Em português, o encadeamento acontece com "de", "do", "da", "dos" e "das". Se a sequência tem mais de três substantivos, divida a informação. **(adaptação)**

| Não use | Use |
|---|---|
| Abra o arquivo de configuração do serviço de autenticação do ambiente de homologação. | No ambiente de homologação, abra o arquivo de configuração do serviço de autenticação. |

**R2.2 Use artigos e preposições.** Não escreva em estilo telegráfico. Títulos e rótulos de tabela são exceção.

| Não use | Use |
|---|---|
| Abrir arquivo e alterar porta. | Abra o arquivo e altere a porta. |

**R2.3 Não use nominalização com verbo de apoio.** Use o verbo que expressa a ação. Verbos de apoio comuns: "realizar", "efetuar", "fazer", "proceder", "promover". **(adaptação)**

| Não use | Use |
|---|---|
| Realize a instalação do pacote. | Instale o pacote. |
| Efetue a validação dos dados. | Valide os dados. |

Exceção: use "fazer" com um nome técnico que não tem verbo aprovado: "Faça o commit", "Faça o backup".

**R2.4 Não use pronomes com referência ambígua.** Se o leitor pode não saber a que um pronome se refere, repita o substantivo. Não use "o mesmo" e "a mesma" como pronome. **(adaptação)**

| Não use | Use |
|---|---|
| Copie o token e cole o mesmo no campo. | Copie o token e cole o token no campo **Chave**. |

---

## 3. Verbos

**R3.1 Use a voz ativa.** Em procedimentos, use só a voz ativa. Em descrições, use a voz ativa sempre que possível. Use a voz passiva só quando o agente da ação não tem importância ou quando ninguém sabe quem executa a ação. Esta regra inclui a voz passiva com "se" ("configura-se", "recomenda-se").

| Não use | Use |
|---|---|
| O relatório é gerado pelo sistema às 2h. | O sistema gera o relatório às 2h. |
| Recomenda-se reiniciar o serviço. | Reinicie o serviço. |

**R3.2 Use os tempos verbais aprovados.** **(adaptação)**

| Uso | Tempo | Exemplo |
|---|---|---|
| Instrução | Imperativo afirmativo ou negativo | "Abra o arquivo." "Não feche a janela." |
| Fato atual ou regra geral (padrão) | Presente do indicativo | "O serviço grava o log." |
| Fato passado | Pretérito perfeito | "O incidente começou às 14h." |
| Fato futuro | Futuro do presente | "A versão 3 removerá a API antiga." |
| Condição | Futuro do subjuntivo, depois de "se" ou "quando" | "Se o serviço falhar, ..." |
| Finalidade | Presente do subjuntivo, depois de "para que" | "Para que o cache expire, ..." |

Não use futuro do pretérito ("seria", "deveria"), exceto para uma hipótese explícita. Não use mesóclise ("configurar-se-á") nem tempos compostos ("tinha configurado", "terá sido").

**R3.3 Não use gerúndio para ligar ações.** O gerúndio corresponde à forma "-ing", que o ASD-STE100 proíbe. Não use gerundismo ("vamos estar enviando"). **(adaptação)**

| Não use | Use |
|---|---|
| Clique em **Salvar**, confirmando a operação. | Clique em **Salvar**. Depois, clique em **Confirmar**. |
| Vamos estar enviando o arquivo amanhã. | Enviaremos o arquivo amanhã. |

**R3.4 Use os verbos modais com um só significado.** **(adaptação)**

- "deve" = obrigação. Não use "deverá", "precisa", "é necessário que" nem "faz-se necessário".
- "pode" = permissão ou possibilidade. Não use "poderá" para permissão.
- "não deve" = proibição em descrições. Em procedimentos, use o imperativo negativo: "Não altere o arquivo."

**R3.5 Use o particípio só como adjetivo ou na voz passiva permitida.** "O arquivo configurado" está correto.

---

## 4. Frases

**R4.1 Escreva um só tópico por frase.**

**R4.2 Respeite o limite de palavras.** Em procedimentos, escreva no máximo 20 palavras por frase. Em descrições, escreva no máximo 25 palavras. Varie o comprimento das frases e use frases curtas sempre que possível. Para as regras de contagem, consulte R8.9.

**R4.3 Não omita palavras para encurtar a frase.** Não omita verbos, artigos, preposições nem conjunções. Divida a frase.

**R4.4 Use listas verticais.** Use uma lista quando a frase tem mais de três itens, condições ou etapas.

**R4.5 Use conectivos simples.** Ligue as frases com conectivos como "depois", "então", "mas", "também", "por isso" e "porque". Não use conectivos rebuscados (consulte o [DICIONARIO.md](DICIONARIO.md)).

**R4.6 Use a ordem direta.** Escreva sujeito, verbo e complemento. Não coloque orações longas entre vírgulas no meio da frase. **(adaptação)**

**R4.7 Use a forma afirmativa.** Não use dupla negação. Prefira a afirmativa quando ela tem o mesmo significado.

| Não use | Use |
|---|---|
| Não deixe o serviço inativo. | Mantenha o serviço ativo. |

---

## 5. Procedimentos

**R5.1 Escreva cada instrução no imperativo.** Use a terceira pessoa ("Abra", "Execute", "Clique"). Escreva o título do procedimento no infinitivo: "Instalar o agente". **(adaptação)**

**R5.2 Escreva uma só instrução por frase.** Escreva uma só ação por passo. Exceção: duas ações que o leitor faz ao mesmo tempo.

| Não use | Use |
|---|---|
| 1. Abra o terminal, acesse a pasta e execute o script. | 1. Abra o terminal. 2. Acesse a pasta `deploy`. 3. Execute o script. |
| (exceção correta) | 1. Mantenha a tecla **Ctrl** pressionada e clique nos arquivos. |

**R5.3 Escreva a condição antes da ação.** "Se a tela de erro aparecer, clique em **Voltar**."

**R5.4 Numere os passos sequenciais.** Use marcadores só para itens sem ordem.

**R5.5 Coloque os pré-requisitos antes do primeiro passo.** Escreva-os em uma lista com o título "Pré-requisitos".

**R5.6 Escreva o resultado esperado quando o leitor deve confirmar.** Use uma frase separada, depois do passo: "Resultado: o painel mostra o status **Ativo**."

**R5.7 Divida procedimentos longos.** Se o procedimento tem mais de 10 passos, divida-o em subprocedimentos com títulos. **(adaptação)**

**R5.8 Não use fórmulas de cortesia.** Não use "por favor", "favor" nem "gentileza". **(adaptação)**

---

## 6. Descrições

**R6.1 Escreva a informação principal primeiro.** A primeira frase do parágrafo diz o tópico.

**R6.2 Escreva um só tópico por parágrafo.** Escreva no máximo seis frases por parágrafo.

**R6.3 Apresente a informação nova de forma gradual.** Vá do geral ao específico e do conhecido ao novo.

**R6.4 Use títulos que dizem o assunto.** "Formato do arquivo de log" diz mais que "Informações gerais".

---

## 7. Avisos de segurança

**R7.1 Use a palavra de aviso correta.** **(adaptação)** O ASD-STE100 usa WARNING para risco a pessoas e CAUTION para risco de dano ao equipamento. Para documentos de software e de processos, use:

| Palavra | Uso |
|---|---|
| `ATENÇÃO` | Risco a pessoas, risco à segurança da informação, exposição de dados pessoais ou perda de dados sem recuperação. |
| `CUIDADO` | Risco de dano ao sistema ou ao equipamento, indisponibilidade de serviço ou perda de dados com recuperação. |
| `NOTA` | Informação útil sem risco. Uma nota não tem instrução obrigatória. |

**R7.2 Comece o aviso com uma instrução.** Escreva primeiro uma instrução curta e específica. Depois, escreva o risco ou a consequência.

```markdown
> **ATENÇÃO:** Faça o backup do banco de dados antes da migração. A migração exclui a tabela `pedidos` e não tem como desfazer a operação.
```

**R7.3 Coloque o aviso antes do passo.** O leitor deve ler o aviso antes de executar o passo.

**R7.4 Escreva um só risco por aviso.** Se há dois riscos, escreva dois avisos.

**R7.5 Não use aviso para informação sem risco.** Use `NOTA`.

---

## 8. Pontuação e contagem de palavras

**R8.1 Não use ponto e vírgula.** Divida a frase ou use uma lista.

**R8.2 Use dois-pontos para introduzir uma lista, um exemplo ou um resultado.**

**R8.3 Use parênteses só para siglas, unidades e referências.** Não coloque informação essencial entre parênteses.

**R8.4 Não use travessão para inserir informação.** Use uma frase separada.

**R8.5 Não use vírgula entre o sujeito e o verbo** nem entre o verbo e o complemento. **(adaptação)**

**R8.6 Escreva os itens de lista de forma paralela.** Todos os itens têm a mesma estrutura. Se cada item é uma frase completa, comece com maiúscula e termine com ponto. Se cada item completa a frase de introdução, comece com minúscula e não use pontuação no fim do item.

**R8.7 Não use reticências, ponto de exclamação nem aspas para ênfase.**

**R8.8 Não use "e/ou".** Escreva "A, B ou os dois".

**R8.9 Conte as palavras assim:**

- Cada sequência de caracteres entre espaços é uma palavra.
- Uma palavra com hífen é uma palavra ("pré-requisito", "configurá-lo").
- Um número, uma data, uma sigla e um identificador em código são uma palavra cada.
- Contrações como "do", "na" e "pelo" são uma palavra.
- Títulos, tabelas, código e rótulos de figura não entram na contagem.

---

## 9. Práticas de redação

**R9.1 Seja consistente.** Use o mesmo termo, o mesmo formato e a mesma estrutura em todo o documento.

**R9.2 Use um tom neutro e direto.** Fale com o leitor por meio do imperativo. Não use "a gente", gírias, ironia, humor nem emojis.

**R9.3 Não use linguagem burocrática.** Não use "vimos por meio desta", "segue em anexo" nem "informamos que". **(adaptação)**

**R9.4 Não use termos vagos.** Escreva o valor exato.

| Não use | Use |
|---|---|
| O processo demora alguns minutos. | O processo demora até 5 minutos. |
| Reinicie o serviço rapidamente. | Reinicie o serviço em até 30 s. |

**R9.5 Não use referências que dependem do layout.** Não use "abaixo" nem "acima". Use "a seguir", "anterior" ou o nome do item ("a tabela 2", "a seção Instalação").

**R9.6 Use termos inclusivos.** Use "lista de bloqueio" e "lista de permissão", e não "blacklist" e "whitelist". Use "primário" e "réplica", e não "master" e "slave".
