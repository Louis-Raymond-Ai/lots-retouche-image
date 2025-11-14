"""
Configuration Loader Module
Loads and validates configuration from YAML file
"""

import yaml
import os
from typing import Dict, Any


class ConfigLoader:
    """Loads and manages configuration settings"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize configuration loader
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file
        
        Returns:
            Dictionary containing configuration
        """
        if not os.path.exists(self.config_path):
            print(f"Warning: Config file not found: {self.config_path}")
            print("Using default configuration")
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(f"Configuration loaded from: {self.config_path}")
            return config
        except Exception as e:
            print(f"Error loading config file: {e}")
            print("Using default configuration")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration
        
        Returns:
            Dictionary with default settings
        """
        return {
            'margins': {
                'right': 21,
                'top': 22
            },
            'directories': {
                'input': 'input',
                'output': 'output',
                'logos': 'logos'
            },
            'logos': {
                'x6': 'logos/logo_x6.png',
                'x8': 'logos/logo_x8.png',
                'x12': 'logos/logo_x12.png'
            },
            'logo_dimensions': {
                'x6': [93, 97],
                'x8': [93, 97],
                'x12': [106, 103]
            },
            'processing': {
                'jpeg_quality': 95,
                'white_threshold': 250,
                'logo_padding': 3
            },
            'output': {
                'format': 'JPEG',
                'suffix_x6': '_x6',
                'suffix_x8': '_x8',
                'suffix_x12': '_x12',
                'preserve_original': True
            },
            'advanced': {
                'verbose': True,
                'save_intermediate': False,
                'batch_size': 10
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Path to config value (e.g., 'margins.right')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_margin_right(self) -> int:
        """Get right margin value"""
        return self.get('margins.right', 21)
    
    def get_margin_top(self) -> int:
        """Get top margin value"""
        return self.get('margins.top', 22)
    
    def get_input_dir(self) -> str:
        """Get input directory"""
        return self.get('directories.input', 'input')
    
    def get_output_dir(self) -> str:
        """Get output directory"""
        return self.get('directories.output', 'output')
    
    def get_logos_dir(self) -> str:
        """Get logos directory"""
        return self.get('directories.logos', 'logos')
    
    def get_logo_path(self, logo_type: str) -> str:
        """
        Get path to logo file
        
        Args:
            logo_type: Type of logo ('x6', 'x8', 'x12')
            
        Returns:
            Path to logo file
        """
        return self.get(f'logos.{logo_type}', f'logos/logo_{logo_type}.png')
    
    def get_logo_suffix(self, logo_type: str) -> str:
        """
        Get output suffix for logo type
        
        Args:
            logo_type: Type of logo ('x6', 'x8', 'x12')
            
        Returns:
            Suffix string
        """
        return self.get(f'output.suffix_{logo_type}', f'_{logo_type}')
    
    def get_jpeg_quality(self) -> int:
        """Get JPEG quality setting"""
        return self.get('processing.jpeg_quality', 95)
    
    def get_white_threshold(self) -> int:
        """Get white threshold for logo detection"""
        return self.get('processing.white_threshold', 250)
    
    def get_logo_padding(self) -> int:
        """Get logo padding"""
        return self.get('processing.logo_padding', 3)
    
    def is_verbose(self) -> bool:
        """Check if verbose mode is enabled"""
        return self.get('advanced.verbose', True)
    
    def print_config(self):
        """Print current configuration"""
        print("\n" + "="*60)
        print("CURRENT CONFIGURATION")
        print("="*60)
        print(f"Margins: Right={self.get_margin_right()}px, Top={self.get_margin_top()}px")
        print(f"Input directory: {self.get_input_dir()}")
        print(f"Output directory: {self.get_output_dir()}")
        print(f"Logos directory: {self.get_logos_dir()}")
        print(f"JPEG quality: {self.get_jpeg_quality()}")
        print(f"White threshold: {self.get_white_threshold()}")
        print("="*60 + "\n")
