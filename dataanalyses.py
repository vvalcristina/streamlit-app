#Imports necessarios
import streamlit as st
import pandas as pd
import altair as alt

#Funções dos gráficos utilizados
def grafico_histograma(coluna, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin=True),
        y='count()', tooltip=[coluna, 'count()']
    ).interactive()
    return chart

#Grafico de Barras
def grafico_barras(coluna_num, coluna_cat, df):
    bars = alt.Chart(df, width=600).mark_bar().encode(
        x=alt.X(coluna_num, stack='zero'),
        y=alt.Y(coluna_cat),
        tooltip=[coluna_cat, coluna_num]
    ).interactive()
    return bars

#BoxPlot
def grafico_boxplot(coluna_num, coluna_cat, df):
    boxplot = alt.Chart(df, width=600).mark_boxplot().encode(
        x=coluna_num,
        y=coluna_cat
    )
    return boxplot

def grafico_scatterplot(x, y, color, df):
    scatter = alt.Chart(df, width=800, height=400).mark_circle().encode(
        alt.X(x),
        alt.Y(y),
        color = color,
        tooltip = [x,y]
    ).interactive()
    return scatter

def main():
    st.title('Análise Exploratória de Dados')
    st.write('Esta página é dedicada ao desenvolvimento de uma aplicação de análise de dados'
             'utilizando o framework de código aberto [Streamlit](https://www.streamlit.io/). ')
    st.image('logo.jpg', width=600)
    file = st.file_uploader('Escolha a base de dados que deseja analisar (.csv)', type='csv')
    if file is not None:
        df = pd.read_csv(file)

        st.subheader('**Conhecendo seu DataFrame**')
        st.markdown('**Número de linhas:**')
        st.markdown(df.shape[0])
        st.markdown('**Número de colunas:**')
        st.markdown(df.shape[1])

        st.markdown('**Visualizando o Dataframe**')
        number = st.slider('**Escolha o numero de linhas que deseja ver**', min_value=1, max_value=30)
        st.write('Você selecionou: ', number)
        st.dataframe(df.head(number))





        st.subheader('Estatística descritiva univariada')
        st.write('Inclui todos os métodos de Estatística Descritiva e da Estatística Inferencial'
                 'que permitem a análise de uma determinada variável ')

        #Criando um DataFrame auxiliar(aux) para a análise dos dados
        aux = pd.DataFrame({"colunas": df.columns, 'tipos':df.dtypes, 'NA #': df.isna().sum(),
                            'NA %': (df.isna().sum()/df.shape[0])*100})

        # Retorna o percentual de dados faltantes

        st.markdown('**Tabela com coluna e percentual de dados faltantes :**')
        st.table(aux[aux['NA #'] != 0][['tipos', 'NA %']])


        colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
        colunas_object = list(aux[aux['tipos'] == 'object']['colunas'])
        colunas = list(df.columns)

        col = st.selectbox('Selecione a coluna: ', colunas_numericas[1:])
        if col is not None:
            st.markdown('Selecione o que deseja analisar: ')
            mean = st.checkbox('Média')
            if mean:
                st.markdown(df[col].mean())
                st.write('A média é calculada somando-se todos os valores '
                         'de um conjunto de dados e dividindo-se pelo número de elementos deste conjunto.')
            median = st.checkbox('Mediana')
            if median:
                st.markdown(df[col].median())
                st.write('A mediana é o valor que separa um conjunto em duas quantidades iguais, ou seja,'
                         ' o valor central do conjunto.')
            desvio_pad = st.checkbox('Desvio Padrão')
            if desvio_pad:
                st.markdown(df[col].std())
                st.write('O desvio padrão é uma medida que expressa o grau de dispersão de um conjunto de dados, '
                         'ou seja, indica um quanto um conjunto de dados é uniforme.')
            kurtosis = st.checkbox('Kurtosis')
            if kurtosis:
                st.markdown(df[col].kurtosis())
                st.write('A Curtose (*kurtosis*) é a medida de dispersão que caracteriza o “achamento” '
                         'da curva de função de distribuição.')
            skewness = st.checkbox('Skewness')
            if skewness:
                st.markdown(df[col].skew())
                st.write('A *Skewness* mede a falta de simetria nos dados')
            describe = st.checkbox('Describe')
            if describe:
                st.table(df[col].describe().transpose())
        st.subheader('Visualização dos dados')
        st.markdown('Selecione a visualização')
        histograma = st.checkbox('Histograma')
        if histograma:
            col_num = st.selectbox('Selecione a Coluna Numérica', col, key='unique')
            st.markdown('Histograma da coluna: '+str(col_num))
            st.write(grafico_histograma(col_num,df))
        barras = st.checkbox('Gráfico de Barras')
        if barras:
            col_num_barras = st.selectbox('Selecione a Coluna Numérica', col, key='unique')
            col_cat_barras = st.selectbox('Selecione uma Coluna Categórica', colunas_object[1:], key='unique')
            st.markdown('Gráfico de Barras da Coluna' + str(colunas_numericas) + 'pela coluna ' +str(colunas_object))
            st.write(grafico_barras(col_num_barras, col_cat_barras, df))
        boxplot = st.checkbox('Boxplot')
        if boxplot:
            col_num_barras = st.selectbox('Selecione a Coluna Numérica', col, key='unique')
            col_cat_barras = st.selectbox('Selecione a uma Coluna Categórica', colunas_object[1:], key='unique')
            st.markdown('Gráfico de Barras da Coluna' + str(colunas_numericas) + 'pela coluna ' +str(colunas_object))
            st.write(grafico_barras(col_num_barras, col_cat_barras, df))

if __name__ == '__main__':
    main()

