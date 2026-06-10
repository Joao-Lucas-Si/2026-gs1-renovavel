# GS - Soluções em Energias Renováveis e sustentáveis

Este é um repositório para o projeto de Global Solution para a máteria Soluções em Energias Renováveis e Sustentáveis, propondo um sistema simulador de missão espacial centralizado no gerenciamento de energia e impacto de uso.

## Integrantes

- João Lucas Silva Lopes – RM: 573875
- Alan Otalvaro – RM: 571794
- João Pedro Evangelista – RM: 573899

## Como Executar

clone o repositório em seu dispositivo:

```
git clone https://github.com/Joao-Lucas-Si/2026-gs1-renovavel.git
```

depois rode o arquivo main.py

```
python main.py
```

deixe o terminal em uma largura e tamanho consideraveis, o projeto tenta replicar um conceito de tui(terminal user interface), então aparecerá imagens ascii, textos, cores e tabelas formatadas, então um terminal pequeno ter uma aparecia confusa devido ao limite de espaços

## Funcionamento

o projeto funciona atráves de três etapas, construção, missão e finalização

### 1. construção

a construção de nave é a primeira etapa que ocorre no projeto, onde o usuário poderá escolher as peças usadas na nave, para escolher uma peça o usuário teverá ter em mente que ele tem um orçamento limitado, gerado por um calculo derivado pelo tempo que a missão demorará, que é gerado aleátoriamente. cada peça tem seu foco e preço, sempre que o usuário vai comprar uma parte de uma categoria, o orçamento será um valor desconsiderando o preço da peça já presente.

#### propulsores

parte responsável por lançar o foguete, sempre vem uma já escolhida por padrão, dependendo do propulsor usado, o tempo de missão diminuirá

#### Bateria

peça que representa o estoque de combustivel, pode aumentar a quantidade de energia máxima da nave, também já vem com uma opção preselecionada.

#### Gerador

peça opcional, gera energia em cada ciclo da missão, há versões poluentes e não poluentes, as poluentes apresenta uma estatistica simbolica de impacto causado.

### 2. missão

a missão é a parte principal, nela ocorre um processo de ciclos, que representam o tempo passando, dentro de cada ciclo temos os parâmetros adicionais, eles são valores que representam a estabilidade da missão, mas são subvergientes a energia da nave, cada um deles representa um custo operacional que diminui energia a cada ciclo, o usuário deve saber administrar para conseguir ter energia suficiente até o fim da missão, mas também tenha parâmetros em valores funcionais, caso alguma dessas duas condições não for cumprida, resultará em falha total da missão.

Cada parâmetro tem uma quantidade de energia máxima que pode consumir por ciclo, mas o usuário pode escolher a porcentagem que será usada, quanto mais próximo do consumo de energia total, maior o valor produzido, também ocorrendo o inverso.

#### Tabela de consumo

| Parâmetro   | Consumo máximo |
| ----------- | -------------- |
| Temperatura | 20             |
| Oxigênio    | 30             |
| Modulo      | 40             |
| Comunicação | 20             |

#### produção

todos os paramêtros produzem a mesma quantidade final derivada de sua porcentagem

| energia distribuida | produção |
| ------------------- | -------- |
| 25%                 | 7        |
| 50%                 | 15       |
| 75%                 | 22       |
| 100%                | 30       |

#### gastos

além dos custos e produção, os parâmetros tem estados, os estados representam o quanto seus valores são gastos em cada ciclo, caso os gasto façam o valor chegar em 0, a distribuição de energia deve ser feita a partir disso, tentando reverter as consequencias dos estados. um estado é escolhido aleátoriamente para cada parâmetro, junto a um tempo de duração que estabelece por quantos ciclos o estado permanecerá, quando a duração acaba outro estado é gerado, além disso, os gastos de um estado são valores pseudo aleátorios dentro de um intervalo numérico.

| estado  | gasto   |
| ------- | ------- |
| ESTAVEL | 20 a 30 |
| ATENCAO | 10 a 20 |
| CRITICO | 5 a 10  |

### 3. final

no fim da simulação, se for uma falha ou um sucesso, aparecerá uma tela de finalização, com alguns dados e imagens
