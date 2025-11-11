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
sudo apt install git python3 python3-venv python3-pip ffmpeg
```

- `python3` fournit l'interpréteur utilisé partout dans ce projet.
- `python3-venv` permet de créer l'environnement virtuel.
- `python3-pip` installe `pip` rattaché à Python 3.
- `ffmpeg` est requis par `imageio` pour l'export vidéo.

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
python3 -m pip install -r requirements.txt
```

> 💡 Si vous préférez automatiser ces étapes, exécutez `./scripts/setup_env.sh`. Ce script détecte `python3`, crée `.venv` et installe les dépendances en utilisant toujours `python3 -m pip`.

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
  --output media/result.mp4
```

Les fichiers générés sont sauvegardés dans le dossier `media/` (à créer si nécessaire).

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
- **Erreurs réseau lors de la génération** : pollinations.ai est un service public ; relancez la commande ou réessayez plus tard.

En suivant ce guide, le projet est opérationnel sur Chromebook avec des commandes `python3` explicites à chaque étape.
