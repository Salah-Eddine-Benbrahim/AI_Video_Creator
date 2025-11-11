# AI_Video_Creator

Ce dépôt fournit deux ressources complémentaires pour créer du contenu visuel à partir de prompts IA :

1. **Une application CLI** capable de générer une image ou une courte vidéo (slideshow) en interrogeant un service d’illustration IA.
2. **Un storyboard lyrique** détaillant la mise en scène image par image de la chanson « Paparazzi Manqué ».

> ℹ️ L’application repose uniquement sur la bibliothèque standard de Python 3. Aucun paquet additionnel n’est requis par défaut et le mode vidéo produit un fichier MJPEG (`.avi`) compatible avec la plupart des lecteurs.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt  # (facultatif : le fichier est vide)
```

> 🆕 **Alternative automatique**
>
> Pour éviter les erreurs de chemin, lancez le script fourni (depuis la racine du projet) :
>
> ```bash
> ./scripts/setup_env.sh
> ```
>
> Il détecte la racine du projet, crée l’environnement `.venv` si besoin, puis exécute `python3 -m pip install -r requirements.txt` (ce qui ne fait rien quand le fichier est vide, mais garantit la compatibilité si des dépendances sont ajoutées plus tard).

### Nettoyer ou repartir de zéro

Pour supprimer un environnement virtuel endommagé ou repartir d’une installation propre :

```bash
./scripts/clean_env.sh
```

Le script efface le dossier `.venv` et les répertoires `__pycache__`. Ajoutez l’option `--purge-media` pour supprimer en plus les fichiers générés dans `media/`.

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
>
> 🔁 **Invite de commande avec `AI_Video_Creator/AI_Video_Creator` ?**
>
> Si votre terminal affiche `~/AI_Video_Creator/AI_Video_Creator$`, vous êtes dans un dossier dupliqué créé lors du clonage ou de la copie du projet. Revenez à la racine unique avec :
>
> ```bash
> cd ~/AI_Video_Creator
> ```
>
> Si un sous-dossier `AI_Video_Creator` vide demeure à l’intérieur de la racine, vous pouvez le supprimer pour éviter toute confusion :
>
> ```bash
> rm -rf AI_Video_Creator
> ```
>
> 📘 **Besoin d’un tutoriel détaillé Chromebook ?** Consultez [docs/chromebook.md](docs/chromebook.md) pour un guide pas-à-pas
> incluant l’activation de Linux, les commandes `python3` exactes et la copie des médias vers ChromeOS.

## Génération d’image ou de vidéo

L’application se lance via le module `app.cli` et contacte par défaut l’API publique de [pollinations.ai](https://pollinations.ai/) pour obtenir des illustrations. En cas d’indisponibilité réseau (proxy, absence de connexion…), le programme bascule automatiquement sur une illustration de secours intégrée au projet afin de terminer la génération sans erreur.

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
  --output media/result.avi
```

Les vidéos sont construites à partir d’un ensemble d’images générées successivement puis assemblées dans un conteneur MJPEG (`.avi`). Ajustez `--frame-count` et `--fps` pour contrôler la durée et le rythme.

> ✅ **Astuce compatibilité :** conservez l’extension `.avi` pour éviter toute confusion lors de la lecture du fichier par les lecteurs multimédias.

> ℹ️ **Astuce** : vous pouvez remplacer l’API par un autre fournisseur en implémentant `ImageProvider` dans `app/services/providers.py`.

## Vérifier l’installation

Une fois l’environnement configuré, vous pouvez vérifier rapidement que les modules Python se compilent correctement :

```bash
python3 -m compileall app
```

> ❗ **Ne copiez pas les emojis dans le terminal.**
> Dans certains guides ou messages, la commande précédente peut être illustrée par un emoji (ex. `✅ python3 -m compileall app`) pour signaler qu’un test a réussi. Saisissez uniquement la commande sans l’emoji, sinon Bash tentera d’exécuter le symbole `✅` comme un programme et affichera `command not found`.

> 🚀 **Envie d’un raccourci sans risque d’emoji ?**
>
> Utilisez le script fourni qui active automatiquement `.venv` si présent puis lance la vérification :
>
> ```bash
> ./scripts/run_compile_check.sh
> ```
>
> Cette commande équivaut à `python3 -m compileall app`, mais évite toute faute de frappe ou copie involontaire de caractères spéciaux.

## Mettre à jour votre copie locale

Si vous ne voyez pas le dossier suivi `media/` (ou les autres fichiers récents) dans votre clone ou sur l’interface GitHub, assu
rez-vous d’être sur la bonne branche et d’avoir récupéré les derniers commits :

```bash
git fetch origin
git checkout codex/create-lyric-images-with-manga-style
git pull --ff-only
```

Ensuite, vérifiez la présence du dossier suivi :

```bash
ls media
```

Le dépôt contient uniquement `README.md` pour garder le dossier visible. Générez vos propres exemples (`sample.avi`, etc.) en local via la CLI décrite ci-dessus. Si GitHub n’affiche toujours pas `media/`, vérifiez que vous consultez bien la branche `codex/create-lyric-images-with-manga-style` dans l’interface web (menu déroulant « Branch » en haut à gauche).

## Vérifier les fichiers suivis sur GitHub

Si certains dossiers (par exemple `app/` ou `media/`) n’apparaissent pas lorsque vous parcourez le dépôt en ligne :

1. Confirmez que vous êtes bien à la racine du dépôt sur GitHub : l’URL doit se terminer par `/tree/codex/create-lyric-images-with-manga-style/` sans dossier supplémentaire.
2. Exécutez localement `./scripts/list_tracked_files.sh` pour afficher tous les chemins suivis par Git. Tout élément présent dans la sortie devrait être visible sur GitHub au même emplacement.
3. Si vous voyez un chemin dupliqué du type `AI_Video_Creator/AI_Video_Creator/...`, remontez d’un niveau via le fil d’Ariane GitHub ou supprimez le dossier redondant dans votre copie locale comme indiqué plus haut.
4. Terminez par `git pull --ff-only` pour récupérer les derniers commits si besoin.

> Astuce : la sortie de `list_tracked_files.sh` est indépendante de votre système d’exploitation. Elle constitue une référence rapide pour vérifier ce qui doit apparaître dans la vue GitHub.

## Storyboard lyrique

- `storyboard.md` : description détaillée de chaque visuel (scène, texte, ambiance) à produire pour la chanson « Paparazzi Manqué ». Chaque image doit comporter une bulle manga manuscrite et un sous-titre simple en bas avec le même contenu.

Utilisez le storyboard comme guide artistique, puis servez-vous de l’application CLI pour prototyper rapidement des visuels ou un montage de base avant un travail de retouche avancée.

Bonne création !
