import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Climate AI App", layout="wide")

st.title("🌍 Climate Data Analysis App")
st.markdown("Application professionnelle d'analyse climatique")

st.sidebar.header("📂 Importer un fichier CSV")
uploaded_file = st.sidebar.file_uploader("Choisir un fichier", type=["csv"])

if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)
    st.subheader("Aperçu des données")
    st.dataframe(df.head())
    
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    if len(numeric_cols) > 0:
        
        st.subheader("Statistiques descriptives")
        st.write(df[numeric_cols].describe())
        
        variable = st.selectbox("Choisir une variable :", numeric_cols)
        
        fig = px.line(df, y=variable, title=f"Evolution de {variable}")
        st.plotly_chart(fig, use_container_width=True)
        
        date_col = st.selectbox("Choisir la colonne date :", df.columns)
        
        try:
            df[date_col] = pd.to_datetime(df[date_col])
            df["Mois"] = df[date_col].dt.month
            monthly_mean = df.groupby("Mois")[variable].mean().reset_index()
            
            fig2 = px.bar(monthly_mean, x="Mois", y=variable,
                          title="Moyenne Mensuelle")
            st.plotly_chart(fig2, use_container_width=True)
        except:
            st.warning("Colonne date invalide.")
        
        if st.checkbox("Calculer les anomalies"):
            mean_val = df[variable].mean()
            df["Anomalie"] = df[variable] - mean_val
            
            fig3 = px.line(df, y="Anomalie",
                           title="Anomalies")
            st.plotly_chart(fig3, use_container_width=True)
        
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Télécharger CSV",
                           csv,
                           "resultats_climat.csv",
                           "text/csv")
