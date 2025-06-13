import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuration de la page avec un thème personnalisé
st.set_page_config(
    page_title="Dashboard de Production",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style personnalisé
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Titre de l'application avec un style amélioré
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>📊 Dashboard de Production</h1>", unsafe_allow_html=True)

# Sidebar pour les paramètres
st.sidebar.header("Paramètres")

# Sélection de la date avec plage de dates
date_range = st.sidebar.date_input(
    "Période d'analyse",
    value=(datetime.now() - timedelta(days=7), datetime.now()),
    max_value=datetime.now()
)

# Sélection du poste de travail
poste = st.sidebar.selectbox(
    "Poste de travail",
    ["Tous les postes", "Poste 1", "Poste 2", "Poste 3", "Poste 4"]
)

# Takt time
takt_time = st.sidebar.slider(
    "Takt Time (secondes)",
    min_value=0.1,
    max_value=10.0,
    value=1.0,
    step=0.1
)

# Filtres supplémentaires
st.sidebar.markdown("---")
st.sidebar.subheader("Filtres supplémentaires")
min_efficacite = st.sidebar.slider(
    "Efficacité minimale (%)",
    min_value=0,
    max_value=100,
    value=80
)

# Données de production (exemple amélioré)
def generate_data():
    np.random.seed(42)
    n_points = 24 * (date_range[1] - date_range[0]).days  # Nombre de points selon la plage de dates
    times = pd.date_range(start=date_range[0], end=date_range[1], freq='H')
    
    data = {
        'Heure': times,
        'Production': np.random.normal(100, 10, len(times)),
        'Objectif': [100] * len(times),
        'Efficacité': np.random.normal(95, 5, len(times)),
        'Défauts': np.random.poisson(2, len(times)),
        'Temps_Arrêt': np.random.exponential(0.5, len(times))
    }
    return pd.DataFrame(data)

df = generate_data()

# Filtrage des données
if poste != "Tous les postes":
    df = df[df['Poste'] == poste]
df = df[df['Efficacité'] >= min_efficacite]

# Métriques principales avec style amélioré
st.markdown("### Indicateurs de Performance")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Production Totale",
        value=f"{df['Production'].sum():.0f}",
        delta=f"{df['Production'].sum() - (100 * len(df)):.0f}",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="Efficacité Moyenne",
        value=f"{df['Efficacité'].mean():.1f}%",
        delta=f"{df['Efficacité'].mean() - 95:.1f}%",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="Taux de Défauts",
        value=f"{(df['Défauts'].sum() / df['Production'].sum() * 100):.1f}%",
        delta=None
    )

with col4:
    st.metric(
        label="Temps d'Arrêt",
        value=f"{df['Temps_Arrêt'].sum():.1f}h",
        delta=None
    )

# Graphiques améliorés
st.markdown("### Analyse de la Production")
col1, col2 = st.columns(2)

with col1:
    fig = px.line(df, x='Heure', y=['Production', 'Objectif'],
                  title="Production vs Objectif",
                  template="plotly_white")
    fig.update_layout(
        hovermode="x unified",
        showlegend=True,
        legend_title="",
        xaxis_title="Heure",
        yaxis_title="Production"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.line(df, x='Heure', y='Efficacité',
                  title="Efficacité de Production",
                  template="plotly_white")
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Heure",
        yaxis_title="Efficacité (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

# Nouveaux graphiques
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(df, x='Heure', y='Défauts',
                 title="Nombre de Défauts par Heure",
                 template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(df, x='Production', y='Efficacité',
                     title="Corrélation Production-Efficacité",
                     template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# Tableau de données avec style
st.markdown("### Données Brutes")
st.dataframe(
    df.style.background_gradient(subset=['Efficacité'], cmap='RdYlGn'),
    use_container_width=True
)

# Pied de page amélioré
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Dashboard créé avec Streamlit | © 2024</p>
        <p style='color: #666; font-size: 0.8em;'>Dernière mise à jour: {}</p>
    </div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True) 
