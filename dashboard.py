

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Titolo
st.title("Dashboard Interattiva di Analisi Dati")

# Caricamento file CSV
uploaded_file = st.file_uploader("Carica un file CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("✅ Ecco un'anteprima del file:", df.head())

    # Seleziona la colonna da analizzare
    colonna = st.selectbox("Scegli una colonna numerica da analizzare", df.select_dtypes("number").columns)

    # Istogramma
    st.subheader(f"Istogramma di {colonna}")
    fig, ax = plt.subplots()
    ax.hist(df[colonna].dropna(), bins=20, color='skyblue', edgecolor='black')
    st.pyplot(fig)

    # Box plot
    st.subheader("Box Plot")
    fig_box, ax_box = plt.subplots()
    ax_box.boxplot(df[colonna].dropna())
    ax_box.set_title(f"Box plot di {colonna}")
    st.pyplot(fig_box)

    # Pie chart
    st.subheader("Grafico a Torta")
    pie_data = df[colonna].value_counts()
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
    ax_pie.axis('equal')
    st.pyplot(fig_pie)

    # Statistiche di base
    st.subheader("Statistiche")
    st.write(df[colonna].describe())

    # Salvataggio CSV
    if st.button("Salva report CSV"):
        report = df[colonna].describe().reset_index()
        report.to_csv("report_statistiche.csv", index=False)
        st.success("✅ Report salvato come report_statistiche.csv!")

    # Esportazione PDF
    if st.button("Esporta in PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Statistiche per {colonna}", ln=True, align='C')

        # Salva e inserisci istogramma
        fig.savefig("istogramma.png")
        pdf.image("istogramma.png", x=10, y=30, w=180)

        # Salva e inserisci boxplot
        fig_box.savefig("boxplot.png")
        pdf.add_page()
        pdf.image("boxplot.png", x=10, y=30, w=180)

        # Salva e inserisci piechart
        fig_pie.savefig("piechart.png")
        pdf.add_page()
        pdf.image("piechart.png", x=10, y=30, w=180)

        # Esporta PDF
        pdf.output("report.pdf")
        st.success("✅ Report esportato come report.pdf!")
