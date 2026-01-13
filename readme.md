# Analyse de Mouvement par Différence Temporelle

Ce projet est une application interactive développée avec **Streamlit** pour illustrer la méthode de détection de mouvement par **différence d'images (Frame Difference)**.

Cette technique consiste à comparer l'image à un instant $t$ avec l'image à l'instant précédent $t-1$. Si la différence d'intensité d'un pixel dépasse un certain seuil, ce pixel est considéré comme étant en mouvement.

## 🚀 Fonctionnalités

*   **Importation de vidéo** : Support des formats MP4, AVI et MOV.
*   **Navigation temporelle** : Possibilité de choisir précisément l'instant $t$ à analyser via un slider.
*   **Visualisation étape par étape** :
    *   Affichage des frames $t$ et $t-1$.
    *   Affichage de la **différence brute** (carte de chaleur pour visualiser les faibles variations).
    *   Affichage du **masque binaire** final après seuillage.
*   **Paramètres ajustables** :
    *   **Seuil de détection** : Permet de filtrer le bruit ou d'affiner la détection.
    *   **Nettoyage morphologique** (Bonus) : Option pour réduire le bruit via des opérations d'ouverture.
*   **Analyse critique** : Explications intégrées sur les limites de la méthode (bruit capteur, objets homogènes/effet fantôme).

## 🛠️ Installation

1.  **Prérequis** : Assurez-vous d'avoir Python installé sur votre machine.

2.  **Cloner ou télécharger ce dépôt**.

3.  **Installer les dépendances** :
    Il est recommandé d'utiliser un environnement virtuel.
    ```bash
    pip install -r requirement.txt
    ```

    Les bibliothèques principales sont :
    *   `streamlit` : Pour l'interface web.
    *   `opencv-python` : Pour le traitement d'images.
    *   `numpy` : Pour les calculs matriciels.
    *   `matplotlib` : Pour la visualisation avancée (colormaps).

## ▶️ Utilisation

Pour lancer l'application, exécutez la commande suivante dans votre terminal :

```bash
streamlit run motion_viz.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut (généralement à l'adresse `http://localhost:8501`).

1.  Chargez une vidéo via la barre latérale ("1. Source Vidéo").
2.  Naviguez dans la vidéo avec le slider ("2. Navigation Temporelle").
3.  Ajustez le seuil de détection pour observer l'impact sur le masque binaire.

## 📂 Structure du projet

*   `motion_viz.py` : Le script principal de l'application Streamlit.
*   `requirement.txt` : Liste des dépendances Python.
*   `readme.md` : Ce fichier de documentation.

<!-- thyzm-title: Python Motion-->
<!-- thyzm-description: Programme d'analyse de mouvement. -->
<!-- thyzm-image: https://mon-site.com/image-cover.png -->
<!-- thyzm-tech: Python, streamlit, OpenCV -->
<!-- thyzm-type: IOT -->
<!-- thyzm-status: IN_PROGRESS -->
<!-- thyzm-live: https://mon-demo-live.com -->