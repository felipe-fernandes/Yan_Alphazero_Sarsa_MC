# Yan AI. AlphaZero - SARSA - MonteCarlo
Este estudo de Reinforcemnt Learning implementa 3 algoritmos diferentes para criar agentes capazes de jogar Yan.

* AlphaZero:
Baseado no tutorial AlphaZeroFromScratch https://youtu.be/wuSQpLinRB4?si=gzNRdX-jP0F1luZf
Existem alguns modelos pre-treinados dentro da pasta alphazero/models os parâmetros usados em cada modelo estão registrados em alphazero/modelsparams.json
Também é possível treinar seu próprio modelo usando alphazero/Train_ai.py
Para testar um modelo use alphazero/Test_Alphazero_Model.py

* SARSA:
Baseado no tutorial Python Implementation of On-Policy SARSA Temporal Difference Learning
https://aleksandarhaber.com/explanation-and-python-implementation-of-on-policy-sarsa-temporal-difference-learning-reinforcement-learning-tutorial/
Use sarsa/Sarsa.py para treinar e testar o desempenho médio do algorítimo. 
Use as variáveis num_game_train e num_game_test para ajustar quantidade de jogos para treinamentos e para teste.

* MonteCarlo:
Baseado no curso Stanford CS234: Reinforcement Learning | Winter 2019 
https://youtube.com/playlist?list=PLoROMvodv4rOSOPzutgyCTapiGlY2Nd8u&si=7ixPmngkAgj_teDR
Use montecarlo/Montecarlo.py para treinar e testar o desempenho médio do algorítimo. 
Use as variáveis num_game_train e num_game_test para ajustar quantidade de jogos para treinamentos e para teste.

# O que é Yan?
Yan é uma variação do clássico jogo de dados Yahtzee, trazendo regras específicas e uma abordagem única para incrementar a estratégia e a diversão. O jogo utiliza uma tabela com quatro colunas, cada uma com suas próprias regras de preenchimento. Para simplificar o estudo, somente uma das colunas foi implementada.

## Estrutura do Jogo
Cada rodada segue um formato simples, mas estratégico:

* Primeira Rolagem: Lance 5 dados de 6 faces.
* Após cada rolagem dos dados você pode registrar o padrão obtido ou selecionar quais dados quer lançar novamente em busca de uma combinação específica.
* Até Três Rolagens: É possível rolar os dados até três vezes em cada rodada visando obter o melhor padrão possível.
* Marcação: Após a terceira rolagem, o padrão final deve ser marcado na tabela. Se a combinação não se encaixar em nenhuma célula disponível, você deve registrar 0 em uma que ainda esteja vazia.
### Final do Jogo
O jogo termina quando todas as células da tabela estiverem preenchidas. A pontuação final é a soma de todos os valores registrados, incluindo bônus. Vence quem acumular mais pontos. Yan também pode ser jogado individualmente, permitindo que você desafie seu próprio recorde pessoal.

## Padrões da Tabela
### Parte Superior:
* Quantidade de Números (1, 2, 3, 4, 5 e 6):
    * Objetivo: Marcar o produto da face dos dados pelo número de dados com aquele valor.
    * Exemplo: Se você obtiver 3 dados com a face 3, marque 9 pontos na célula correspondente à face 3 (3 x 3 = 9 pontos).
    * Bônus: Se a soma total desta seção for de pelo menos 60 pontos, você receberá um bônus adicional de 30 pontos.

### Parte Inferior:
* Quadra:
    * Requisitos: Pelo menos 4 dados com a mesma face.
    * Pontuação: Multiplique o valor da face por 4 e adicione um bônus de 30 pontos.
    * Exemplo: Quatro dados com a face 5 resultam em 4 x 5 + 30 = 50 pontos.

* Full House:
     *Requisitos: Uma combinação de uma trinca (três dados iguais) e uma dupla (dois dados iguais).
    * Pontuação: Some os valores das faces e adicione um bônus de 20 pontos.
    * Exemplo: Três dados com a face 6 e dois com a face 5 somam 18 + 10 + 20 = 48 pontos.

* Sequência Máxima:
    * Requisitos: Uma sequência de 2, 3, 4, 5 e 6.
    * Pontuação: 60 pontos fixos.

* Sequência Mínima:
    * Requisitos: Uma sequência de 1, 2, 3, 4 e 5.
     *Pontuação: 50 pontos fixos.

* X+:
    * Requisitos: A soma das faces deve ser maior que o valor registrado em X-.
    * Pontuação:A soma das faces dos 5 dados.

* X-:
    * Requisitos: A soma das faces deve ser menor que o valor registrado em X+.
    * Pontuação:A soma das faces dos 5 dados.

* Yan:
    * Requisitos: Cinco dados com a mesma face.
    * Pontuação: Multiplique o valor da face por 5 e adicione um bônus de 50 pontos.
    * Exemplo: Cinco dados com a face 2 resultam em 5 x 2 + 50 = 60 pontos.



