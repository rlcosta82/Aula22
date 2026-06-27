import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    print('Obtendo os dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    df_recuperacao_veiculos = df_ocorrencias[['cisp', 'recuperacao_veiculos']] # delimitando as variáveis
    
    # Totalizando a recuperação de veículos por delegacia
    df_recuperacao_veiculos = df_recuperacao_veiculos.groupby('cisp', as_index=False)['recuperacao_veiculos'].sum()
    # print(df_recuperacao_veiculos)

    # ordenando o dataframe
    df_recuperacao_veiculos = df_recuperacao_veiculos.sort_values(by='recuperacao_veiculos', ascending=False)
    # print(df_recuperacao_veiculos)

except Exception as e:
    print(f'Erro ao obter dados {e}')

# Obter as medidas
try:
    print ('Calculando s medidas... ')
    array_recuperacao_veiculos = np.array(df_recuperacao_veiculos['recuperacao_veiculos'])

    media_recuperacao_veiculos = np.mean(array_recuperacao_veiculos)
    mediana_recuperacao_veiculos = np.median(array_recuperacao_veiculos)


    distancia = abs((media_recuperacao_veiculos - mediana_recuperacao_veiculos) / mediana_recuperacao_veiculos * 100)

    print('\nMedidas de Tendência Central')
    print(30*"=")
    print(f'Média: {media_recuperacao_veiculos}')
    print(f'Mediana: {mediana_recuperacao_veiculos}')
    print(f'Distância: {distancia}')

except Exception as e:
     print(f'Erro ao processar as medidas {e}')

# Obtendo a distribuição
try:
    print('Processando os quartis')

    q1 = np.quantile(array_recuperacao_veiculos, .25)
    q3 = np.quantile(array_recuperacao_veiculos, .75)

    print('\nQuartis')
    print(30*"=")
    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_recuperacao_veiculos}')
    print(f'Q3: {q3}')


    # Delegacia com menor recuperação de veículos
    df_recuperacao_veiculos_menores = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos'] < q1]

    # Delegacia com maior recuperação de veículos
    df_recuperacao_veiculos_maiores = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos'] > q3]

    print('\nDelegacia com menor recuperação de veículos: ')
    print(30*"=")
    print(df_recuperacao_veiculos_menores.sort_values(by='recuperacao_veiculos', ascending=True))

    print('\nDelegacia com maior recuperação de veículos: ')
    print(30*"=")
    print(df_recuperacao_veiculos_maiores)

except Exception as e:
    print(f'Erro ao obter a distribuição {e}')

# Obtendo medidas de dispersão
# Amplitude Total temos que obter o maior e o menor valor da distribuição.
    
try:
    maximo = np.max(array_recuperacao_veiculos)
    minimo = np.min(array_recuperacao_veiculos)
    amplitude = maximo - minimo

    print('\nMedidas de Dispersão')
    print(30*"=")
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude Total: {amplitude}')

except Exception as e:
    print(f'Erro ao calcular medidas de dispersão: {e}')

# Calcular Outliers
try:
    iqr = q3 - q1

    limite_inferior = q1 - (1.5 * iqr)

    limite_superior = q3 + (1.5 * iqr)


    print('\nMedidas ')
    print(30*"=")
    print(f'IQR: {iqr}')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_recuperacao_veiculos}')  # q2
    print(f'Q3: {q3}')
    print(f'Limite superior: {limite_superior}')
    print(f'Máximo: {maximo}')  

except Exception as e:
    print(f'Erro ao calcular os limites: {e}')

# Exibindo os outliers
try:
    # outliers superiores
    df_recuperacao_veiculos_outliers_superiores = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos'] > limite_superior]
    
    # outliers inferiores
    df_recuperacao_veiculos_outliers_inferiores = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos'] < limite_inferior]

    print('\nDelegacias c/ Outliers Inferiores ')
    print(30*"=")
    if len(df_recuperacao_veiculos_outliers_inferiores) == 0:
        print('Não existe outliers inferiores')
    else:
        print(df_recuperacao_veiculos_outliers_inferiores.sort_values(by='recuperacao_veiculos', ascending=True))


    print('\nDelegacias c/ Outliers Superiores ')
    print(30*"=")
    if len(df_recuperacao_veiculos_outliers_superiores) == 0:
        print('Não existe outliers superiores')
    else:
        print(df_recuperacao_veiculos_outliers_superiores.sort_values(by='recuperacao_veiculos', ascending=False))

except Exception as e:
    print(f'Erro ao Calular Outliers {e}')


try:
    assimetria = df_recuperacao_veiculos['recuperacao_veiculos'].skew()

    curtose = df_recuperacao_veiculos['recuperacao_veiculos']. kurtosis()

    print('\nMedidas de Distribuição')
    print(30*"=")
    print(f'Assimetria: {assimetria}')
    print(f'Curtose: {curtose}')

except Exception as e:
    print(f'Erro ao calcular medidas de distribuição {e}')

# Medidas de Variabilidade
try:
    print('Calculando variabilidade dos dados')

    variancia = np.var(array_recuperacao_veiculos)

    # Distância entre a Média e Variância
    distancia_var_media = variancia / (media_recuperacao_veiculos ** 2) * 100

    # Desvio Padrão
    desvio_padrao = np.std(array_recuperacao_veiculos)
   
    # Coeficiente de Variação
    coef_variacao = desvio_padrao / media_recuperacao_veiculos

    print('\nMedidas de Variabilidade')
    print(30*"=")
    print(f'Variância: {variancia}')
    print(f'Distância entre Variância e a Média: {distancia_var_media} %')
    print(f'Desvio Padrão: {desvio_padrao}')
    print(f'Coeficiente de Variação: {coef_variacao}')

except Exception as e:
    print(f'Erro ao calcular a variabilidade dos dados: {e}')


# Visualizando os dados
try:
    
    plt.subplots(2, 2, figsize=(18, 10))
    #color='blue'
    plt.suptitle('Recuperação de Veículos por Delegacia', fontsize=16, fontweight='bold')

    # POSIÇÃO 01 - BOXPLOT
    plt.subplot(2, 2, 1)
    plt.boxplot(array_recuperacao_veiculos, vert=False, showmeans=True) # showfliers=False 
    plt.title('Boxplot da Distribuição')

    # POSIÇÃO 2 - MEDIDAS
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_recuperacao_veiculos}', fontsize=9)
    plt.text(0.1, 0.8, f'Distância: {distancia}', fontsize=9)
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior}', fontsize=9)
    plt.text(0.1, 0.6, f'Mínimo: {minimo}', fontsize=9)      
    plt.text(0.1, 0.5, f'Q1: {q1}', fontsize=9)
    plt.text(0.1, 0.4, f'Mediana: {mediana_recuperacao_veiculos}', fontsize=9)
    plt.text(0.1, 0.3, f'Q3: {q3}', fontsize=9)
    plt.text(0.1, 0.2, f'Limite Superior: {limite_superior}', fontsize=9)
    plt.text(0.1, 0.1, f'Máximo: {maximo}', fontsize=9)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}', fontsize=9)

    plt.axis('off')
    plt.title('Resumo Estatístico')


    # POSIÇÃO 3 - OUTLIERS
    plt.subplot(2, 2, 3)
    df_recuperacao_veiculos_outliers_superiores = (
        df_recuperacao_veiculos_outliers_superiores
        .head(10)
        .sort_values(by='recuperacao_veiculos', ascending=False)
    )

    plt.bar(
        df_recuperacao_veiculos_outliers_superiores['cisp'],
        df_recuperacao_veiculos_outliers_superiores['recuperacao_veiculos'] 
    )

    # Espaço para afastar os valores, cada um de sua coluna
    deslocamento = max(df_recuperacao_veiculos_outliers_superiores['recuperacao_veiculos']) * 0.02

    for i, valor in enumerate(df_recuperacao_veiculos_outliers_superiores['recuperacao_veiculos']):
        plt.text(
            # i e valor, são usados como coordenadas q dão a posição dos valores no gráfico
            i, # posição X
            valor + deslocamento, # posição Y
            f'{valor:,}',
            ha='center'
        )

    plt.xticks(rotation=45, ha='right') # Rotaciona o texto do eixo X
    plt.title('Outliers Superiores')

    # POSIÇÃO 4 - HISTOGRAMA
    plt.subplot(2, 2, 4)
    plt.hist(array_recuperacao_veiculos, bins=393)
    plt.axvline(media_recuperacao_veiculos, color='green', linewidth=1, label='Média')
    plt.axvline(mediana_recuperacao_veiculos, color='orange', linewidth=1, label='Mediana')
    plt.legend() 

    contagens, limites = np.histogram(array_recuperacao_veiculos, bins=393)
    print('\nFaixas do Histograma')
    for i in range(len(contagens)):

        if contagens[i] > 0:
            print(
                f'Faixa {i+1} - '
                f'{limites[i]:.0f} até {limites[i+1]:.0f} recuperação de veículos'
                f'=> {contagens[i]} Delegacias'

        )


    plt.tight_layout()  # Ajusta o layout
    plt.show()

except Exception as e:
    print(f'Erro ao plotar o gráfico: {e}')
    