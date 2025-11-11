# AI_Video_Creator

Ce dépôt fournit deux ressources complémentaires pour créer du contenu visuel à partir de prompts IA :

1. **Une application CLI** capable de générer une image ou une courte vidéo (slideshow) en interrogeant un service d’illustration IA.
2. **Un storyboard lyrique** détaillant la mise en scène image par image de la chanson « Paparazzi Manqué ».

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

> 🆕 **Alternative automatique**
>
> Pour éviter les erreurs de chemin comme `requirements.txt introuvable`, lancez le script fourni (depuis la racine du projet) :
>
> ```bash
> ./scripts/setup_env.sh
> ```
>
> Il détecte la racine du projet, crée l’environnement `.venv` si besoin, puis installe les dépendances via `python3 -m pip`.

> 💡 **Besoin d’installer Python sur ChromeOS/Debian ?**
> 
> Si la commande `python3 -m venv` échoue (erreur « externally managed environment » ou `python: command not found`), installez
> les paquets système suivants puis relancez les commandes ci-dessus :
>
> ```bash
> sudo apt update
> sudo apt install python3 python3-venv python3-pip
> ```
>
> Ces paquets fournissent l’exécutable `python3`, la fonctionnalité de virtualenv (`python3-venv`) et `pip`. Une fois
> l’environnement virtuel activé, utilisez toujours `python3 -m pip` (ou `python -m pip` si `python` pointe bien vers Python 3)
> d’éviter les erreurs PEP 668 liées aux environnements gérés par le système.
>
> **Astuce Chromebook** : vérifiez que vous êtes bien dans le dossier du projet avant d’installer :
>
> ```bash
> cd ~/AI_Video_Creator
> ls requirements.txt
> ```
>
> Si la commande `ls` affiche bien `requirements.txt`, l’installation peut se faire sans erreur.

## Génération d’image ou de vidéo

L’application se lance via le module `app.cli` et contacte par défaut l’API publique de [pollinations.ai](https://pollinations.ai/) pour obtenir des illustrations.

### Générer une image

```bash
python3 -m app.cli --prompt "portrait manga blonde" --mode image --output media/result.jpg
```

### Générer une vidéo (slideshow)

```bash
python3 -m app.cli \
  --prompt "manga girl in neon city" \
  --mode video \
  --frame-count 8 \
  --fps 4 \
  --output media/result.mp4
```

Les vidéos sont construites à partir d’un ensemble d’images générées successivement puis assemblées avec `imageio`. Ajustez `--frame-count` et `--fps` pour contrôler la durée et le rythme.

> ℹ️ **Astuce** : vous pouvez remplacer l’API par un autre fournisseur en implémentant `ImageProvider` dans `app/services/providers.py`.

## Storyboard lyrique

- `storyboard.md` : description détaillée de chaque visuel (scène, texte, ambiance) à produire pour la chanson « Paparazzi Manqué ». Chaque image doit comporter une bulle manga manuscrite et un sous-titre simple en bas avec le même contenu.

Utilisez le storyboard comme guide artistique, puis servez-vous de l’application CLI pour prototyper rapidement des visuels ou un montage de base avant un travail de retouche avancée.

Bonne création !
