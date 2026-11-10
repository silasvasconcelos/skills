# Dicionário controlado

Este dicionário tem três partes:

1. Verbos aprovados, cada um com um só significado.
2. Conectivos aprovados.
3. Termos não aprovados e a alternativa para cada termo.

O glossário do projeto tem prioridade sobre este dicionário. Se o glossário aprova um termo que este dicionário não aprova, use o termo do glossário.

Para adicionar um termo, coloque-o na tabela correta e escreva o significado aprovado. O verificador `scripts/verificar_ste.py` tem uma lista própria com os termos não aprovados mais comuns. Se você adicionar um termo não aprovado aqui, adicione-o também na lista `TERMOS_NAO_APROVADOS` do script.

## 1. Verbos aprovados

| Verbo | Significado aprovado | Não use para |
|---|---|---|
| abrir | Mostrar o conteúdo de um arquivo, uma tela ou um programa. | Iniciar um serviço ("iniciar"). |
| acessar | Entrar em uma tela, uma pasta ou um endereço. | Entrar no sistema com credenciais ("entrar"). |
| adicionar | Colocar um item novo em um conjunto. | Criar um item novo ("criar"). |
| alterar | Mudar o valor ou o conteúdo de um item que já existe. | — |
| baixar | Copiar um arquivo de um servidor para o computador local. | — |
| clicar | Pressionar o botão do mouse sobre um elemento. Use "clique em". | Escolher uma opção em lista ("selecionar"). |
| compilar | Transformar código-fonte em um programa executável. | — |
| configurar | Definir um conjunto de parâmetros para um sistema funcionar. | Atribuir um só valor ("definir"). |
| criar | Fazer um item novo que não existia. | — |
| definir | Atribuir um valor a um parâmetro ou a uma variável. | — |
| depurar | Procurar e corrigir a causa de um erro no código. | — |
| desinstalar | Tirar um programa do computador ou do servidor. | — |
| digitar | Escrever um valor com o teclado. | — |
| enviar | Transferir dados ou um arquivo para outro sistema. | — |
| entrar | Acessar um sistema com credenciais. | — |
| excluir | Apagar um registro ou um arquivo de forma permanente. | Tirar um item de um conjunto ("remover"). |
| executar | Fazer um programa, um comando ou um script funcionar. | Fazer uma tarefa manual ("fazer"). |
| implantar | Colocar uma versão de software em um ambiente. | Iniciar um serviço ("iniciar"). |
| iniciar | Fazer um serviço ou um processo começar a funcionar. | — |
| inicializar | Atribuir o valor inicial a uma variável ou a uma estrutura. | Iniciar um serviço ("iniciar"). |
| instalar | Colocar um programa no computador ou no servidor. | — |
| marcar | Ativar uma caixa de seleção. | — |
| desmarcar | Desativar uma caixa de seleção. | — |
| parar | Fazer um serviço ou um processo deixar de funcionar. | — |
| preencher | Escrever valores nos campos de um formulário. | Um só campo ("digitar"). |
| reiniciar | Parar e iniciar de novo um serviço, um processo ou um equipamento. | — |
| remover | Tirar um item de um conjunto sem apagar o item. | Apagar de forma permanente ("excluir"). |
| sair | Encerrar a sessão em um sistema. | — |
| salvar | Gravar as alterações de um arquivo ou de um formulário. | — |
| selecionar | Escolher uma opção em uma lista, um menu ou um grupo. | — |
| verificar | Examinar um estado ou um valor sem alterar o item. | — |

## 2. Conectivos aprovados

| Função | Conectivo aprovado |
|---|---|
| Sequência | depois, então, em seguida, antes de |
| Adição | e, também |
| Oposição | mas |
| Causa | porque |
| Consequência | por isso, então |
| Condição | se, quando |
| Finalidade | para, para que |
| Exemplo | por exemplo |

## 3. Termos não aprovados

### 3.1 Verbos e expressões verbais

| Não use | Use |
|---|---|
| utilizar | usar |
| possuir | ter |
| efetuar, realizar (com substantivo) | o verbo da ação: "efetue o login" → "entre no sistema" |
| proceder com, proceder à | o verbo da ação |
| encontra-se, se encontra | está, fica |
| disponibilizar | oferecer, publicar |
| viabilizar | permitir |
| deverá, poderá | deve, pode |
| é necessário que, faz-se necessário, se faz necessário | deve, ou o imperativo |
| vir a + infinitivo | o verbo direto: "vir a falhar" → "falhar" |
| estar + gerúndio (gerundismo) | presente ou futuro do presente |

### 3.2 Estrangeirismos informais

| Não use | Use |
|---|---|
| deletar | excluir |
| setar | definir, configurar |
| startar, dar start | iniciar |
| logar | entrar |
| deslogar | sair |
| printar | capturar a tela, imprimir |
| buildar | compilar, gerar o build |
| debugar | depurar |
| checar | verificar |
| rodar (um programa) | executar |
| subir (uma aplicação) | implantar (em um ambiente), iniciar (um serviço) |
| baixar (um serviço) | parar |

### 3.3 Conectivos e expressões rebuscadas

| Não use | Use |
|---|---|
| visando, objetivando, com o objetivo de, no intuito de, no sentido de | para |
| através de (sem sentido físico) | por, com, pelo |
| a nível de, em nível de | em, no |
| tendo em vista que, haja vista, em virtude de, devido ao fato de que | porque |
| uma vez que | porque, depois que |
| caso (conjunção) | se |
| mediante | com, por |
| sendo que | e, mas, porque, ou uma frase nova |
| enquanto (no sentido de "como") | como |
| destarte, outrossim, ademais, não obstante, conquanto | por isso, também, mas |
| assim sendo, dessa forma | por isso, então |
| eventualmente (no sentido de "no fim") | no fim; para "às vezes", use "às vezes" |

### 3.4 Pronomes e referências

| Não use | Use |
|---|---|
| o mesmo, a mesma (como pronome) | o substantivo, ele, ela |
| onde (sem sentido de lugar) | em que, no qual, na qual |
| abaixo, acima | a seguir, anterior, ou o nome do item |
| segue abaixo, segue em anexo | o item: "A tabela 1 mostra..." |

### 3.5 Cortesia, burocracia e linguagem vaga

| Não use | Use |
|---|---|
| por favor, favor, gentileza | (omita) |
| vimos por meio desta, informamos que | (omita) |
| a gente | (use o imperativo) |
| e/ou | A, B ou os dois |
| etc. (em procedimentos) | a lista completa |
| alguns, vários, diversos, rapidamente, em breve | o valor exato |

### 3.6 Termos não inclusivos

| Não use | Use |
|---|---|
| blacklist | lista de bloqueio |
| whitelist | lista de permissão |
| master, slave | primário, réplica |
