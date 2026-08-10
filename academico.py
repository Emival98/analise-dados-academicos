import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st



COR_PRINCIPAL = "#1f77b4"

PALETA_RORXO = [
        "#1f77b4",
        "#ff7f0e",
        "#A855F7",
        "#C4B5FD",
        "#E9D5FF"
]

@st.cache_data
def carregar_dados(arquivo):
    # Carregamento dos dados 
    dados = pd.read_csv(arquivo)


    #-----------------------------------Tratamento dos dados--------------------------------------------------
    # Criação do coluna  Nota_Final
    dados["nota_final"] = dados["nota1"]*0.3+dados["nota2"]*0.3+dados["nota3"]*0.4


    # Coluna situação
    dados["situacao"] = np.where(dados['nota_final'] >= 14, 'Aprovado',
                                    np.where(dados['nota_final']>=10, 'Exame', 'Reprovado'))


    
    return dados

df = carregar_dados("academico.csv")

# Estatisticas 
media = df["nota_final"].mean()
mediana = df["nota_final"].median()
moda = df["nota_final"].mode()[0]
variancia = df["nota_final"].var()
desvio_padrao= df['nota_final'].std()
qtd_aprovados = len(df.query('situacao== "Aprovado"'))
qtd_exame = len(df.query('situacao== "Exame"'))
qtd_reprovados = len(df.query('situacao== "Reprovado"'))
qtd_alunos = len (df)



valores = {
    "media das notas":media,
    "mediana": mediana,
    "moda": moda,
    "variância": variancia,
    "desvio padrao": desvio_padrao,
    "reprovados":qtd_reprovados,
    "aprovados": qtd_aprovados,
    "exame": qtd_exame,
    "numero de alunos": qtd_alunos
}

# Configuraça da página
st.set_page_config(page_title="Gestão Acadêmica de Emival",
                   page_icon="📚", layout="wide")

st.title("Gestão Academica")
st.caption(f"Lendo os histórico acadêmicos de {valores['numero de alunos']} estudantes")
st.markdown("---")

# Configarção do painel lateral da página
st.sidebar.title("Filtro dos estudantes")

#------------Filtros de multi seleção
genero = st.sidebar.multiselect(
    "Género", 
    options=sorted(df["genero"].unique()),
    default=sorted(df["genero"].unique())

)

curso = st.sidebar.multiselect(
    "Curso", 
    options=sorted(df["curso"].unique()),
    default=sorted(df["curso"].unique())

)

situacao = st.sidebar.multiselect(
    "Situação", 
    options=sorted(df["situacao"].unique()),
    default=sorted(df["situacao"].unique())

)

df_filtrado = df[
           (df["genero"].isin(genero)) &
            (df["curso"].isin(curso)) &
            (df["situacao"].isin(situacao))
                 ]

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com o filtro selecionado, Altere o filtro.")
    st.stop()


# Apresetação das métricas estatísticas

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    taxa = (valores["aprovados"]/valores["numero de alunos"])*100
    st.metric("Taxa de aproveitamento", f"{taxa:.2f}%")
with col2:
    st.metric("Quantidade Aprovados", valores["aprovados"])
with col3:
    st.metric("Quantidade Reprovados", valores["reprovados"])
with col4:
    st.metric("Quantidade Exame", valores["exame"])
with col5:
    st.metric("Media das Notas", f"{df['nota_final'].mean():.2f}")

st.markdown("---")

#-----------------------------------Apresentação dos gráficos--------------------------------------------------

# Gráfico de Barra
col_barras, col_pizza = st.columns(2)

with col_barras:
    st.subheader("Quantidade de aprovados por curso")
    at_situacao = df.query('situacao== "Aprovado"').groupby("curso")["situacao"].count().reset_index()
    at_situacao = at_situacao.sort_values('situacao', ascending=True)

    fig_bar , ax_bar = plt.subplots()
    ax_bar.barh(at_situacao['curso'], at_situacao['situacao'], color = COR_PRINCIPAL)
    #plt.title("Quantidade Aprovados por curso")
    ax_bar.set_xlabel("Curso")
    ax_bar.set_ylabel("Quantidade")
    

    st.pyplot(fig_bar)

# Gráfico de Pizza
with col_pizza:
    st.subheader("Distirbuição de aprovados por sexo")
    qtd_aprovados_sexo = df.query('situacao== "Aprovado"').groupby("genero")["situacao"].count().reset_index()
    qtd_aprovados_sexo["genero"] = np.where(qtd_aprovados_sexo["genero"] == 'F', 'Feminino', 'Masculino')


    fig_pizza, ax_pizza = plt.subplots()

    ax_pizza.pie(x=qtd_aprovados_sexo['situacao'],labels=qtd_aprovados_sexo['genero'], colors=PALETA_RORXO, autopct="%.1f%%", pctdistance=0.7, labeldistance=1.15)
    ax_pizza.legend(labels=qtd_aprovados_sexo["genero"])
    #plt.title("Distirbuição de aprovados por sexo")
    ax_pizza.axis('equal')
    st.pyplot(fig_pizza)
    



with st.expander ("Ver a tabela dos estudantes"):
    st.dataframe(df_filtrado.sort_values("nota_final"), use_container_width=True)
