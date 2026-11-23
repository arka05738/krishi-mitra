# Synthetic and Test Sample Image Generator for Offline Vision Pipeline
"""
Generates realistic crop and flower leaf images with symptoms for offline testing and demo.
Produces clean JPEG files in server/app/vision/sample_images/:
- tomato_healthy.jpg
- tomato_early_blight.jpg
- potato_late_blight.jpg
- sunflower_healthy.jpg
- corn_common_rust.jpg
- apple_scab.jpg
"""

import os
import math
import random
from pathlib import Path
from typing import Tuple, List, Optional
from PIL import Image, ImageDraw, ImageFilter


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "sample_images"


def _create_base_canvas(width: int = 512, height: int = 512, bg_color: Tuple[int, int, int] = (240, 238, 230)) -> Image.Image:
    """Create a textured neutral background canvas for realistic leaf staging."""
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Subtle background vignette and grain
    for _ in range(300):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        shade = random.randint(-8, 8)
        c = (
            max(0, min(255, bg_color[0] + shade)),
            max(0, min(255, bg_color[1] + shade)),
            max(0, min(255, bg_color[2] + shade))
        )
        draw.point((x, y), fill=c)
    return img


def generate_tomato_healthy(output_path: Path) -> Path:
    """Generate healthy tomato compound leaflet with clean veins and vibrant green color."""
    img = _create_base_canvas(512, 512, bg_color=(235, 232, 222))
    draw = ImageDraw.Draw(img)

    # Stem
    draw.line([(256, 490), (256, 320)], fill=(76, 120, 50), width=9)
    draw.line([(256, 380), (160, 310)], fill=(80, 125, 52), width=6)
    draw.line([(256, 350), (350, 290)], fill=(80, 125, 52), width=6)

    # Draw central large leaflet (lobed tomato shape)
    leaf_pts = [
        (256, 80), (280, 110), (315, 140), (310, 175), (330, 205),
        (300, 235), (285, 275), (270, 315), (256, 335),
        (242, 315), (227, 275), (212, 235), (182, 205),
        (202, 175), (197, 140), (232, 110)
    ]
    draw.polygon(leaf_pts, fill=(45, 125, 40), outline=(32, 95, 28))

    # Lateral leaflets
    left_leaflet = [
        (160, 310), (130, 280), (105, 250), (115, 220), (145, 235),
        (165, 255), (180, 285)
    ]
    draw.polygon(left_leaflet, fill=(48, 130, 42), outline=(35, 98, 30))

    right_leaflet = [
        (350, 290), (380, 260), (405, 230), (395, 200), (365, 215),
        (345, 235), (330, 265)
    ]
    draw.polygon(right_leaflet, fill=(48, 130, 42), outline=(35, 98, 30))

    # Main midrib and lateral veins
    draw.line([(256, 335), (256, 85)], fill=(95, 165, 75), width=4)
    for y_pos in [130, 170, 210, 250, 290]:
        offset = (y_pos - 80) // 4
        draw.line([(256, y_pos), (256 - 35 - offset, y_pos - 20)], fill=(90, 160, 70), width=2)
        draw.line([(256, y_pos), (256 + 35 + offset, y_pos - 20)], fill=(90, 160, 70), width=2)

    # Smooth blur for realistic natural leaf texture
    img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
    img.save(output_path, "JPEG", quality=95)
    return output_path


def generate_tomato_early_blight(output_path: Path) -> Path:
    """Generate tomato leaflet showing early blight concentric target-board ring lesions."""
    img = _create_base_canvas(512, 512, bg_color=(235, 232, 222))
    draw = ImageDraw.Draw(img)

    # Stem
    draw.line([(256, 490), (256, 320)], fill=(85, 115, 55), width=8)

    # Tomato leaflet base with stressed yellow-green margins
    leaf_pts = [
        (256, 80), (285, 115), (320, 150), (310, 185), (335, 220),
        (300, 245), (285, 285), (270, 320), (256, 340),
        (242, 320), (227, 285), (212, 245), (177, 220),
        (202, 185), (192, 150), (227, 115)
    ]
    draw.polygon(leaf_pts, fill=(65, 120, 45), outline=(45, 95, 30))

    # Main veins
    draw.line([(256, 340), (256, 85)], fill=(110, 150, 70), width=4)
    for y_pos in [140, 180, 220, 260, 300]:
        draw.line([(256, y_pos), (210, y_pos - 18)], fill=(105, 145, 65), width=2)
        draw.line([(256, y_pos), (300, y_pos - 18)], fill=(105, 145, 65), width=2)

    # Early Blight Lesions: Concentric target-board brown rings with chlorotic yellow halos
    lesions = [
        (230, 210, 34),  # Center-left spot
        (280, 250, 28),  # Lower-right spot
        (245, 140, 24),  # Upper spot
        (205, 170, 18),  # Left margin spot
        (295, 180, 20),  # Right margin spot
    ]

    for cx, cy, rad in lesions:
        # Chlorotic yellow outer halo
        draw.ellipse([cx - rad - 8, cy - rad - 8, cx + rad + 8, cy + rad + 8], fill=(195, 185, 45, 180))
        # Outer dark ring
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(55, 35, 20))
        # Intermediate lighter brown ring
        draw.ellipse([cx - rad + 5, cy - rad + 5, cx + rad - 5, cy + rad - 5], fill=(95, 65, 35))
        # Inner dark ring
        draw.ellipse([cx - rad + 10, cy - rad + 10, cx + rad - 10, cy + rad - 10], fill=(45, 28, 15))
        # Center necrotic spot
        draw.ellipse([cx - rad + 14, cy - rad + 14, cx + rad - 14, cy + rad - 14], fill=(30, 20, 10))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    img.save(output_path, "JPEG", quality=95)
    return output_path


def generate_potato_late_blight(output_path: Path) -> Path:
    """Generate potato leaf displaying severe dark water-soaked late blight decay lesions."""
    img = _create_base_canvas(512, 512, bg_color=(230, 228, 220))
    draw = ImageDraw.Draw(img)

    # Stalk
    draw.line([(256, 490), (256, 330)], fill=(90, 110, 60), width=9)

    # Broad ovate potato leaf blade
    leaf_pts = [
        (256, 75), (295, 105), (345, 155), (370, 215), (365, 285),
        (335, 340), (290, 375), (256, 390), (222, 375), (177, 340),
        (147, 285), (142, 215), (167, 155), (217, 105)
    ]
    draw.polygon(leaf_pts, fill=(55, 105, 40), outline=(38, 78, 28))

    # Midrib and veins
    draw.line([(256, 390), (256, 80)], fill=(115, 145, 75), width=5)
    for y_pos in [140, 195, 250, 305, 350]:
        draw.line([(256, y_pos), (175, y_pos - 25)], fill=(105, 135, 70), width=2)
        draw.line([(256, y_pos), (337, y_pos - 25)], fill=(105, 135, 70), width=2)

    # Late Blight Lesions: Irregular, water-soaked black/brown rotting areas spreading from edges
    # Major rotting blotch at right leaf margin
    blight_patch_1 = [
        (310, 160), (365, 180), (375, 240), (360, 290), (320, 280),
        (290, 240), (285, 190)
    ]
    draw.polygon(blight_patch_1, fill=(35, 25, 20), outline=(95, 120, 60))

    # Major rotting blotch at leaf tip
    blight_patch_2 = [
        (256, 75), (285, 100), (275, 145), (240, 140), (225, 100)
    ]
    draw.polygon(blight_patch_2, fill=(28, 20, 15), outline=(100, 125, 60))

    # Lower left water-soaked lesion
    blight_patch_3 = [
        (160, 260), (210, 275), (220, 330), (175, 340), (145, 300)
    ]
    draw.polygon(blight_patch_3, fill=(38, 30, 22), outline=(105, 130, 65))

    # White fuzzy mold fringes on the lesion edges
    for bx, by in [(285, 195), (290, 230), (318, 275), (245, 138), (212, 285)]:
        draw.ellipse([bx - 8, by - 5, bx + 8, by + 5], fill=(225, 228, 220, 170))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.9))
    img.save(output_path, "JPEG", quality=95)
    return output_path


def generate_sunflower_healthy(output_path: Path) -> Path:
    """Generate vibrant healthy sunflower head with golden petals and central seed disk."""
    img = _create_base_canvas(512, 512, bg_color=(238, 235, 225))
    draw = ImageDraw.Draw(img)

    # Green stem and background leaves
    draw.line([(256, 490), (256, 256)], fill=(55, 125, 45), width=16)

    # Background cordate green leaves
    left_leaf = [(256, 360), (160, 380), (100, 420), (130, 470), (210, 460), (256, 410)]
    draw.polygon(left_leaf, fill=(45, 115, 38), outline=(32, 90, 28))
    right_leaf = [(256, 360), (352, 380), (412, 420), (382, 470), (302, 460), (256, 410)]
    draw.polygon(right_leaf, fill=(45, 115, 38), outline=(32, 90, 28))

    cx, cy = 256, 240
    num_petals = 28
    petal_len = 110
    disk_radius = 65

    # Draw golden yellow ray petals radiating around the head
    for i in range(num_petals):
        angle = (2 * math.pi / num_petals) * i
        # Petal tip
        tx = cx + int((disk_radius + petal_len) * math.cos(angle))
        ty = cy + int((disk_radius + petal_len) * math.sin(angle))
        # Petal base sides
        b_angle1 = angle - 0.08
        b_angle2 = angle + 0.08
        bx1 = cx + int(disk_radius * math.cos(b_angle1))
        by1 = cy + int(disk_radius * math.sin(b_angle1))
        bx2 = cx + int(disk_radius * math.cos(b_angle2))
        by2 = cy + int(disk_radius * math.sin(b_angle2))

        # Petal color variation
        petal_color = (255, 205 + (i % 5) * 8, 10 + (i % 3) * 10)
        draw.polygon([(bx1, by1), (tx, ty), (bx2, by2)], fill=petal_color, outline=(225, 160, 5))

    # Central dark disk (spiral florets)
    draw.ellipse([cx - disk_radius, cy - disk_radius, cx + disk_radius, cy + disk_radius], fill=(68, 42, 20), outline=(48, 28, 12))

    # Inner disk texture
    for _ in range(250):
        r = random.uniform(0, disk_radius - 5)
        theta = random.uniform(0, 2 * math.pi)
        px = cx + int(r * math.cos(theta))
        py = cy + int(r * math.sin(theta))
        seed_shade = random.choice([(85, 55, 25), (105, 75, 35), (55, 35, 15)])
        draw.point((px, py), fill=seed_shade)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
    img.save(output_path, "JPEG", quality=95)
    return output_path


def generate_corn_common_rust(output_path: Path) -> Path:
    """Generate maize corn leaf with parallel veins and elongated cinnamon-brown rust pustules."""
    img = _create_base_canvas(512, 512, bg_color=(235, 235, 225))
    draw = ImageDraw.Draw(img)

    # Elongated broad maize leaf blade angled diagonally
    corn_leaf_pts = [
        (80, 480), (120, 360), (180, 240), (250, 140), (320, 60), (360, 30),
        (380, 35), (370, 90), (340, 190), (290, 300), (240, 400), (200, 490)
    ]
    draw.polygon(corn_leaf_pts, fill=(75, 135, 50), outline=(55, 105, 38))

    # Prominent central midrib
    draw.line([(140, 485), (370, 32)], fill=(145, 185, 95), width=7)

    # Parallel lateral veins along the blade
    for offset in range(-60, 70, 12):
        if offset == 0:
            continue
        p1 = (140 + offset, 485)
        p2 = (370 + int(offset * 0.4), 32)
        draw.line([p1, p2], fill=(95, 155, 68), width=2)

    # Cinnamon-brown and golden-orange rust pustules scattered along the blade
    random.seed(42)
    for _ in range(65):
        # Sample points along the leaf
        t = random.uniform(0.15, 0.85)
        lx = 140 * (1 - t) + 370 * t + random.uniform(-45, 45)
        ly = 485 * (1 - t) + 32 * t + random.uniform(-20, 20)
        pustule_w = random.randint(4, 9)
        pustule_h = random.randint(2, 5)

        # Yellowish halo
        draw.ellipse([lx - pustule_w - 2, ly - pustule_h - 2, lx + pustule_w + 2, ly + pustule_h + 2], fill=(190, 170, 40))
        # Rust colored pustule
        draw.ellipse([lx - pustule_w, ly - pustule_h, lx + pustule_w, ly + pustule_h], fill=(175, 65, 20))
        # Powder core
        draw.ellipse([lx - pustule_w + 2, ly - pustule_h + 1, lx + pustule_w - 2, ly + pustule_h - 1], fill=(210, 105, 30))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
    img.save(output_path, "JPEG", quality=95)
    return output_path


def generate_apple_scab(output_path: Path) -> Path:
    """Generate rounded apple leaf showing olive-green to black velvety scab lesions."""
    img = _create_base_canvas(512, 512, bg_color=(236, 234, 224))
    draw = ImageDraw.Draw(img)

    # Petiole (leaf stem)
    draw.line([(256, 490), (256, 370)], fill=(95, 110, 65), width=7)

    # Rounded oval apple leaf with fine serrations
    leaf_pts = [
        (256, 75), (290, 100), (330, 140), (360, 195), (370, 260),
        (350, 320), (310, 365), (256, 380), (202, 365), (162, 320),
        (142, 260), (152, 195), (182, 140), (222, 100)
    ]
    draw.polygon(leaf_pts, fill=(50, 115, 45), outline=(35, 88, 32))

    # Veins
    draw.line([(256, 380), (256, 80)], fill=(110, 155, 80), width=5)
    for y_pos in [140, 190, 240, 290, 340]:
        draw.line([(256, y_pos), (175, y_pos - 30)], fill=(95, 140, 70), width=2)
        draw.line([(256, y_pos), (337, y_pos - 30)], fill=(95, 140, 70), width=2)

    # Apple Scab Lesions: Olive-green to dark velvety circular spots with feathery edges
    scab_lesions = [
        (225, 175, 26),
        (285, 210, 30),
        (210, 265, 22),
        (295, 285, 25),
        (256, 125, 18),
        (325, 160, 16),
        (185, 205, 15),
    ]

    for cx, cy, rad in scab_lesions:
        # Feathery olive border
        draw.ellipse([cx - rad - 4, cy - rad - 4, cx + rad + 4, cy + rad + 4], fill=(70, 85, 45))
        # Dark olive velvety scab body
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(42, 52, 28))
        # Central darker crust
        draw.ellipse([cx - rad + 6, cy - rad + 6, cx + rad - 6, cy + rad - 6], fill=(28, 35, 18))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    img.save(output_path, "JPEG", quality=95)
    return output_path


def generate_all_sample_images(output_dir: Optional[Path] = None) -> List[Path]:
    """
    Generate the complete curated suite of realistic sample images:
    - tomato_healthy.jpg
    - tomato_early_blight.jpg
    - potato_late_blight.jpg
    - sunflower_healthy.jpg
    - corn_common_rust.jpg
    - apple_scab.jpg
    """
    out_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    generators = {
        "tomato_healthy.jpg": generate_tomato_healthy,
        "tomato_early_blight.jpg": generate_tomato_early_blight,
        "potato_late_blight.jpg": generate_potato_late_blight,
        "sunflower_healthy.jpg": generate_sunflower_healthy,
        "corn_common_rust.jpg": generate_corn_common_rust,
        "apple_scab.jpg": generate_apple_scab,
    }

    generated_paths: List[Path] = []
    for filename, gen_fn in generators.items():
        file_path = out_dir / filename
        gen_fn(file_path)
        generated_paths.append(file_path)
        print(f"Generated sample image: {file_path}")

    return generated_paths


if __name__ == "__main__":
    generate_all_sample_images()
