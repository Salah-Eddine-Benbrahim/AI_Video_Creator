# AI_Video_Creator

Ce dépôt fournit deux ressources complémentaires pour créer du contenu visuel à partir de prompts IA :

1. **Une application CLI** capable de générer une image ou une courte vidéo (slideshow) en interrogeant un service d’illustration IA.
2. **Un storyboard lyrique** détaillant la mise en scène image par image de la chanson « Paparazzi Manqué ».

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Génération d’image ou de vidéo

L’application se lance via le module `app.cli` et contacte par défaut l’API publique de [pollinations.ai](https://pollinations.ai/) pour obtenir des illustrations.

### Générer une image

```bash
python -m app.cli --prompt "portrait manga blonde" --mode image --output media/result.jpg
```

### Générer une vidéo (slideshow)

```bash
python -m app.cli \
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
