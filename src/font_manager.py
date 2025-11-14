"""
Dynamic Font Manager Module
Handles intelligent font loading with fallback system for logo generation
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple
from PIL import ImageFont


class DynamicFontManager:
    """Gestionnaire dynamique de polices avec fallback intelligent"""
    
    # Spécifications du logo x2 (basées sur l'analyse typographique)
    X2_SPECS = {
        'preferred_fonts': ['impact.ttf', 'Impact.ttf', 'IMPACT.TTF'],
        'fallback_fonts': [
            'arialbd.ttf', 'Arial-Bold.ttf', 'arial-black.ttf',
            'helvetica-black.ttf', 'Helvetica-Black.ttf',
            'anton.ttf', 'Anton-Regular.ttf',
            'futura-black.ttf', 'bebas-neue.ttf', 'Bebas-Neue.ttf',
            'montserrat-black.ttf', 'Montserrat-Black.ttf',
            'oswald-bold.ttf', 'Oswald-Bold.ttf'
        ],
        'width': 99,
        'height': 90,
        'kerning': -70,
        'color': (0, 0, 0, 255),  # Noir pur
        'dpi': (72, 72)
    }
    
    def __init__(self, local_fonts_dir: str = "fonts"):
        """
        Initialize the font manager
        
        Args:
            local_fonts_dir: Path to local fonts directory
        """
        self.local_fonts_dir = Path(local_fonts_dir)
        self.system_font_paths = self._get_system_font_paths()
        self.font_cache = {}
        
    def _get_system_font_paths(self) -> List[Path]:
        """Détecte automatiquement les chemins de polices système"""
        paths = []
        
        # Windows
        if sys.platform == 'win32':
            paths.append(Path('C:/Windows/Fonts'))
            
        # macOS
        elif sys.platform == 'darwin':
            paths.extend([
                Path('/Library/Fonts'),
                Path('/System/Library/Fonts'),
                Path.home() / 'Library/Fonts'
            ])
            
        # Linux
        else:
            paths.extend([
                Path('/usr/share/fonts'),
                Path('/usr/local/share/fonts'),
                Path.home() / '.fonts',
                Path('/usr/share/fonts/truetype'),
                Path('/usr/share/fonts/truetype/msttcorefonts')
            ])
            
        return [p for p in paths if p.exists()]
    
    def find_font(self, font_name: str, verbose: bool = False) -> Optional[Path]:
        """
        Recherche une police dans toutes les sources disponibles
        
        Args:
            font_name: Name of the font file to find
            verbose: Print search progress
            
        Returns:
            Path to font file if found, None otherwise
        """
        # 1. Dossier local (priorité maximale)
        local_path = self.local_fonts_dir / font_name
        if local_path.exists():
            if verbose:
                print(f"✓ Police trouvée (local): {local_path}")
            return local_path
            
        # 2. Polices système
        for sys_path in self.system_font_paths:
            font_path = sys_path / font_name
            if font_path.exists():
                if verbose:
                    print(f"✓ Police trouvée (système): {font_path}")
                return font_path
                
            # Recherche récursive dans les sous-dossiers (limité à 2 niveaux)
            try:
                for font_file in sys_path.glob(f'**/{font_name}'):
                    if font_file.is_file():
                        if verbose:
                            print(f"✓ Police trouvée (système): {font_file}")
                        return font_file
            except (PermissionError, OSError):
                # Ignorer les erreurs de permission
                continue
                    
        return None
    
    def get_best_font_for_x2(self, verbose: bool = True) -> Tuple[str, str]:
        """
        Retourne le meilleur chemin de police pour le logo x2
        
        Args:
            verbose: Print search progress
            
        Returns:
            Tuple of (font_path, quality_level)
            quality_level can be: 'preferred', 'fallback', or 'system_default'
            
        Raises:
            FileNotFoundError: If no suitable font is found
        """
        # Essayer les polices préférées (Impact)
        for font_name in self.X2_SPECS['preferred_fonts']:
            font_path = self.find_font(font_name, verbose=verbose)
            if font_path:
                if verbose:
                    print(f"✓ OPTIMAL: Police Impact détectée")
                return (str(font_path), 'preferred')
                
        # Essayer les polices de fallback
        for font_name in self.X2_SPECS['fallback_fonts']:
            font_path = self.find_font(font_name, verbose=False)
            if font_path:
                if verbose:
                    print(f"⚠ FALLBACK: Utilisation de {font_name}")
                    print(f"  Pour un rendu optimal, ajoutez impact.ttf dans le dossier 'fonts/'")
                return (str(font_path), 'fallback')
        
        # Dernier recours : chercher n'importe quelle police bold
        if verbose:
            print("⚠ Recherche d'une police bold système...")
        
        common_bold_fonts = ['arial.ttf', 'Arial.ttf', 'helvetica.ttf', 'Helvetica.ttf']
        for font_name in common_bold_fonts:
            font_path = self.find_font(font_name, verbose=False)
            if font_path:
                if verbose:
                    print(f"⚠ SYSTÈME: Utilisation de {font_name} (non optimal)")
                return (str(font_path), 'system_default')
                
        # Échec total
        raise FileNotFoundError(
            "\n❌ ERREUR: Aucune police compatible trouvée!\n\n"
            "SOLUTION:\n"
            "  1. Téléchargez Impact.ttf depuis https://www.fonts100.com/font+14752_Impact.html\n"
            "  2. Placez le fichier dans le dossier 'fonts/' du projet\n"
            "  3. Relancez le script\n\n"
            "Alternative: Installez Impact sur votre système (Windows: C:/Windows/Fonts/)"
        )
    
    def load_font(self, font_path: str, size: int) -> ImageFont.FreeTypeFont:
        """
        Charge une police avec mise en cache
        
        Args:
            font_path: Path to font file
            size: Font size in points
            
        Returns:
            Loaded font object
            
        Raises:
            RuntimeError: If font cannot be loaded
        """
        cache_key = (font_path, size)
        
        if cache_key not in self.font_cache:
            try:
                self.font_cache[cache_key] = ImageFont.truetype(font_path, size)
            except Exception as e:
                raise RuntimeError(f"Impossible de charger la police {font_path}: {e}")
                
        return self.font_cache[cache_key]
    
    def get_font_info(self, font_path: str) -> dict:
        """
        Get information about a font file
        
        Args:
            font_path: Path to font file
            
        Returns:
            Dictionary with font information
        """
        font_path_obj = Path(font_path)
        return {
            'name': font_path_obj.name,
            'path': str(font_path_obj),
            'exists': font_path_obj.exists(),
            'size_kb': font_path_obj.stat().st_size // 1024 if font_path_obj.exists() else 0
        }
