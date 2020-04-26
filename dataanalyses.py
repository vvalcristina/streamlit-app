# Imports necessarios
import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib as plt

# Funções dos gráficos utilizados

def grafico_histograma(coluna, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin=True),
        y='count()', tooltip=[coluna, 'count()']
    ).interactive()
    return chart


# Grafico de Barras
def grafico_barras(coluna_num, coluna_cat, df):
    bars = alt.Chart(df, width=600).mark_bar().encode(
        x=alt.X(coluna_num, stack='zero'),
        y=alt.Y(coluna_cat),
        tooltip=[coluna_cat, coluna_num]
    ).interactive()
    return bars


# BoxPlot
def grafico_boxplot(coluna_num, coluna_cat, df):
    boxplot = alt.Chart(df, width=600).mark_boxplot().encode(
        x=coluna_num,
        y=coluna_cat
    )
    return boxplot

#ScaterPlot
def grafico_scatterplot(x, y, df):
    scatter = alt.Chart(df, width=800, height=400).mark_circle().encode(
        alt.X(x),
        alt.Y(y),
        # color = '[200, 30, 0, 160]',
        tooltip=[x, y]
    ).interactive()
    return scatter

#Correlacao
def matriz_correlacao(numero):
    st.markdown('**Correlação:**')
    st.write('A [correlação](https://medium.com/brdata/correla%C3%A7%C3%A3o-direto-ao-ponto-9ec1d48735fb) é uma análise descritiva que mede se há e qual o grau de dependência entre duas variáveis')

    st.markdown('**Correlação de Pearson:** Também chamado de “coeficiente de correlação produto-momento” ou simplesmente '
                'de “ρ de Pearson” mede o grau da correlação (e a direção dessa correlação — se positiva ou negativa) entre '
                'duas variáveis. Este coeficiente, normalmente representado por ρ assume apenas valores entre -1 e 1.')

    st.markdown('**Correlação de Spearman:** Indicado para o cálculo da correlação entre variáveis aleatórias x e y '
                'relacionadas monotonicamente entre si, mas não necessariamente de maneira linear. Se a relação é linear '
                'o método de Pearson é o mais indicado.')

    st.markdown('**Correlação de Kendall:** É uma medida de correlação de postos, ou seja, verifica a semelhança entre'
                ' as ordens dos dados quando classificados por cada uma das quantidades.')

    st.markdown('O tipo de correlação mais adequado pra cada situação varia de acordo com o problema.')

    var_corr = st.multiselect('Selecione as variáveis:', list(numero.columns), default=list(numero.columns))

    corr_metodo = st.radio('Selecione o método de correlação', ('Pearson','Spearman','Kendall'))

    if(var_corr) == 0:
        var_corr = list(numero)
    corr = numero[var_corr].corr(method=corr_metodo[0].lower() + corr_metodo[1:])
    st.markdown('**Tabela de Correlação**')
    st.write(corr)
    st.markdown('**Matriz de Correlação')
    st.write('Para grande bases de dados a matriz de correlação pode ser mais adequada')
    sns.heatmap(corr, fmt='.2f', square=True, annot=True)
    st.pyplot()


def main():
    st.title('Análise Exploratória de Dados')
    st.write('Esta página é dedicada ao desenvolvimento de uma aplicação de análise de dados'
             'proposta pelo Prof. Tulio Nogueira durante a Semana 3- do AceleraDev DataScience'
             'utilizando o framework de código aberto [Streamlit](https://www.streamlit.io/). ')
    st.image('logo.jpg', width=600)
    file = st.file_uploader('Faça upload da base de dados que deseja analisar (.csv)', type='csv')
    st.markdown('**Valéria Cristina Silva**')
    st.write('[Github](https://github.com/vvalcristina/streamlit-app)')
    st.write('[Linkedin](https://www.linkedin.com/in/valeria-cristina/)')
    if file is not None:
        df = pd.read_csv(file)
        st.subheader('**Conhecendo sua base de dados**')
        st.write('O arquivo de sua base de dados possui ', df.shape[0],' linhas e ', df.shape[1],' colunas.')

        st.markdown('**Visualizando o Dataframe**')
        number = st.slider('Escolha o numero de linhas que deseja ver', min_value=2, max_value=10)
        st.write('Você selecionou: ', number, 'linhas.')
        st.dataframe(df.head(number))

        # Criando um DataFrame auxiliar(aux) para a análise dos dados
        #Esse dataframe retorna as colunas, os tipos de cada variável e a soma e porcentagem dos dados faltantes
        aux = pd.DataFrame({"colunas": df.columns, 'tipos': df.dtypes, 'NA #': df.isna().sum(),
                            'NA %': (df.isna().sum() / df.shape[0]) * 100})
        st.markdown('**Qualidade dos dados:** ')
        st.write('A qualidade dos dados é de extrema importância para a análise. Verificar e tratar valores'
                 'ausentes (nulos), assim como conhecer os tipos de dados analisados, é um dos primeiros passos'
                 'para uma análise consistente. ')
        st.write('Valores ausentes não tratados podem impactar na análise, podendo gerar conclusões equivocadas.')

        # Separando as variáveis numéricas e as variáveis categóricas
        st.markdown('**Variáveis numéricas: **')
        st.write('As variáveis numéricas são as variáveis que podem ser medidas numa escala quantitativa,'
                 'ou seja, apresentam valores numéricos que fazem sentido. Podem ser mensuradas através da '
                 'média, desvio padrão, valores máximos e mínimos por exemplo ')
        colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
        st.table(colunas_numericas)

        st.markdown('**Variáveis Categóricas:')
        st.write('As variáveis categóricas dizem respeito as variáveis qualitativas que podem ser medidas em '
                 'várias categorias, podendo ser nominais ou ordinais')
        colunas_object = list(aux[aux['tipos'] == 'object']['colunas'])
        st.table(colunas_object)

        colunas = list(df.columns)

        st.subheader('**Estatística Descritiva Univariada**')
        st.write(' A Estatística Univariada inclui todos os métodos de Estatística Descritiva e '
                 'da Estatística Inferencial que permitem a análise de uma determinada variável ')
        st.write('A estatística descritiva diz respeito as variáveis numéricas')
        col = st.selectbox('Selecione a coluna: ', colunas_numericas[1:])

        if col is not None:
            st.markdown('Selecione o que deseja analisar: ')
            mean = st.checkbox('Média')
            if mean:
                st.markdown(df[col].mean())
                st.write('A média é calculada somando-se todos os valores '
                         'de um conjunto de dados e dividindo-se pelo número de elementos deste conjunto.')
                st.image('media.png', width=600)
            median = st.checkbox('Mediana')
            if median:
                st.markdown(df[col].median())
                st.write('A mediana é o valor que separa um conjunto em duas quantidades iguais, ou seja,'
                         ' o valor central do conjunto.')
            desvio_pad = st.checkbox('Desvio Padrão')
            if desvio_pad:
                st.markdown(df[col].std())
                st.write('O desvio padrão é uma medida que expressa o grau de dispersão de um conjunto de dados, '
                         'ou seja, indica um quanto um conjunto de dados é uniforme. Quanto mais próximo de zero'
                         'mais uniforme o conjunto de dados')
            kurtosis = st.checkbox('Kurtosis')
            if kurtosis:
                st.markdown(df[col].kurtosis())
                st.write('A Curtose (kurtosis) é a medida de dispersão que caracteriza o “achamento” '
                         'da curva de função de distribuição. É medida em relação a curva Gaussiana '
                         '(normal).')
                st.write('Uma curva leptocúrtica (>0) tem sua distribuiçãi mais afuniladam com pico '
                         'maior que o de uma distribuição Gaussiana e com caudas pesadas.')
                st.write('Uma curva platicúrtica tem sua função de distribuição mais achatada que a '
                         'Gaussiana.')
                st.image('kurtosis.jpg', width=600)
            skewness = st.checkbox('Skewness')
            if skewness:
                st.markdown(df[col].skew())
                st.write('A Skewness mede a falta de simetria nos dados. Diferencia os valores extremos em uma '
                         'cauda versus a outra. O valor de skewness em uma curva simétrica é zero.')
                st.image('skewness.png', width=600)
            describe = st.checkbox('Describe')
            if describe:
                st.table(df[col].describe().transpose())
                st.write('')
        st.subheader('Estatística Descritiva Bivariada/ Multivariada')
        st.write('A estatística descritiva bivariada/multivariada diz respeito ao relacionamento entre os '
                 'pares ou conjunto de variáveis como um todo.')


        matriz_correlacao(df[colunas_numericas])


        st.markdown('**Visualizações dos dados**')

        st.write('Aqui temos alguns exemplos mais comuns de visualização dos dados de forma gráfica. A melhor forma de'
                 'visualização depende muito dos tipos de dados analisados.')

        histograma = st.checkbox('Histograma')
        if histograma:
            col_num = st.selectbox('Selecione a Coluna Numérica', colunas_numericas[1:], key='unique')
            st.markdown('Histograma da coluna: ' + str(col_num))
            st.write('O histograma é a distribuição de frequências  de uma amostra de forma gráfica.Quando o volume de '
                     'dados aumenta indefinidamente dentro do conjunto de dados e o intervalo de classes tende a zero (o'
                     ' que torna os retângulos cada vez mais finos e altos), a distribuição de frequência torna–se uma '
                     'distribuição de densidade de probabilidades')


        barras = st.checkbox('Gráfico de Barras')
        if barras:
            col_num_barras = st.selectbox('Selecione a Coluna Numérica', colunas_numericas[1:], key='unique')
            col_cat_barras = st.selectbox('Selecione uma Coluna Categórica', colunas_object[1:], key='unique')
            st.write(grafico_barras(col_num_barras, col_cat_barras, df))
            st.write('O gráfico de barras  gráfico de barras é utilizado para realizar comparações entre as categorias '
                     'de uma variável qualitativa ou quantitativa discreta')

        boxplot = st.checkbox('Boxplot')
        if boxplot:
            col_num_barras = st.selectbox('Selecione a Coluna Numérica', colunas_numericas[1:], key='unique')
            col_cat_barras = st.selectbox('Selecione a uma Coluna Categórica', colunas_object[1:], key='unique')
            st.write(grafico_boxplot(col_num_barras, col_cat_barras, df))
            st.write('Representa a variação de dados observados de uma variável numérica por meio de quartis. Os outliers'
                     'ficam como pontos individuais')


        scatter = st.checkbox('ScatterPlot')
        if scatter:
            col_num_barras = st.selectbox('Selecione a Coluna Numérica', colunas_numericas[1:], key='unique')
            col_cat_barras = st.selectbox('Selecione a uma Coluna Categórica', colunas_object[1:], key='unique')
            st.write(grafico_scatterplot(col_num_barras, col_cat_barras, df))
            st.write('O gráfico de dispersão utiliza coordenadas cartesianas para exibir valores de um conjunto de dados.'
                     'Cada ponto é o valor de uma variável')


if __name__ == '__main__':
    main()
