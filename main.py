#!/usr/bin/env python
"""
Logo Processor - Main Script
Apply logos (x6, x8, x12) to product images in batch
"""

import os
import sys
from pathlib import Path
import argparse

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from logo_processor import LogoProcessor
from config_loader import ConfigLoader


def print_banner():
    """Print application banner"""
    print("\n" + "="*70)
    print(" "*20 + "LOGO PROCESSOR v1.0")
    print(" "*15 + "Batch Logo Application Tool")
    print("="*70 + "\n")


def check_directories(config: ConfigLoader):
    """
    Check and create necessary directories
    
    Args:
        config: Configuration loader instance
    """
    input_dir = config.get_input_dir()
    output_dir = config.get_output_dir()
    logos_dir = config.get_logos_dir()
    
    # Create directories if they don't exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(logos_dir, exist_ok=True)
    
    print(f"✓ Directories checked:")
    print(f"  Input:  {os.path.abspath(input_dir)}")
    print(f"  Output: {os.path.abspath(output_dir)}")
    print(f"  Logos:  {os.path.abspath(logos_dir)}")
    print()


def check_logos(config: ConfigLoader) -> dict:
    """
    Check which logos are available
    
    Args:
        config: Configuration loader instance
        
    Returns:
        Dictionary of available logos
    """
    available_logos = {}
    
    for logo_type in ['x6', 'x8', 'x12']:
        logo_path = config.get_logo_path(logo_type)
        if os.path.exists(logo_path):
            available_logos[logo_type] = logo_path
            print(f"✓ Logo {logo_type.upper()} found: {logo_path}")
        else:
            print(f"✗ Logo {logo_type.upper()} not found: {logo_path}")
    
    print()
    return available_logos


def select_logo(available_logos: dict) -> tuple:
    """
    Let user select which logo to apply
    
    Args:
        available_logos: Dictionary of available logos
        
    Returns:
        Tuple of (logo_type, logo_path) or (None, None) if cancelled
    """
    if not available_logos:
        print("ERROR: No logos found! Please add logo files to the 'logos' folder.")
        return (None, None)
    
    print("Available logos:")
    logo_list = list(available_logos.keys())
    for i, logo_type in enumerate(logo_list, 1):
        print(f"  {i}. {logo_type.upper()}")
    
    while True:
        try:
            choice = input(f"\nSelect logo to apply (1-{len(logo_list)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                return (None, None)
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(logo_list):
                logo_type = logo_list[choice_num - 1]
                return (logo_type, available_logos[logo_type])
            else:
                print(f"Please enter a number between 1 and {len(logo_list)}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return (None, None)


def count_images(input_dir: str) -> int:
    """
    Count number of images in input directory
    
    Args:
        input_dir: Path to input directory
        
    Returns:
        Number of image files found
    """
    extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    count = 0
    for ext in extensions:
        count += len(list(Path(input_dir).glob(f'*{ext}')))
    return count


def main():
    """Main application function (supports CLI arguments)"""
    parser = argparse.ArgumentParser(description="Batch apply a logo to product images.")
    # Allow dynamic logos from x2 to x20
    parser.add_argument('--logo', '--lots', dest='logo', help='Logo type to apply (x2..x20). Generated automatically if file missing.')
    parser.add_argument('--margin-right','-r', dest='margin_right', type=int, help='Override right margin (pixels)')
    parser.add_argument('--margin-top','-t', dest='margin_top', type=int, help='Override top margin (pixels)')
    parser.add_argument('--input','-i', dest='input_dir', help='Override input directory path')
    parser.add_argument('--output','-o', dest='output_dir', help='Override output directory path')
    parser.add_argument('--quality','-q', dest='jpeg_quality', type=int, help='JPEG quality (1-100)')
    parser.add_argument('--white-threshold', dest='white_threshold', type=int, help='White detection threshold (0-255)')
    parser.add_argument('--extensions', '-e', nargs='*', help='Image extensions to process, e.g. --extensions .jpg .png .webp')
    parser.add_argument('--workers','-w', type=int, default=1, help='Number of threads for parallel processing')
    parser.add_argument('--yes','-y', action='store_true', help='Run non-interactively (skip confirmations)')
    parser.add_argument('--full-quality', action='store_true', help='Force JPEG quality=100 (no subsampling, no optimization)')
    parser.add_argument('--levels', nargs='+', help='Process multiple logo levels (e.g. x2 x4 x6 or range x2-x10); overrides --logo and interactive mode')
    parser.add_argument('--font-path', type=str, help='Chemin vers la police à utiliser pour le logo (ex: fonts/impact.ttf ou C:/Windows/Fonts/impact.ttf)')
    parser.add_argument('--kerning', type=int, default=-70, help='Kerning (espacement horizontal) entre les caractères du logo, valeur négative pour compacter')
    args = parser.parse_args()

    print_banner()
    
    # Load configuration
    config = ConfigLoader('config.yaml')
    config.print_config()
    
    # Apply CLI overrides before directory checks
    if args.input_dir:
        config.config['directories']['input'] = args.input_dir
    if args.output_dir:
        config.config['directories']['output'] = args.output_dir

    # Check directories
    check_directories(config)
    
    # Check for images in input folder
    input_dir = config.get_input_dir()
    image_count = count_images(input_dir)
    
    if image_count == 0:
        print(f"ERROR: No images found in '{input_dir}' folder!")
        print(f"Please add images to process in: {os.path.abspath(input_dir)}")
        input("\nPress Enter to exit...")
        return
    
    print(f"✓ Found {image_count} image(s) to process\n")
    
    # Check available logos (legacy predefined x6/x8/x12)
    available_logos = check_logos(config)

    # Parse levels list if provided
    levels_list = []
    if args.levels:
        for token in args.levels:
            token = token.strip()
            if '-' in token:
                start, end = token.split('-',1)
                start = start.strip().lower(); end = end.strip().lower()
                if start.startswith('x') and end.startswith('x') and start[1:].isdigit() and end[1:].isdigit():
                    s = int(start[1:]); e = int(end[1:])
                    if 2 <= s <= 20 and 2 <= e <= 20 and s <= e:
                        for n in range(s, e+1):
                            levels_list.append(f'x{n}')
                    else:
                        print(f"Ignored invalid range: {token}")
                else:
                    print(f"Ignored invalid range: {token}")
            else:
                low = token.lower()
                if low.startswith('x') and low[1:].isdigit():
                    num = int(low[1:])
                    if 2 <= num <= 20:
                        levels_list.append(low)
                    else:
                        print(f"Ignored out-of-range level: {token}")
                else:
                    print(f"Ignored invalid level token: {token}")
        # Deduplicate preserving order
        seen = set(); ordered = []
        for lv in levels_list:
            if lv not in seen:
                seen.add(lv); ordered.append(lv)
        levels_list = ordered

    if args.logo and not levels_list:
        logo_type = args.logo.lower()
        # Validate pattern xN
        if logo_type.startswith('x') and logo_type[1:].isdigit():
            n_val = int(logo_type[1:])
            if 2 <= n_val <= 20:
                # If file exists use it; else auto-generate
                requested_path = config.get_logo_path(logo_type)
                if os.path.exists(requested_path):
                    logo_path = requested_path
                    print(f"Using existing logo file: {logo_path}")
                else:
                    # Auto-generate in logos directory
                    logos_dir = config.get_logos_dir()
                    os.makedirs(logos_dir, exist_ok=True)
                    logo_path = os.path.join(logos_dir, f"logo_{logo_type}.png")
                    from logo_processor import LogoProcessor as _LP
                    _LP().generate_text_logo(logo_type, logo_path)
                    print(f"Auto-generated logo: {logo_path}")
            else:
                print("ERROR: Numeric part must be between 2 and 20.")
                sys.exit(1)
        else:
            print("ERROR: --logo value must match pattern xN (e.g., x6, x12).")
            sys.exit(1)
    else:
        # Interactive fallback
        if not available_logos:
            print("\nAucun logo trouvé dans le dossier 'logos'. Ajoutez au moins un logo (logo_x6.png, logo_x8.png, logo_x12.png) pour continuer.")
            input("\nAppuyez sur Entrée pour quitter...")
            return
        logo_type, logo_path = select_logo(available_logos)
        if logo_type is None:
            print("\nOpération annulée.")
            return

    # Suffixe de sortie pour mode mono-logo
    suffix = config.get_logo_suffix(logo_type) if not levels_list else None

    # Extensions supportées (tous types d'images courants) ou celles données en CLI
    extensions = args.extensions if args.extensions else ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.JPG', '.JPEG', '.PNG', '.BMP', '.TIFF', '.WEBP']

    # Confirmation
    print(f"\n{'='*70}")
    print(f"Prêt à traiter {image_count} image(s)")
    if levels_list:
        print(f"  Logos multiples: {', '.join(levels_list)} (auto-génération si absents)")
    else:
        print(f"  Logo: {logo_type.upper()} ({logo_path})")
        print(f"  Suffixe: {suffix}")
    print(f"  Dossier d'entrée: {os.path.abspath(input_dir)}")
    print(f"  Dossier de sortie: {os.path.abspath(config.get_output_dir())}")
    print(f"{'='*70}\n")

    if not args.yes:
        confirm = input("Continuer le traitement ? (o/n): ").strip().lower()
        if confirm != 'o':
            print("\nOpération annulée.")
            return
    else:
        print("Mode non interactif: confirmation automatique.")

    # Initialisation du processor
    # Override margins & quality via CLI if provided
    margin_right = args.margin_right if args.margin_right is not None else config.get_margin_right()
    margin_top = args.margin_top if args.margin_top is not None else config.get_margin_top()
    jpeg_quality = args.jpeg_quality if args.jpeg_quality is not None else config.get_jpeg_quality()
    white_threshold = args.white_threshold if args.white_threshold is not None else config.get_white_threshold()

    # Si --font-path n'est pas fourni, cherche fonts/impact.ttf dans le projet
    font_path = args.font_path
    if not font_path:
        local_fonts = [
            os.path.join(os.path.dirname(__file__), 'fonts', 'impact.ttf'),
            os.path.join(os.path.dirname(__file__), 'fonts', 'anton.ttf'),
            os.path.join(os.path.dirname(__file__), 'fonts', 'arialbd.ttf')
        ]
        for fp in local_fonts:
            if os.path.exists(fp):
                font_path = fp
                print(f"Police locale trouvée : {font_path}")
                break
    processor = LogoProcessor(
        margin_right=margin_right,
        margin_top=margin_top,
        jpeg_quality=jpeg_quality,
        white_threshold=white_threshold
    )

    # Traitement des images
    print("\nTraitement des images...\n")
    if levels_list:
        from logo_processor import LogoProcessor as _LP
        gen_proc = _LP()
        total_success = 0
        total_failed = 0
        for lv in levels_list:
            out_logo_path = os.path.join(config.get_logos_dir(), f"logo_{lv}.png")
            if not os.path.exists(out_logo_path):
                gen_proc.generate_heavy_logo(
                    lv,
                    out_logo_path,
                    kerning=args.kerning,
                    font_path=font_path
                )
            run_suffix = config.get_logo_suffix(lv)
            print(f"\n--- Niveau {lv} ---")
            s, f = processor.apply_logo_to_folder(
                logo_path=out_logo_path,
                input_folder=input_dir,
                output_folder=config.get_output_dir(),
                suffix=run_suffix,
                extensions=extensions,
                workers=args.workers,
                full_quality=args.full_quality
            )
            total_success += s; total_failed += f
        successful, failed = total_success, total_failed
    else:
        successful, failed = processor.apply_logo_to_folder(
            logo_path=logo_path,
            input_folder=input_dir,
            output_folder=config.get_output_dir(),
            suffix=suffix,
            extensions=extensions,
            workers=args.workers,
            full_quality=args.full_quality
        )

    # Résumé
    print(f"\n{'='*70}")
    print("TRAITEMENT TERMINÉ")
    print(f"{'='*70}")
    print(f"  Nombre total d'images (par logo): {image_count}")
    if levels_list:
        print(f"  Logos traités: {len(levels_list)}")
    print(f"  Succès: {successful}")
    print(f"  Échecs: {failed}")
    print(f"  Dossier de sortie: {os.path.abspath(config.get_output_dir())}")
    print(f"{'='*70}\n")

    input("Appuyez sur Entrée pour quitter...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
