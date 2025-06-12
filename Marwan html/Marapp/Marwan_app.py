"""
Application Romantique - 6 Mois d'Amour
---------------------------------------
Pour installer les dépendances :
pip install -r requir.txt

Pour lancer l'application :
streamlit run Marwan_app.py
"""

import streamlit as st
import random
import time
from PIL import Image
import base64
from io import BytesIO

# Configuration de la page
st.set_page_config(
    page_title="6 Mois d'Amour",
    page_icon="❤️",
    layout="centered"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .stButton>button {
        background-color: #ff69b4;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        font-size: 18px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff1493;
    }
    .memory-image {
        border-radius: 15px;
        margin: 20px 0;
    }
    .heart {
        font-size: 30px;
        animation: float 2s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    </style>
    """, unsafe_allow_html=True)

# Données du quiz
quiz_data = [
    {
        "image": "images/memory1.jpg",
        "question": "Où avons-nous eu notre premier rendez-vous ?",
        "answers": ["Au cinéma", "Au restaurant", "Dans un parc", "À la plage"],
        "correct": 1
    },
    {
        "image": "images/memory2.jpg",
        "question": "Quel est mon plat préféré ?",
        "answers": ["Pizza", "Sushi", "Pâtes", "Burger"],
        "correct": 2
    },
    {
        "image": "images/memory3.jpg",
        "question": "Quelle est notre chanson ?",
        "answers": ["Perfect - Ed Sheeran", "All of Me - John Legend", 
                   "Thinking Out Loud - Ed Sheeran", "A Thousand Years - Christina Perri"],
        "correct": 0
    },
    {
        "image": "images/memory4.jpg",
        "question": "Quel est mon film préféré ?",
        "answers": ["Titanic", "Notebook", "La La Land", "Before Sunrise"],
        "correct": 1
    },
    {
        "image": "images/memory5.jpg",
        "question": "Quelle est ma couleur préférée ?",
        "answers": ["Bleu", "Rose", "Vert", "Rouge"],
        "correct": 1
    },
    {
        "image": "images/memory6.jpg",
        "question": "Quel est mon rêve ?",
        "answers": ["Voyager autour du monde", "Avoir une grande maison", 
                   "Devenir célèbre", "Avoir une famille"],
        "correct": 0
    }
]

# Initialisation des variables de session
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'hearts_found' not in st.session_state:
    st.session_state.hearts_found = 0
if 'game_time' not in st.session_state:
    st.session_state.game_time = 30

def load_image(image_path):
    try:
        return Image.open(image_path)
    except:
        return None

def show_quiz():
    if st.session_state.current_question < len(quiz_data):
        question = quiz_data[st.session_state.current_question]
        
        # Afficher l'image
        image = load_image(question["image"])
        if image:
            st.image(image, use_column_width=True, caption="Photo souvenir")
        
        # Afficher la question
        st.markdown(f"### {question['question']}")
        
        # Afficher les réponses
        for i, answer in enumerate(question["answers"]):
            if st.button(answer, key=f"q{st.session_state.current_question}a{i}"):
                if i == question["correct"]:
                    st.session_state.score += 1
                    st.success("Bonne réponse ! ❤️")
                else:
                    st.error("Mauvaise réponse... 💔")
                time.sleep(1)
                st.session_state.current_question += 1
                st.experimental_rerun()
        
        # Afficher la progression
        st.progress((st.session_state.current_question + 1) / len(quiz_data))
        st.markdown(f"Question {st.session_state.current_question + 1} sur {len(quiz_data)}")
    else:
        if st.session_state.score >= 4:
            show_game()
        else:
            show_fail()

def show_game():
    st.markdown("### Trouve et clique sur tous les cœurs cachés !")
    
    # Créer une grille de 5x5 pour les cœurs
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            if st.button("❤️", key=f"heart{i}"):
                st.session_state.hearts_found += 1
                st.success("Cœur trouvé !")
    
    # Afficher le nombre de cœurs trouvés
    st.markdown(f"Cœurs trouvés : {st.session_state.hearts_found}/5")
    
    # Timer
    if st.session_state.game_time > 0:
        st.progress(st.session_state.game_time / 30)
        st.session_state.game_time -= 1
        time.sleep(1)
        st.experimental_rerun()
    else:
        show_fail()
    
    # Vérifier la victoire
    if st.session_state.hearts_found >= 5:
        show_victory()

def show_victory():
    st.balloons()
    st.markdown("## 🎉 Tu as gagné ! 🎉")
    st.markdown("### Bravo mon amour ! Tu connais vraiment bien notre histoire 💖")
    st.markdown("### Maintenant… va dans ta voiture. Une surprise t'attend 💝")
    if st.button("Rejouer"):
        reset_game()

def show_fail():
    st.markdown("## Oops !")
    st.markdown("Tu peux retenter ta chance mon cœur 💕")
    st.markdown("Il faut au moins 4 bonnes réponses sur 6 pour débloquer la surprise…")
    if st.button("Réessayer"):
        reset_game()

def reset_game():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.game_started = False
    st.session_state.hearts_found = 0
    st.session_state.game_time = 30
    st.experimental_rerun()

# Page principale
if not st.session_state.game_started:
    st.markdown("# 6 Mois d'Amour")
    image = load_image("images/photo-couple.jpg")
    if image:
        st.image(image, use_column_width=True)
    st.markdown("## Mon cœur, voilà déjà 6 mois que tu illumines ma vie ✨")
    if st.button("Commencer l'aventure"):
        st.session_state.game_started = True
        st.experimental_rerun()
else:
    show_quiz() 