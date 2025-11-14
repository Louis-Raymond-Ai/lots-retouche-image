# Logo Processor - Batch Logo Application Tool

## Description

Application Python pour appliquer automatiquement des logos sur des images de produits en lot. Supporte les logos de x2 à x20 avec création automatique de sous-dossiers organisés.

## Fonctionnalités

- ✅ **Support complet** : Logos de x2 à x20 (19 logos différents)
- ✅ **Organisation automatique** : Création de sous-dossiers spécifiques (x2-lots, x3-lots, etc.)
- ✅ **Auto-génération** : Les logos manquants sont générés automatiquement
- ✅ **Traitement en lot** : Multiple logos et plages de logos
- ✅ **Interface flexible** : Mode interactif et ligne de commande
- ✅ **Optimisé** : Traitement parallèle et qualité JPEG configurable

## Installation Rapide

```bash
# 1. Installer Python 3.8+
# 2. Cloner/télécharger le projet
# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Tester l'installation
python test_installation.py
```

## Structure du Projet

```
logo_project_final/
├── main.py                 # Script principal
├── config.yaml             # Configuration
├── requirements.txt        # Dépendances Python
├── input/                  # Images à traiter
├── output/                 # Résultats organisés par logo
│   ├── x2-lots/
│   ├── x3-lots/
│   └── ... (x4-lots à x20-lots)
├── logos/                  # Logos (auto-générés si absents)
├── fonts/                  # Polices pour génération
└── src/                    # Code source modulaire
```

## Utilisation

Voir **README-RUN-INFO.md** pour toutes les commandes et exemples détaillés.

## Support

- Windows, macOS, Linux
- Python 3.8+
- Formats supportés : JPG, JPEG, PNG, BMP, TIFF, WEBP
