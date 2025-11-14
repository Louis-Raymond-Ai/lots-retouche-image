#!/usr/bin/env python
"""
Script de validation des polices pour le logo x2
Vérifie la disponibilité et la qualité des polices
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from font_manager import DynamicFontManager
from logo_processor import LogoProcessor


def validate_fonts():
    """Valide toutes les polices disponibles"""
    print("\n" + "="*70)
    print(" "*20 + "VALIDATION DES POLICES")
    print("="*70 + "\n")
    
    # Initialiser le gestionnaire
    manager = DynamicFontManager(local_fonts_dir="fonts")
    
    # Recherche de la meilleure police
    try:
        font_path, quality = manager.get_best_font_for_x2(verbose=True)
        
        print(f"\n{'='*70}")
        print(f"RÉSULTAT:")
        print(f"  Police sélectionnée: {font_path}")
        print(f"  Niveau de qualité: {quality.upper()}")
        
        if quality == 'preferred':
            print(f"  ✓ OPTIMAL - Impact détecté (conforme aux spécifications)")
        elif quality == 'fallback':
            print(f"  ⚠ ACCEPTABLE - Police de fallback (rendu légèrement différent)")
        else:
            print(f"  ⚠ SYSTÈME - Police système (rendu non optimal)")
            
        print(f"{'='*70}\n")
        
        # Générer un aperçu du logo x2
        print("Génération d'un aperçu du logo x2...")
        test_logo_path = "fonts/test_x2_preview.png"
        
        processor = LogoProcessor()
        processor.generate_heavy_logo(
            text="x2",
            output_path=test_logo_path,
            target_size=(99, 90),
            kerning=-70,
            font_path=font_path
        )
        
        print(f"\n✓ Aperçu généré: {test_logo_path}")
        print(f"  Ouvrez ce fichier pour vérifier la qualité du rendu")
        print(f"  Dimensions attendues: 99×90 pixels")
        print(f"  Kerning: -70 (très serré)")
        
        # Afficher les informations de la police
        font_info = manager.get_font_info(font_path)
        print(f"\nInformations de la police:")
        print(f"  Nom: {font_info['name']}")
        print(f"  Chemin: {font_info['path']}")
        print(f"  Taille: {font_info['size_kb']} KB")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERREUR: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERREUR INATTENDUE: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    print("\n" + "="*70)
    print("✓ Validation terminée avec succès!")
    print("="*70 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(validate_fonts())
