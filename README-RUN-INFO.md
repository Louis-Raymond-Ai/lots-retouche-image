# README-RUN-INFO.md - Guide Complet d'Utilisation

## 🚀 Comment Lancer le Projet

### 1. Installation et Préparation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Tester que tout fonctionne
python test_installation.py

# Vérifier les polices disponibles
python validate_fonts.py
```

### 2. Préparation des Images

```bash
# Placer vos images dans le dossier input/
# Formats supportés: JPG, JPEG, PNG, BMP, TIFF, WEBP
input/
├── image1.jpg
├── image2.png
└── image3.webp
```

---

## 📋 Toutes les Méthodes de Lancement

### Mode 1: Interface Interactive

```bash
python main.py
```

**Menu affiché :**
```
Available logos:
  1. X2
  2. X3
  3. X4
  ...
  19. X20

Select logo to apply (1-19) or 'q' to quit:
```

**Utilisation :**
- Tapez un numéro (1-19) pour traiter un logo spécifique
- Tapez `q` pour quitter

### Mode 2: Traiter TOUS les Logos (x2 à x20)

```bash
python main.py --levels x2-x20 --yes
```

**Résultat :** Crée 19 sous-dossiers avec tous les logos appliqués
```
output/
├── x2-lots/
├── x3-lots/
├── x4-lots/
...
└── x20-lots/
```

### Mode 3: Logo Spécifique

```bash
# Traiter seulement le logo x8
python main.py --logo x8 --yes

# Traiter seulement le logo x15
python main.py --logo x15 --yes
```

### Mode 4: Plage de Logos

```bash
# Traiter les logos de x5 à x12
python main.py --levels x5-x12 --yes

# Traiter les logos de x10 à x20
python main.py --levels x10-x20 --yes
```

### Mode 5: Logos Spécifiques (Liste)

```bash
# Traiter seulement x2, x8, x15, x20
python main.py --levels x2 x8 x15 x20 --yes

# Traiter x5, x10, x15
python main.py --levels x5 x10 x15 --yes
```

---

## ⚙️ Options Avancées

### Configuration des Marges

```bash
# Modifier les marges (en pixels)
python main.py --logo x8 --margin-right 30 --margin-top 25 --yes
```

### Qualité JPEG

```bash
# Qualité maximale (100)
python main.py --logo x8 --quality 100 --yes

# Qualité personnalisée
python main.py --logo x8 --quality 85 --yes
```

### Traitement Parallèle

```bash
# Utiliser 4 threads pour aller plus vite
python main.py --levels x2-x20 --workers 4 --yes

# Traitement séquentiel (1 thread)
python main.py --levels x2-x20 --workers 1 --yes
```

### Dossiers Personnalisés

```bash
# Dossiers d'entrée et sortie personnalisés
python main.py --logo x8 --input "C:/mes_images" --output "C:/resultats" --yes
```

---

## 📂 Organisation des Résultats

### Structure Automatique

Chaque logo crée son propre sous-dossier :

```
output/
├── x2-lots/
│   ├── image1_x2.jpg
│   ├── image2_x2.jpg
│   └── image3_x2.jpg
├── x8-lots/
│   ├── image1_x8.jpg
│   ├── image2_x8.jpg
│   └── image3_x8.jpg
└── x20-lots/
    ├── image1_x20.jpg
    ├── image2_x20.jpg
    └── image3_x20.jpg
```

### Noms des Fichiers

- **Format :** `nom_original_xN.jpg`
- **Exemple :** `produit123.png` → `produit123_x8.jpg`

---

## 🎯 Exemples Pratiques

### Exemple 1: Débutant - Un seul logo

```bash
# 1. Placez vos images dans input/
# 2. Lancez cette commande
python main.py --logo x8 --yes

# Résultat: Dossier x8-lots/ créé avec les images traitées
```

### Exemple 2: Professionnel - Tous les logos

```bash
# Traiter toutes les images avec tous les logos
python main.py --levels x2-x20 --workers 4 --yes

# Résultat: 19 dossiers créés (x2-lots à x20-lots)
```

### Exemple 3: E-commerce - Logos populaires

```bash
# Traiter seulement les tailles populaires
python main.py --levels x6 x8 x12 x15 --workers 2 --yes

# Résultat: 4 dossiers (x6-lots, x8-lots, x12-lots, x15-lots)
```

### Exemple 4: Personnalisé - Haute qualité

```bash
# Qualité maximale, marges personnalisées
python main.py --levels x8-x12 --quality 100 --margin-right 25 --margin-top 30 --yes
```

---

## 🔧 Configuration Avancée

### Fichier config.yaml

Modifiez `config.yaml` pour changer les paramètres par défaut :

```yaml
processing:
  margin_right: 21     # Marge droite en pixels
  margin_top: 22       # Marge haute en pixels
  jpeg_quality: 95     # Qualité JPEG (1-100)
  white_threshold: 250 # Seuil de détection blanc

directories:
  input: "input"       # Dossier d'entrée
  output: "output"     # Dossier de sortie
  logos: "logos"       # Dossier des logos
```

### Polices Personnalisées

```bash
# Utiliser une police spécifique
python main.py --logo x8 --font-path "fonts/arial.ttf" --yes

# Modifier l'espacement des lettres
python main.py --logo x8 --kerning -50 --yes
```

---

## 🚨 Dépannage

### Problème: "No images found"
```bash
# Vérifiez que vos images sont dans input/
ls input/

# Formats supportés: JPG, JPEG, PNG, BMP, TIFF, WEBP
```

### Problème: "Logo not found"
```bash
# Les logos sont auto-générés, pas de problème
# Si erreur persiste, vérifiez les polices:
python validate_fonts.py
```

### Problème: Qualité d'image
```bash
# Utilisez la qualité maximale
python main.py --logo x8 --quality 100 --full-quality --yes
```

### Problème: Traitement lent
```bash
# Augmentez le nombre de threads
python main.py --levels x2-x20 --workers 8 --yes
```

---

## 📊 Performances

### Temps de Traitement Estimés

| Images | Logos | Workers | Temps |
|--------|-------|---------|-------|
| 100    | 1     | 1       | ~2 min |
| 100    | 19    | 1       | ~30 min |
| 100    | 19    | 4       | ~8 min |
| 1000   | 19    | 8       | ~45 min |

### Optimisations

```bash
# Traitement ultra-rapide
python main.py --levels x2-x20 --workers 8 --quality 85 --yes

# Traitement haute qualité
python main.py --levels x2-x20 --workers 4 --quality 100 --full-quality --yes
```

---

## 📞 Support

Si vous rencontrez des problèmes :

1. **Vérifiez l'installation :** `python test_installation.py`
2. **Vérifiez les polices :** `python validate_fonts.py`  
3. **Testez avec une image :** `python main.py --logo x8 --yes`

**Commande de diagnostic complète :**
```bash
python main.py --logo x2 --input "input" --output "output" --quality 95 --workers 1 --yes
```