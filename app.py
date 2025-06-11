import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

# Configuration de la page
st.set_page_config(
    page_title="Simulation Ligne de Production",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .station-block {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #e8f4f8;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Données de base des îlots et postes
STATIONS_DATA = {
    "Contrôle": {"C1": 15, "C2": 12, "C3": 18},
    "Montage": {"M1": 20, "M2": 25, "M3": 22},
    "Soudure": {"S1": 30, "S2": 28},
    "Peinture": {"P1": 45, "P2": 40},
    "Électronique": {"E1": 35, "E2": 32, "E3": 38},
    "Test": {"T1": 25, "T2": 28},
    "Chaîne Finale": {"F1": 20}
}

@st.cache_data
def calculate_weekly_production(takt_time_hours: float) -> int:
    """Calcule la production hebdomadaire à partir du takt time en heures."""
    weekly_hours = 5 * 8  # 5 jours, 8 heures
    return int(weekly_hours / takt_time_hours)

@st.cache_data
def calculate_operators_needed(station_time: float, takt_time_hours: float) -> int:
    """Calcule le nombre d'opérateurs nécessaires pour une station."""
    takt_time_minutes = takt_time_hours * 60
    return max(1, int(np.ceil(station_time / takt_time_minutes)))

@st.cache_data
def calculate_station_load(station_time: float, takt_time_hours: float, operators: int) -> float:
    """Calcule la charge d'une station en pourcentage."""
    takt_time_minutes = takt_time_hours * 60
    return (station_time / (takt_time_minutes * operators)) * 100

@st.cache_data
def merge_stations(stations: Dict[str, Dict[str, float]], takt_time_hours: float) -> Dict[str, Dict[str, float]]:
    """Fusionne les stations selon les critères définis."""
    merged_stations = stations.copy()
    to_merge = []
    
    # Identifier les stations à fusionner
    for station_name, posts in stations.items():
        total_load = sum(posts.values()) / (takt_time_hours * 60)
        if total_load < 0.6 or len(posts) < 2:
            to_merge.append(station_name)
    
    # Fusionner les stations
    if to_merge:
        for station in to_merge:
            if station in merged_stations:
                del merged_stations[station]
                # Ajouter les postes à la station la plus proche
                nearest_station = min(
                    [s for s in merged_stations.keys() if s != station],
                    key=lambda x: abs(len(merged_stations[x]) - len(stations[station]))
                )
                merged_stations[nearest_station].update(stations[station])
    
    return merged_stations

def main():
    try:
        st.title("🏭 Simulation Ligne de Production")
        
        # Création de deux colonnes pour les entrées
        col1, col2 = st.columns(2)
        
        with col1:
            # Saisie du takt time avec un curseur
            takt_time = st.slider(
                "Takt Time (heures)",
                min_value=0.2,
                max_value=0.6,
                value=0.47,  # Valeur par défaut (environ 85 robots/semaine)
                step=0.01,
                help="Temps disponible entre chaque unité produite (en heures)"
            )
            
            # Affichage du takt time en format détaillé
            st.markdown(f"""
                <div class="info-box">
                    <p>Takt Time détaillé :</p>
                    <ul>
                        <li>{takt_time:.2f} heures</li>
                        <li>{takt_time*60:.1f} minutes</li>
                        <li>{takt_time*3600:.0f} secondes</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Affichage de la production hebdomadaire calculée
            weekly_production = calculate_weekly_production(takt_time)
            st.metric(
                "Production hebdomadaire calculée",
                f"{weekly_production} robots/semaine",
                help="Calculé à partir du takt time : (5 jours × 8 heures) ÷ takt time"
            )
        
        # Explication du calcul de la charge
        st.markdown("""
            <div class="info-box">
                <h4>📊 Comment est calculée la charge ?</h4>
                <p>La charge d'un poste est calculée comme suit :</p>
                <ul>
                    <li>Charge (%) = (Temps du poste ÷ (Takt Time × Nombre d'opérateurs)) × 100</li>
                    <li>Si la charge > 100% : le poste est surchargé</li>
                    <li>Si la charge < 60% : le poste est sous-chargé</li>
                </ul>
                <p>Le nombre d'opérateurs est calculé pour maintenir la charge sous 100%.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Fusion des stations si nécessaire
        merged_stations = merge_stations(STATIONS_DATA, takt_time)
        
        # Affichage des stations
        for station_name, posts in merged_stations.items():
            st.subheader(f"Îlot {station_name}")
            cols = st.columns(len(posts))
            
            for col, (post_name, time) in zip(cols, posts.items()):
                with col:
                    operators = calculate_operators_needed(time, takt_time)
                    load = calculate_station_load(time, takt_time, operators)
                    
                    # Déterminer la couleur en fonction de la charge
                    load_color = "red" if load > 100 else "green" if load < 60 else "orange"
                    
                    st.markdown(f"""
                        <div class="station-block">
                            <h4>{post_name}</h4>
                            <p>Temps: {time} min</p>
                            <p>Opérateurs: {'👤' * operators}</p>
                            <p style="color: {load_color};">Charge: {load:.1f}%</p>
                        </div>
                    """, unsafe_allow_html=True)
        
        # Tableau de synthèse
        st.subheader("📊 Tableau de Synthèse")
        
        total_operators = sum(
            sum(calculate_operators_needed(time, takt_time) for time in posts.values())
            for posts in merged_stations.values()
        )
        
        total_posts = sum(len(posts) for posts in merged_stations.values())
        
        summary_data = {
            "Métrique": [
                "Îlots actifs",
                "Îlots fusionnés",
                "Total postes",
                "Total opérateurs",
                "Charge moyenne"
            ],
            "Valeur": [
                len(merged_stations),
                len(STATIONS_DATA) - len(merged_stations),
                total_posts,
                total_operators,
                f"{sum(calculate_station_load(time, takt_time, calculate_operators_needed(time, takt_time)) for posts in merged_stations.values() for time in posts.values()) / total_posts:.1f}%"
            ]
        }
        
        st.table(pd.DataFrame(summary_data))
        
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")
        st.stop()

if __name__ == "__main__":
    main() 
