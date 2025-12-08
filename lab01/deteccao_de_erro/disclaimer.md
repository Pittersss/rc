# USO de IA no laboratório
Foi utilizado inteligência artificial para:
- Testar se o código da etapa 4.1 estava correto
- Após atestar que tinha alguns erros, pedimos para que a IA mostrasse a solução e explicasse o problema e a solução, os erros encontrados foram:
    - Uso errado da biblioteca CRC, requerendo configurações adicionais
    - Erro de passagem de parâmetro, passando um texto em ascii sendo que era para ser uma string binária
    - Na funcionalidade de preeencher os bits para formar um byte estavamos fazendo de maneira errada, impactando no cálculo do crc
- Gerar o código para o plot dos gráficos através do matplotlib na etapa 3
