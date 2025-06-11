# Simulation Ligne de Production

Cette application Streamlit simule une ligne de production industrielle pour la fabrication de robots, permettant de calculer automatiquement les besoins en opérateurs et l'organisation des postes de travail.

## 🚀 Installation

1. Clonez ce dépôt
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 🎯 Utilisation

Lancez l'application avec la commande :
```bash
streamlit run app.py
```

## 📋 Fonctionnalités

- Calcul automatique du takt time
- Simulation de 6 îlots de production + 1 chaîne finale
- Calcul automatique du nombre d'opérateurs nécessaires
- Fusion automatique des îlots sous-chargés
- Affichage visuel de la charge de travail
- Tableau de synthèse des indicateurs clés

## 🎨 Interface

- Design épuré en mode clair
- Interface responsive
- Visualisation claire des postes de travail
- Indicateurs de charge en temps réel

## 📊 Métriques calculées

- Takt time
- Nombre d'opérateurs par poste
- Charge de travail par poste
- Nombre total d'opérateurs
- Charge moyenne globale 