# Exemplos

Cada exemplo mostra o texto original, o texto no padrão e as regras aplicadas.

## Exemplo 1: procedimento

**Antes**

> Para realizar a instalação do agente, é necessário que o usuário efetue o login no servidor e, após isso, rode o script de instalação, verificando se o mesmo foi executado com sucesso.

**Depois**

> **Pré-requisitos**
>
> - Acesso SSH ao servidor
>
> **Passos**
>
> 1. Entre no servidor.
> 2. Execute o script `install-agent.sh`.
>
>    Resultado: o terminal mostra a mensagem `Agent installed`.

**Regras aplicadas:** R2.3 (realizar a instalação), R3.4 (é necessário que), R1.1 (efetue o login, rode), R3.3 (verificando), R2.4 (o mesmo), R5.2 (uma ação por passo), R5.6 (resultado esperado).

## Exemplo 2: descrição

**Antes**

> O serviço de autenticação, que foi desenvolvido visando atender às necessidades de segurança da organização, possui a capacidade de efetuar a validação dos tokens emitidos pelo provedor de identidade, sendo que os mesmos são armazenados em cache por um período de tempo de alguns minutos.

**Depois**

> O serviço de autenticação valida os tokens do provedor de identidade. O serviço guarda cada token em cache por 5 minutos.

**Regras aplicadas:** R6.1 (informação principal primeiro), R1.1 (visando, possui, sendo que), R2.3 (efetuar a validação), R2.4 (os mesmos), R3.1 (são armazenados), R9.4 (alguns minutos), R4.2 (limite de palavras).

## Exemplo 3: aviso de segurança

**Antes**

> NOTA: A execução deste comando poderá causar a perda dos dados, então recomenda-se que seja feito um backup antes!

**Depois**

> **ATENÇÃO:** Faça o backup do banco de dados antes de executar o comando. O comando exclui todos os registros da tabela `clientes` e não tem como desfazer a operação.

**Regras aplicadas:** R7.1 (palavra de aviso correta), R7.2 (instrução primeiro, depois o risco), R3.1 (recomenda-se, seja feito), R3.4 (poderá), R9.4 (perda dos dados → item exato), R8.7 (exclamação).

## Exemplo 4: condição

**Antes**

> Clique em **Enviar**. Caso apareça a mensagem de erro, verifique a conexão.

**Depois**

> 1. Clique em **Enviar**.
> 2. Se a mensagem `Falha na conexão` aparecer, verifique a conexão de rede.

**Regras aplicadas:** R1.1 (caso → se), R5.3 (condição antes da ação), R5.4 (passos numerados), R9.4 (mensagem exata).

## Exemplo 5: sintagma nominal longo

**Antes**

> Altere o parâmetro de tempo limite da conexão do pool de conexões do banco de dados de produção.

**Depois**

> No banco de dados de produção, altere o tempo limite de conexão do pool. O parâmetro é `pool.timeout`.

**Regras aplicadas:** R2.1 (encadeamento de mais de três substantivos), R1.4 (nome técnico em código).

## Exemplo 6: estrangeirismos informais

**Antes**

> Depois de buildar a aplicação, sete a variável `ENV`, starte o container e logue no painel para checar o status.

**Depois**

> 1. Compile a aplicação.
> 2. Defina a variável `ENV`.
> 3. Inicie o container.
> 4. Entre no painel.
> 5. Verifique o status do container.

**Regras aplicadas:** R1.7 (buildar, setar, startar, logar, checar), R5.2 (uma ação por passo).

## Exemplo 7: relatório de revisão

Se o pedido é uma revisão, entregue uma tabela neste formato:

| Trecho original | Regra | Texto novo |
|---|---|---|
| "Recomenda-se reiniciar o serviço." | R3.1 | "Reinicie o serviço." |
| "Efetue a validação dos dados." | R2.3 | "Valide os dados." |
| "O processo demora alguns minutos." | R9.4 | "O processo demora até 5 minutos." |
