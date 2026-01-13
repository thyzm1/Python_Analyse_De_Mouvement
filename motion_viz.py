import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Analyse de Mouvement : Différence d'Images")

st.title("🏃‍♂️ Analyse de Mouvement par Différence Temporelle")
st.markdown("""
Cette interface implémente la méthode décrite dans la section **3.1 Méthode par Différence d’Images**.
Elle compare l'image au temps $t$ avec l'image au temps $t-1$ pour isoler les pixels qui ont changé d'intensité.
""")

# --- 1. GESTION DE LA VIDÉO ---
st.sidebar.header("1. Source Vidéo")
video_file = st.sidebar.file_uploader("Importer une vidéo (MP4, AVI, MOV)", type=["mp4", "avi", "mov"])

# Fonction de chargement vidéo
@st.cache_resource
def load_video(video_file):
    # OpenCV a besoin d'un chemin de fichier physique, on crée un fichier temporaire
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    return tfile.name

if video_file is not None:
    temp_filename = load_video(video_file)
    cap = cv2.VideoCapture(temp_filename)
    
    # Récupérer les infos de la vidéo
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    st.sidebar.success(f"Vidéo chargée : {total_frames} frames, {width}x{height} px")
else:
    st.info("Veuillez charger une vidéo pour commencer. (Si vous n'en avez pas, téléchargez une courte vidéo de trafic routier ou de piétons).")
    st.stop() # Arrête le script ici tant qu'il n'y a pas de vidéo

# --- 2. CONTRÔLE TEMPOREL ---
st.sidebar.markdown("---")
st.sidebar.header("2. Navigation Temporelle")

# On commence à 1 car on a besoin de t-1
frame_index = st.slider("Sélectionner l'instant t (Frame)", 1, total_frames - 1, 10)

# Lecture des images t et t-1
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index - 1)
ret1, frame_prev_bgr = cap.read()
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
ret2, frame_curr_bgr = cap.read()

if not ret1 or not ret2:
    st.error("Erreur lors de la lecture des frames.")
    st.stop()

# Conversion en niveaux de gris (Nécessaire pour la soustraction simple)
frame_prev_gray = cv2.cvtColor(frame_prev_bgr, cv2.COLOR_BGR2GRAY)
frame_curr_gray = cv2.cvtColor(frame_curr_bgr, cv2.COLOR_BGR2GRAY)

# --- 3. TRAITEMENT (Le Cœur du TP) ---
st.sidebar.markdown("---")
st.sidebar.header("3. Paramètres de Détection")

# Paramètre Seuil (Threshold)
seuil = st.sidebar.slider("Seuil de détection (S)", 0, 255, 30, help="Si la différence > S, le pixel est considéré en mouvement.")

# 1. Calcul de la différence absolue (Section 3.1)
# Équivalent Python de : abs(Pixel(im2) - Pixel(im1))
diff_img = cv2.absdiff(frame_curr_gray, frame_prev_gray)

# 2. Seuillage (Section 3.2)
# Équivalent Python de : if (diff > SEUIL) pixel = 255 else pixel = 0
_, thresh_img = cv2.threshold(diff_img, seuil, 255, cv2.THRESH_BINARY)

# Option Bonus : Nettoyage Morphologique (pour contrer les limites observées en 3.3)
use_morphology = st.sidebar.checkbox("Activer le nettoyage de bruit (Bonus)", value=False)
if use_morphology:
    kernel = np.ones((3,3), np.uint8)
    # Ouverture : Érosion suivie de Dilatation (enlève les petits points blancs isolés)
    thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel)

# --- 4. VISUALISATION DÉTAILLÉE ---

st.subheader(f"Analyse à l'instant t = {frame_index}")

col1, col2 = st.columns(2)

with col1:
    st.caption("Frame précédente (t-1)")
    st.image(frame_prev_gray, use_container_width=True, clamp=True)

with col2:
    st.caption("Frame actuelle (t)")
    st.image(frame_curr_gray, use_container_width=True, clamp=True)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**1. Image de Différence Brute**")
    st.markdown(r"$D(x,y) = |I_t(x,y) - I_{t-1}(x,y)|$")
    # On utilise une colormap 'inferno' pour mieux voir les faibles variations (bruit)
    fig_diff, ax_diff = plt.subplots()
    im = ax_diff.imshow(diff_img, cmap='inferno')
    plt.colorbar(im, ax=ax_diff)
    ax_diff.axis('off')
    st.pyplot(fig_diff)
    st.warning("Notez comment les zones unies (intérieur des voitures) ont une différence faible (noir/violet), seules les bordures apparaissent clairement.")

with col4:
    st.markdown(f"**2. Masque Binaire (Seuil = {seuil})**")
    st.markdown("Résultat final après décision.")
    st.image(thresh_img, use_container_width=True, clamp=True)
    
    # Calcul du pourcentage de mouvement
    motion_pixels = np.count_nonzero(thresh_img)
    total_pixels = thresh_img.size
    ratio = (motion_pixels / total_pixels) * 100
    st.metric("Taux de mouvement dans l'image", f"{ratio:.2f}%")

# --- 5. ANALYSE CRITIQUE (Basée sur le texte) ---
st.markdown("---")
with st.expander("🔍 Analyse des limites (Basée sur Section 3.3 du rapport)"):
    st.markdown(f"""
    En observant l'image de différence brute ci-dessus, on constate les phénomènes décrits :
    
    1.  **Sensibilité au seuil :**
        * Essayez de baisser le seuil vers **5** : Vous verrez apparaître le "bruit
                 capteur" dans le fond statique.
        * Essayez de monter le seuil vers **100** : Les objets en mouvement s'effacent ou se morcellent.
    
    2.  **Problème des objets homogènes :**
        * Si une voiture blanche passe, l'intérieur de son capot est uniforme. $Pixel(t) \\approx Pixel(t-1)$.
        * Résultat : Le centre de la voiture est noir (pas de mouvement détecté), seuls les contours (phares, pare-brise) sont blancs. On appelle ça l'effet **"fantôme"** ou "aperture problem".
    """)

# --- 6. CODE RAW COMPARATIF ---
with st.expander("Voir la correspondance Code C vs Python"):
    st.code(f"""
    # CODE ORIGINAL (C)                # CODE PYTHON (Vectorisé)
    
    for y in range(H):                 # Opération matricielle immédiate :
        for x in range(W):             
            
            # Calcul différence          # 1. Différence Absolue
            diff = abs(im2 - im1)        diff = cv2.absdiff(img_t, img_t_minus_1)
            
            # Seuillage                  # 2. Seuillage binaire
            if diff > SEUIL:             _, res = cv2.threshold(diff, {seuil}, 255, cv2.THRESH_BINARY)
                res = 255
            else:
                res = 0
    """, language='python')