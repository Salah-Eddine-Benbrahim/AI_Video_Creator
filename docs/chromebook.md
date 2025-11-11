# Guide d'installation sur Chromebook

Ce guide décrit comment préparer un Chromebook (ChromeOS) pour exécuter l'application CLI du projet **AI_Video_Creator**. Les commandes utilisent explicitement `python3` afin d'éviter les erreurs « command not found ».

## 1. Activer l'environnement Linux
1. Ouvrez **Paramètres → Avancé → Développeurs → Linux (Beta)**.
2. Cliquez sur **Activer** puis suivez l'assistant pour créer le conteneur Debian.
3. Une fois l'installation terminée, une application **Terminal** s'ouvre automatiquement.

## 2. Mettre à jour le conteneur
Dans le terminal Linux :

```bash
sudo apt update
sudo apt upgrade
```

## 3. Installer les dépendances système
Toujours dans le terminal :

```bash
sudo apt install git python3 python3-venv python3-pip
```

- `python3` fournit l'interpréteur utilisé partout dans ce projet.
- `python3-venv` permet de créer l'environnement virtuel.
- `python3-pip` installe `pip` rattaché à Python 3.

> ℹ️ **Optionnel :** installez également `ffmpeg` (`sudo apt install ffmpeg`) si vous préférez utiliser le binaire système au lieu
> de laisser l'outil télécharger une version portable automatiquement.

Vérifiez ensuite que la commande est disponible :

```bash
python3 --version
which python3
```

## 4. Récupérer le projet
Clonez le dépôt dans votre répertoire utilisateur :

```bash
git clone https://github.com/<votre-compte>/AI_Video_Creator.git
cd AI_Video_Creator
```

Assurez-vous que le fichier `requirements.txt` est présent :

```bash
ls requirements.txt
```

Si vous ne voyez pas certains fichiers récents (par exemple le dossier suivi `media/`), récupérez la dernière version de la bra
nche de travail :

```bash
git fetch origin
git checkout codex/create-lyric-images-with-manga-style
git pull --ff-only
ls media
```

Sur GitHub, vérifiez également que vous consultez la même branche (`codex/create-lyric-images-with-manga-style`) via le menu « B
ranch ».

> 🔁 **Invite de commande affichant `AI_Video_Creator/AI_Video_Creator` ?**
>
> Vous êtes probablement entré dans un dossier dupliqué (par exemple après avoir extrait une archive). Revenez à la racine du projet avec :
>
> ```bash
> cd ~/AI_Video_Creator
> ```
>
> Si un sous-dossier `AI_Video_Creator` superflu reste à l’intérieur et qu’il ne contient rien de nécessaire, vous pouvez le supprimer pour éviter la confusion :
>
> ```bash
> rm -rf AI_Video_Creator
> ```
>
> La racine correcte doit contenir `README.md`, `app/`, `docs/`, `scripts/`, etc.

## 5. Créer et activer l'environnement virtuel
Depuis la racine du projet :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

L'invite du terminal affiche maintenant le préfixe `(.venv)`.

## 6. Installer les dépendances Python
Utilisez l'interpréteur de l'environnement pour piloter `pip` :

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt  # (facultatif : fichier vide par défaut)
```

> 💡 Si vous préférez automatiser ces étapes, exécutez `./scripts/setup_env.sh`. Ce script détecte `python3`, crée `.venv` et exécute `python3 -m pip install -r requirements.txt` pour conserver la compatibilité si des dépendances sont ajoutées ultérieurement.

## 7. Générer une image ou une vidéo
a. **Image unique** :

```bash
python3 -m app.cli --prompt "portrait manga blonde" --mode image --output media/result.jpg
```

b. **Slideshow vidéo** :

```bash
python3 -m app.cli \
  --prompt "manga girl in neon city" \
  --mode video \
  --frame-count 8 \
  --fps 4 \
  --output media/result.avi
```

Les fichiers générés sont sauvegardés dans le dossier `media/` (à créer si nécessaire). Le mode vidéo produit un conteneur MJPEG (`.avi`) lisible par la majorité des lecteurs.

## 8. Exporter les médias vers ChromeOS
Pour copier le résultat dans le stockage partagé ChromeOS :

```bash
cp media/result.jpg /mnt/chromeos/MyFiles/Downloads/
```

Remplacez `result.jpg` par le nom du fichier souhaité.

## Dépannage
- **`python3: command not found`** : vérifiez l'étape d'installation (`sudo apt install python3 ...`).
- **Erreur « externally managed environment »** : assurez-vous d'exécuter `python3 -m pip` depuis l'environnement virtuel activé.
- **`requirements.txt introuvable`** : confirmez que vous êtes bien dans la racine du projet (`pwd` doit se terminer par `AI_Video_Creator`).
- **Erreurs réseau lors de la génération** : si l’accès à pollinations.ai est bloqué (proxy, mode avion…), la CLI affiche un
  avertissement et insère automatiquement un visuel de secours intégré au projet pour finaliser l’image ou la vidéo.
- **Repartir sur une base propre** : exécutez `./scripts/clean_env.sh` pour supprimer `.venv` et les caches Python. Ajoutez `--purge-media` si vous souhaitez effacer les visuels générés dans `media/` avant de relancer `./scripts/setup_env.sh`.
- **Vérifier rapidement l’installation** : lancez `./scripts/run_compile_check.sh`. Le script active `.venv` si besoin et exécute `python3 -m compileall app` sans que vous ayez à saisir la commande manuellement.
- **Comparer avec la vue GitHub** : `./scripts/list_tracked_files.sh` affiche la liste complète des fichiers suivis par Git. Utilisez-la pour confirmer quels répertoires devraient apparaître en ligne lorsque certains dossiers semblent manquants.
- **Commande précédée d’un emoji (`✅ python3 ...`)** : tapez la commande sans l’emoji. Les emojis servent uniquement à indiquer la réussite d’un test dans la documentation ; s’ils sont copiés tels quels dans le terminal, Bash tentera de les exécuter et renverra `command not found`.

En suivant ce guide, le projet est opérationnel sur Chromebook avec des commandes `python3` explicites à chaque étape.
