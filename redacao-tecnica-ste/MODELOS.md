# Modelos de documento

Use estes modelos como estrutura inicial. Remova as seções que não se aplicam. Não remova as seções obrigatórias, marcadas com (obrigatória).

## Procedimento

```markdown
# <Verbo no infinitivo + objeto, por exemplo: Instalar o agente de monitoramento>

<Uma ou duas frases que dizem o objetivo do procedimento e quando o leitor deve usá-lo.>

## Pré-requisitos (obrigatória)

- <Acesso, permissão, ferramenta ou versão necessária>
- <Outro pré-requisito>

## Passos (obrigatória)

> **CUIDADO:** <Instrução curta.> <Risco ou consequência.>

1. <Ação no imperativo.>
2. <Ação no imperativo.>

   Resultado: <o que o leitor vê depois do passo>.

3. Se <condição>, <ação no imperativo>.

## Verificação

1. <Ação que confirma o resultado do procedimento.>

   Resultado: <estado esperado>.

## Como desfazer

1. <Ação que reverte o procedimento.>
```

## Descrição técnica

```markdown
# <Nome do componente, do sistema ou do conceito>

<Primeira frase: o que o item é. Segunda frase: para que ele serve.>

## Funcionamento

<Um parágrafo por tópico, com no máximo seis frases. Vá do geral ao específico.>

## Componentes

| Componente | Função |
|---|---|
| `<nome>` | <Uma frase curta.> |

## Limitações

- <Limitação com valor exato, por exemplo: o serviço aceita até 100 conexões ao mesmo tempo.>

## Referências

- <Documento relacionado, com link>
```

## Solução de problemas

```markdown
# Solução de problemas: <componente>

## <Sintoma, como o leitor o vê, por exemplo: O painel mostra o erro 503>

**Causa:** <Uma frase que diz a causa.>

**Solução:**

1. <Ação no imperativo.>
2. <Ação no imperativo.>

Se o problema continuar, <próxima ação ou contato>.
```

## Notas de versão

```markdown
# Versão <X.Y.Z>, <DD/MM/AAAA>

## Novas funções

- <Função nova, no presente: "O relatório mostra o total por mês.">

## Alterações

- <Mudança de comportamento. Diga o comportamento anterior e o novo.>

## Correções

- <Erro corrigido. Diga o erro e a correção: "Na versão anterior, a exportação para CSV falhou com nomes acentuados. A exportação agora aceita acentos.">

## Ações necessárias

> **ATENÇÃO:** <Instrução curta.> <Risco se o leitor não fizer a ação.>

1. <Ação no imperativo.>
```
