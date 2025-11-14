"""
Logo Processor Module
Handles logo extraction, resizing, and application on product images
"""

from PIL import Image
from PIL import ImageDraw, ImageFont
import numpy as np
import os
from typing import Tuple, List, Optional
from pathlib import Path


class LogoProcessor:
    """Main class for processing logos on product images"""
    
    def __init__(self, margin_right: int = 21, margin_top: int = 22, 
                 jpeg_quality: int = 95, white_threshold: int = 250):
        """
        Initialize the LogoProcessor
        
        Args:
            margin_right: Distance from right edge in pixels
            margin_top: Distance from top edge in pixels
            jpeg_quality: JPEG output quality (1-100)
            white_threshold: Threshold for detecting non-white pixels (0-255)
        """
        self.margin_right = margin_right
        self.margin_top = margin_top
        self.jpeg_quality = jpeg_quality
        self.white_threshold = white_threshold
    
    def extract_logo_from_image(self, image_path: str, output_path: str) -> Tuple[int, int]:
        """
        Extract logo from an image by detecting non-white pixels in top-right corner
        
        Args:
            image_path: Path to source image
            output_path: Path to save extracted logo
            
        Returns:
            Tuple of (width, height) of extracted logo
            
        Raises:
            ValueError: If no logo is detected
            FileNotFoundError: If image file doesn't exist
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        print(f"Extracting logo from: {image_path}")
        
        # Load image
        img = Image.open(image_path)
        width, height = img.size
        print(f"  Image dimensions: {width}x{height}")
        
        # Convert to array
        img_array = np.array(img)
        
        # Define search area (top-right corner)
        search_area_left = width - 150
        search_area_top = self.margin_top
        search_area_right = width - self.margin_right
        search_area_bottom = self.margin_top + 150
        
        # Extract search region
        search_region = img_array[search_area_top:search_area_bottom, 
                                   search_area_left:search_area_right]
        
        # Find non-white pixels
        if len(search_region.shape) == 3:
            non_white_mask = (search_region[:, :, 0] < self.white_threshold) | \
                           (search_region[:, :, 1] < self.white_threshold) | \
                           (search_region[:, :, 2] < self.white_threshold)
        else:
            non_white_mask = search_region < self.white_threshold
        
        # Find coordinates
        rows, cols = np.where(non_white_mask)
        
        if len(rows) == 0:
            raise ValueError("No logo detected in search area")
        
        # Find logo boundaries
        logo_top_rel = rows.min()
        logo_bottom_rel = rows.max() + 1
        logo_left_rel = cols.min()
        logo_right_rel = cols.max() + 1
        
        # Convert to absolute coordinates
        logo_top_abs = search_area_top + logo_top_rel
        logo_bottom_abs = search_area_top + logo_bottom_rel
        logo_left_abs = search_area_left + logo_left_rel
        logo_right_abs = search_area_left + logo_right_rel
        
        print(f"  Logo boundaries: top={logo_top_abs}, bottom={logo_bottom_abs}, "
              f"left={logo_left_abs}, right={logo_right_abs}")
        
        # Extract logo
        logo_region = img.crop((logo_left_abs, logo_top_abs, logo_right_abs, logo_bottom_abs))
        
        # Convert to RGBA for transparency
        logo_region = logo_region.convert('RGBA')
        logo_data = np.array(logo_region)
        # Strict binary transparency: any pixel whose all channels > threshold becomes fully transparent
        # (luminosity > threshold => transparent, else opaque)
        rgb = logo_data[:, :, :3]
        white_mask = (rgb[:, :, 0] > self.white_threshold) & \
                (rgb[:, :, 1] > self.white_threshold) & \
                (rgb[:, :, 2] > self.white_threshold)
        alpha_channel = (~white_mask).astype(np.uint8) * 255
        logo_data[:, :, 3] = alpha_channel
        
        # Create transparent logo
        logo_transparent = Image.fromarray(logo_data, 'RGBA')
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save
        logo_transparent.save(output_path, dpi=(72,72))
        print(f"  Logo saved: {output_path}")
        print(f"  Dimensions: {logo_transparent.size}")
        
        return logo_transparent.size

    def extract_fixed_logo(self, image_path: str, output_path: str, 
                            fixed_width: int = 99, fixed_height: int = 90) -> Tuple[int, int]:
        """Extract a fixed-size logo region using margins without dynamic detection.

        The region is defined as a rectangle of size (fixed_width x fixed_height)
        whose right edge is margin_right pixels from the image's right border and
        whose top edge is margin_top pixels from the top border.

        Transparency is applied using strict binary threshold: pixels with ALL
        RGB channels > white_threshold become fully transparent; others opaque.
        Saved at 72 DPI.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        print(f"Fixed extraction from: {image_path}")
        img = Image.open(image_path).convert('RGB')
        width, height = img.size
        # Compute crop box
        right = width - self.margin_right
        left = right - fixed_width
        top = self.margin_top
        bottom = top + fixed_height
        if left < 0 or bottom > height:
            raise ValueError("Fixed logo region goes outside image bounds. Adjust margins or provide larger image.")
        region = img.crop((left, top, right, bottom)).convert('RGBA')
        data = np.array(region)
        rgb = data[:, :, :3]
        white_mask = (rgb[:, :, 0] > self.white_threshold) & \
                     (rgb[:, :, 1] > self.white_threshold) & \
                     (rgb[:, :, 2] > self.white_threshold)
        data[:, :, 3] = (~white_mask).astype(np.uint8) * 255
        logo = Image.fromarray(data, 'RGBA')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logo.save(output_path, dpi=(72,72))
        print(f"  Fixed logo saved: {output_path} size={logo.size}")
        return logo.size

    def validate_logo_dimensions(self, logo_path: str, expected: Tuple[int,int] = (99,90)) -> bool:
        """Validate that an existing logo file matches expected dimensions."""
        if not os.path.exists(logo_path):
            print(f"Logo not found for validation: {logo_path}")
            return False
        with Image.open(logo_path) as im:
            if im.size == expected:
                return True
            print(f"Warning: Logo {logo_path} has size {im.size}, expected {expected}.")
            return False

    def generate_text_logo(self, text: str, output_path: str,
                            width: int = 99, height: int = 90,
                            dpi: Tuple[int,int] = (72,72)) -> Tuple[int,int]:
        """Generate a black text logo (e.g., 'x6') with transparent background.

        Args:
            text: The text to render (e.g. 'x6').
            output_path: Destination PNG path.
            width: Target width (default 99).
            height: Target height (default 90).
            dpi: DPI tuple (default 72,72).

        Returns:
            (width, height) of generated logo.
        """
        img = Image.new('RGBA', (width, height), (255,255,255,0))
        draw = ImageDraw.Draw(img)
        # Attempt to load a common font; fallback to default.
        try:
            font = ImageFont.truetype("arial.ttf", 72)
        except Exception:
            font = ImageFont.load_default()
        # Compute text bounding box
        bbox = draw.textbbox((0,0), text, font=font)
        text_w = bbox[2]-bbox[0]
        text_h = bbox[3]-bbox[1]
        # Center text
        x = (width - text_w)//2
        y = (height - text_h)//2
        draw.text((x,y), text, font=font, fill=(0,0,0,255))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, dpi=dpi)
        print(f"Generated logo '{text}' -> {output_path} size={img.size}")
        return img.size

    def generate_heavy_logo(self, text: str, output_path: str,
                             target_size: Tuple[int,int] = (99,90),
                             dpi: Tuple[int,int] = (72,72),
                             max_font: int = 160,
                             min_font: int = 40,
                             kerning: int = -70,
                             font_path: str = None) -> Tuple[int,int]:
        """
        Génère un logo typographique ultra-bold selon les spécifications fournies.
        Police prioritaire : Impact, puis Arial Black, Anton, Helvetica Black, Futura Black, Bebas Neue, Montserrat Black, Oswald Bold, League Gothic Bold.
        Taille ajustée pour occuper 99x90px, kerning très serré (-70 par défaut), couleur #000000, fond transparent, lissage activé.
        """
        tw, th = target_size
        # Sélection de la police
        font_candidates = []
        if font_path:
            font_candidates.append(font_path)
        font_candidates += [
            "C:/Windows/Fonts/impact.ttf",
            "/Library/Fonts/Impact.ttf",
            "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/anton.ttf",
            "C:/Windows/Fonts/helveticablack.ttf",
            "C:/Windows/Fonts/futurablack.ttf",
            "C:/Windows/Fonts/BebasNeue-Regular.ttf",
            "C:/Windows/Fonts/Montserrat-Black.ttf",
            "C:/Windows/Fonts/Oswald-Bold.ttf",
            "C:/Windows/Fonts/LeagueGothic-Bold.ttf"
        ]
        selected_font_path = None
        for p in font_candidates:
            if os.path.exists(p):
                selected_font_path = p
                break
        if selected_font_path:
            font_name = os.path.basename(selected_font_path)
        else:
            font_name = "default"
        # Boucle de taille pour occuper au mieux 99x90
        size_found = max_font
        for fs in range(max_font, min_font-1, -2):
            try:
                font = ImageFont.truetype(selected_font_path, fs) if selected_font_path else ImageFont.load_default()
            except Exception:
                font = ImageFont.load_default()
            tmp = Image.new('RGBA', (tw*4, th*4), (255,255,255,0))
            d = ImageDraw.Draw(tmp)
            x_cursor = 0
            max_y = 0
            for idx, ch in enumerate(text):
                bbox = d.textbbox((x_cursor,0), ch, font=font)
                d.text((x_cursor,0), ch, font=font, fill=(0,0,0,255))
                x_cursor += (bbox[2]-bbox[0]) + kerning
                max_y = max(max_y, bbox[3])
            # Validation des coordonnées de crop
            crop_right = max(x_cursor + 10, 10)
            crop_bottom = max(max_y + 10, 10)
            content = tmp.crop((0, 0, crop_right, crop_bottom))
            cw,ch = content.size
            if cw <= tw and ch <= th:
                size_found = fs
                break
        # Rendu final
        try:
            font = ImageFont.truetype(selected_font_path, size_found) if selected_font_path else ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        canvas = Image.new('RGBA', (tw, th), (255,255,255,0))
        draw = ImageDraw.Draw(canvas)
        x_cursor = 0
        max_y = 0
        for ch in text:
            bbox = draw.textbbox((x_cursor,0), ch, font=font)
            draw.text((x_cursor,0), ch, font=font, fill=(0,0,0,255))
            x_cursor += (bbox[2]-bbox[0]) + kerning
            max_y = max(max_y, bbox[3])
        # Validation des coordonnées de crop
        crop_right = max(min(x_cursor, tw), 1)
        crop_bottom = max(min(max_y, th), 1)
        content = canvas.crop((0, 0, crop_right, crop_bottom))
        cw,ch = content.size
        result = Image.new('RGBA', (tw,th), (255,255,255,0))
        off_x = (tw - cw)//2
        off_y = (th - ch)//2
        result.paste(content, (off_x, off_y), content)
        # Créer le dossier parent si nécessaire
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        result.save(output_path, dpi=dpi)
        print(f"Logo '{text}' généré: police={font_name}, taille={size_found}, kerning={kerning}, {output_path}")
        return result.size
    
    def resize_logo(self, source_path: str, output_path: str, 
                   target_height: int, padding: int = 3) -> Tuple[int, int]:
        """
        Resize logo to target height while maintaining aspect ratio
        
        Args:
            source_path: Path to source logo
            output_path: Path to save resized logo
            target_height: Target height in pixels
            padding: Padding around logo in pixels
            
        Returns:
            Tuple of (width, height) of resized logo
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Logo not found: {source_path}")
        
        print(f"Resizing logo: {source_path}")
        
        logo = Image.open(source_path).convert('RGBA')
        logo_data = np.array(logo)
        
        # Find content boundaries
        alpha_channel = logo_data[:, :, 3]
        non_transparent = alpha_channel > 0
        rows, cols = np.where(non_transparent)
        
        if len(rows) == 0:
            raise ValueError("No content found in logo")
        
        top = rows.min()
        bottom = rows.max() + 1
        left = cols.min()
        right = cols.max() + 1
        
        # Extract content
        content = logo.crop((left, top, right, bottom))
        content_width, content_height = content.size
        
        # Calculate new dimensions
        scale_factor = target_height / content_height
        new_width = int(content_width * scale_factor)
        new_height = target_height
        
        print(f"  Original size: {content_width}x{content_height}")
        print(f"  Target size: {new_width}x{new_height}")
        
        # Resize
        content_resized = content.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Add padding
        final_width = new_width + (padding * 2)
        final_height = new_height + (padding * 2)
        
        final_logo = Image.new('RGBA', (final_width, final_height), (255, 255, 255, 0))
        final_logo.paste(content_resized, (padding, padding), content_resized)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save
        final_logo.save(output_path)
        print(f"  Resized logo saved: {output_path}")
        print(f"  Final dimensions: {final_logo.size}")
        
        return final_logo.size
    
    def apply_logo_to_image(self, logo_path: str, image_path: str, 
                           output_path: str, full_quality: bool = False) -> bool:
        """
        Apply logo to a single image
        
        Args:
            logo_path: Path to logo file
            image_path: Path to source image
            output_path: Path to save processed image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load logo
            logo = Image.open(logo_path)
            
            # Load image
            img = Image.open(image_path)
            width, height = img.size
            
            # Convert to RGBA
            img_rgba = img.convert('RGBA')
            
            # Calculate logo position
            paste_x = width - self.margin_right - logo.width
            paste_y = self.margin_top
            
            # Paste logo
            img_rgba.paste(logo, (paste_x, paste_y), logo)
            
            # Convert back to RGB for JPEG
            img_final = img_rgba.convert('RGB')
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save
            if full_quality:
                img_final.save(output_path, 'JPEG', quality=100, subsampling=0, optimize=False)
            else:
                img_final.save(output_path, 'JPEG', quality=self.jpeg_quality)
            
            return True
        except Exception as e:
            print(f"  Error processing {image_path}: {e}")
            return False
    
    def apply_logo_to_folder(self, logo_path: str, input_folder: str, 
                            output_folder: str, suffix: str = "_logo",
                            extensions: List[str] = None, workers: int = 1,
                            full_quality: bool = False) -> Tuple[int, int]:
        """
        Apply logo to all images in a folder
        
        Args:
            logo_path: Path to logo file
            input_folder: Folder containing input images
            output_folder: Folder for output images
            suffix: Suffix to add to filenames
            extensions: List of file extensions to process (default: ['.jpg', '.jpeg', '.png'])
            
        Returns:
            Tuple of (successful_count, failed_count)
        """
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
        
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"Logo not found: {logo_path}")
        
        if not os.path.exists(input_folder):
            raise FileNotFoundError(f"Input folder not found: {input_folder}")
        
        # Créer un sous-dossier spécifique selon le type de logo
        logo_filename = os.path.basename(logo_path)
        if "_x" in logo_filename:
            # Extraire le type de logo (x2, x3, etc.) du nom de fichier
            logo_type = logo_filename.split("_x")[1].split(".")[0]
            specific_output_folder = os.path.join(output_folder, f"x{logo_type}-lots")
        else:
            # Fallback si le pattern n'est pas reconnu
            specific_output_folder = os.path.join(output_folder, "processed")
        
        # Créer le dossier de sortie spécifique s'il n'existe pas
        os.makedirs(specific_output_folder, exist_ok=True)
        
        # Utiliser le dossier spécifique au lieu du dossier de sortie général
        output_folder = specific_output_folder
        
        # Get all image files
        image_files = []
        for ext in extensions:
            image_files.extend(Path(input_folder).glob(f'*{ext}'))
        
        if len(image_files) == 0:
            print(f"No images found in {input_folder}")
            return (0, 0)
        
        print(f"\nProcessing {len(image_files)} images from {input_folder}")
        print(f"Output folder: {output_folder}")
        print(f"Logo: {logo_path}")
        if workers > 1:
            print(f"Parallel workers: {workers}")
        print()
        
        successful = 0
        failed = 0
        
        if workers <= 1:
            # Sequential processing
            for i, image_path in enumerate(image_files, 1):
                image_path = str(image_path)
                base_name = os.path.basename(image_path)
                name_without_ext = os.path.splitext(base_name)[0]
                output_path = os.path.join(output_folder, f"{name_without_ext}{suffix}.jpg")
                print(f"[{i}/{len(image_files)}] Processing: {base_name}")
                if self.apply_logo_to_image(logo_path, image_path, output_path, full_quality=full_quality):
                    print(f"  ✓ Saved: {output_path}")
                    successful += 1
                else:
                    print(f"  ✗ Failed")
                    failed += 1
        else:
            # Parallel processing
            from concurrent.futures import ThreadPoolExecutor, as_completed
            def task(image_path):
                image_path = str(image_path)
                base_name = os.path.basename(image_path)
                name_without_ext = os.path.splitext(base_name)[0]
                output_path = os.path.join(output_folder, f"{name_without_ext}{suffix}.jpg")
                ok = self.apply_logo_to_image(logo_path, image_path, output_path, full_quality=full_quality)
                return base_name, output_path, ok
            with ThreadPoolExecutor(max_workers=workers) as executor:
                future_map = {executor.submit(task, p): p for p in image_files}
                done_count = 0
                for future in as_completed(future_map):
                    done_count += 1
                    try:
                        base_name, output_path, ok = future.result()
                        print(f"[{done_count}/{len(image_files)}] {base_name}: {'✓' if ok else '✗'}")
                        if ok:
                            successful += 1
                        else:
                            failed += 1
                    except Exception as e:
                        p = future_map[future]
                        print(f"Error processing {p}: {e}")
                        failed += 1
        
        print(f"\n{'='*60}")
        print(f"Processing complete!")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"{'='*60}\n")
        
        return (successful, failed)
