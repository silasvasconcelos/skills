# Documentação Negocial — {{Nome da Funcionalidade}}

| Campo             | Valor                                                        |
| ----------------- | ------------------------------------------------------------ |
| **Cliente**       | {{Nome do cliente}}                                          |
| **Projeto**       | {{Nome do projeto}}                                          |
| **Funcionalidade**| {{Nome da funcionalidade}}                                   |
| **Referência**    | {{Código da user story / ticket — ex.: UP-000}}             |
| **Data-base**     | {{DD/MM/AAAA}} ({{contexto — ex.: reunião de levantamento}}) |
| **Versão**        | {{1.0}}                                                      |

---

## 1. Visão Geral

> Descreva em 2-3 parágrafos o contexto do sistema, o problema atual e o objetivo da funcionalidade. Inclua dados quantitativos quando houver (ex.: tempo gasto, % de casos, volume).

{{Contexto do produto/sistema.}}

{{Problema atual e seu impacto operacional.}}

{{Objetivo da funcionalidade e benefício esperado.}}

---

## 2. Objetivos de Negócio

| #  | Objetivo                                                  |
| -- | --------------------------------------------------------- |
| O1 | {{Objetivo mensurável 1}}                                 |
| O2 | {{Objetivo mensurável 2}}                                 |
| O3 | {{Objetivo mensurável 3}}                                 |
| O4 | {{...}}                                                   |

---

## 3. Atores

| Ator              | Descrição                                                  |
| ----------------- | ---------------------------------------------------------- |
| **{{Ator 1}}**    | {{Quem é e qual seu papel na funcionalidade}}              |
| **{{Ator 2}}**    | {{...}}                                                    |
| **{{Sistema X}}** | {{Sistema/serviço que participa do fluxo}}                 |

---

## 4. Contexto Atual (AS-IS)

> Descreva o fluxo atual (manual ou existente). Use diagrama ASCII, lista numerada ou Mermaid.

```
{{Diagrama / passo a passo do processo atual}}
```

### 4.1 Problemas Identificados

| #  | Problema                                                  |
| -- | --------------------------------------------------------- |
| P1 | {{Problema 1}}                                            |
| P2 | {{Problema 2}}                                            |
| P3 | {{...}}                                                   |

---

## 5. Solução Proposta (TO-BE)

> Descreva o fluxo proposto e onde a funcionalidade será integrada. Use diagrama ASCII/Mermaid e/ou esboço de telas.

```
{{Diagrama do fluxo proposto / esboço de telas}}
```

---

## 6. Regras de Negócio

> Agrupe as regras por tema. Numere sequencialmente (RN-01, RN-02, ...).

### 6.1 {{Tema do grupo de regras}}

| ID    | Regra                                                     |
| ----- | --------------------------------------------------------- |
| RN-01 | {{Regra de negócio}}                                      |
| RN-02 | {{Regra de negócio}}                                      |

### 6.2 {{Outro tema}}

| ID    | Regra                                                     |
| ----- | --------------------------------------------------------- |
| RN-03 | {{Regra de negócio}}                                      |

---

## 7. Casos de Uso

### UC-01 — {{Nome do caso de uso}}

| Campo              | Descrição                                              |
| ------------------ | ------------------------------------------------------ |
| **Ator principal** | {{Ator}}                                               |
| **Pré-condição**   | {{Estado necessário antes do fluxo}}                   |
| **Pós-condição**   | {{Estado resultante após o fluxo}}                     |
| **Fluxo principal**| 1. {{Passo 1}} |
|                    | 2. {{Passo 2}} |
|                    | 3. {{Passo 3}} |
| **Fluxo alternativo Na** | {{Condição e desvio do fluxo}}                   |

---

### UC-02 — {{Nome do caso de uso}}

| Campo              | Descrição                                              |
| ------------------ | ------------------------------------------------------ |
| **Ator principal** | {{Ator}}                                               |
| **Pré-condição**   | {{...}}                                                |
| **Pós-condição**   | {{...}}                                                |
| **Fluxo principal**| 1. {{Passo 1}} |
|                    | 2. {{Passo 2}} |

---

## 8. Modelo de Dados (Conceitual)

> Represente as entidades principais e seus relacionamentos. ASCII ou Mermaid.

```
{{Diagrama de entidades / relacionamentos}}
```

---

## 9. Valores Iniciais dos Domínios Configuráveis

> Liste valores iniciais de domínios configuráveis (status, classificações, tipos, etc.). Remova esta seção se não aplicável.

### 9.1 {{Domínio 1}}

| Código        | Descrição                          | {{Atributo extra}} |
| ------------- | ---------------------------------- | ------------------ |
| {{COD_1}}     | {{Descrição}}                      | {{Sim/Não}}        |
| {{COD_2}}     | {{Descrição}}                      | {{Sim/Não}}        |

### 9.2 {{Domínio 2}}

| Código        | Descrição                          |
| ------------- | ---------------------------------- |
| {{COD_1}}     | {{Descrição}}                      |

---

## 10. Requisitos Não-Funcionais

| ID     | Requisito                                                |
| ------ | -------------------------------------------------------- |
| RNF-01 | {{Requisito de integração / plataforma}}                 |
| RNF-02 | {{Requisito de usabilidade / dispositivo}}               |
| RNF-03 | {{Requisito de desempenho / segurança / custo}}          |

---

## 11. Fora de Escopo (Melhorias Futuras)

> Itens mencionados, porém fora do escopo inicial.

| Item                  | Descrição                                            |
| --------------------- | ---------------------------------------------------- |
| {{Item 1}}            | {{Descrição}}                                        |
| {{Item 2}}            | {{Descrição}}                                        |

---

## 12. Glossário

| Termo              | Definição                                             |
| ------------------ | ----------------------------------------------------- |
| **{{Termo 1}}**    | {{Definição}}                                         |
| **{{Termo 2}}**    | {{Definição}}                                         |

---

## 13. Referências

- {{Reunião / fonte 1}}
- {{Documento / protótipo 2}}
- {{...}}

---

*Documento gerado a partir de {{fonte — ex.: transcrição da reunião de DD/MM/AAAA entre {{cliente}} e {{analista}}}}, referente à user story {{REF}}.*
