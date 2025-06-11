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
def calculate_takt_time(weekly_production: int) -> float:
    """Calcule le takt time en minutes."""
    weekly_minutes = 5 * 8 * 60  # 5 jours, 8 heures, 60 minutes
    return weekly_minutes / weekly_production

@st.cache_data
def calculate_operators_needed(station_time: float, takt_time: float) -> int:
    """Calcule le nombre d'opérateurs nécessaires pour une station."""
    return max(1, int(np.ceil(station_time / takt_time)))

@st.cache_data
def calculate_station_load(station_time: float, takt_time: float, operators: int) -> float:
    """Calcule la charge d'une station en pourcentage."""
    return (station_time / (takt_time * operators)) * 100

@st.cache_data
def merge_stations(stations: Dict[str, Dict[str, float]], takt_time: float) -> Dict[str, Dict[str, float]]:
    """Fusionne les stations selon les critères définis."""
    merged_stations = stations.copy()
    to_merge = []
    
    # Identifier les stations à fusionner
    for station_name, posts in stations.items():
        total_load = sum(posts.values()) / takt_time
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
        
        # Saisie de la production hebdomadaire
        weekly_production = st.number_input(
            "Production hebdomadaire (robots/semaine)",
            min_value=1,
            value=85,
            step=1
        )
        
        # Calcul du takt time
        takt_time = calculate_takt_time(weekly_production)
        st.info(f"Takt Time: {takt_time:.2f} minutes")
        
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
                    
                    st.markdown(f"""
                        <div class="station-block">
                            <h4>{post_name}</h4>
                            <p>Temps: {time} min</p>
                            <p>Opérateurs: {'👤' * operators}</p>
                            <p>Charge: {load:.1f}%</p>
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
