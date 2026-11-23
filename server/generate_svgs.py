import os

svg_dir = r"D:\ARM\client\src\assets\crops"
os.makedirs(svg_dir, exist_ok=True)

svgs = {
    "wheat.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="wheatGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD700" />
      <stop offset="100%" stop-color="#D4AF37" />
    </linearGradient>
    <linearGradient id="wheatBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#wheatBlue)" stroke="#D4AF37" stroke-width="1.5"/>
  <path d="M32 54 C32 40 32 20 32 10" stroke="#FFD700" stroke-width="2" stroke-linecap="round"/>
  <path d="M32 46 C24 43 23 35 30 38" fill="url(#wheatGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <path d="M32 38 C23 35 22 27 30 30" fill="url(#wheatGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <path d="M32 30 C22 27 21 19 30 22" fill="url(#wheatGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <path d="M32 22 C22 19 21 11 30 14" fill="url(#wheatGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <path d="M32 46 C40 43 41 35 34 38" fill="url(#wheatGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <path d="M32 38 C41 35 42 27 34 30" fill="url(#wheatGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <path d="M32 30 C42 27 43 19 34 22" fill="url(#wheatGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <path d="M32 22 C42 19 43 11 34 14" fill="url(#wheatGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <path d="M32 14 C32 10 32 8 32 6" stroke="#FFD700" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M32 12 C28 9 24 7 22 5" stroke="#FFD700" stroke-width="1" stroke-linecap="round"/>
  <path d="M32 12 C36 9 40 7 42 5" stroke="#FFD700" stroke-width="1" stroke-linecap="round"/>
</svg>""",

    "rice.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="riceGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="100%" stop-color="#CA8A04" />
    </linearGradient>
    <linearGradient id="riceBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#riceBlue)" stroke="#D4AF37" stroke-width="1.5"/>
  <path d="M18 54 C20 38 28 22 46 16" stroke="#D4AF37" stroke-width="2" stroke-linecap="round" fill="none"/>
  <ellipse cx="44" cy="18" rx="3.5" ry="2" transform="rotate(-15 44 18)" fill="url(#riceGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <ellipse cx="39" cy="21" rx="3.5" ry="2" transform="rotate(10 39 21)" fill="url(#riceGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <ellipse cx="41" cy="27" rx="3.5" ry="2" transform="rotate(35 41 27)" fill="url(#riceGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <ellipse cx="34" cy="26" rx="3.5" ry="2" transform="rotate(-5 34 26)" fill="url(#riceGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <ellipse cx="33" cy="33" rx="3.5" ry="2" transform="rotate(30 33 33)" fill="url(#riceGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <ellipse cx="27" cy="32" rx="3.5" ry="2" transform="rotate(5 27 32)" fill="url(#riceGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <ellipse cx="27" cy="39" rx="3.5" ry="2" transform="rotate(40 27 39)" fill="url(#riceGold)" stroke="#FFFFFF" stroke-width="0.5"/>
  <ellipse cx="22" cy="42" rx="3.5" ry="2" transform="rotate(15 22 42)" fill="url(#riceGold)" stroke="#FFFFFF" stroke-width="0.5"/>
</svg>""",

    "tomato.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="tomatoRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EF4444" />
      <stop offset="70%" stop-color="#DC2626" />
      <stop offset="100%" stop-color="#991B1B" />
    </linearGradient>
    <linearGradient id="tomatoBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#tomatoBlue)" stroke="#D4AF37" stroke-width="1.5"/>
  <path d="M32 20 C22 20 14 26 14 36 C14 47 23 54 32 54 C41 54 50 47 50 36 C50 26 42 20 32 20 Z" fill="url(#tomatoRed)" stroke="#F59E0B" stroke-width="1"/>
  <ellipse cx="25" cy="30" rx="5" ry="3" transform="rotate(-30 25 30)" fill="#FFFFFF" opacity="0.4"/>
  <path d="M32 22 L32 13 C32 11 34 10 36 10" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <path d="M32 20 L27 16 M32 20 L37 16 M32 20 L23 23 M32 20 L41 23 M32 20 L32 26" stroke="#D4AF37" stroke-width="2" stroke-linecap="round"/>
</svg>""",

    "potato.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="potatoGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EAB308" />
      <stop offset="50%" stop-color="#CA8A04" />
      <stop offset="100%" stop-color="#854D0E" />
    </linearGradient>
    <linearGradient id="potatoBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#potatoBlue)" stroke="#D4AF37" stroke-width="1.5"/>
  <path d="M22 24 C28 20 40 22 46 28 C52 34 50 44 42 48 C34 52 24 50 18 44 C12 38 16 28 22 24 Z" fill="url(#potatoGold)" stroke="#FEF08A" stroke-width="1"/>
  <circle cx="26" cy="30" r="1.5" fill="#0B192C" opacity="0.7"/>
  <circle cx="38" cy="32" r="1.5" fill="#0B192C" opacity="0.7"/>
  <circle cx="32" cy="42" r="1.5" fill="#0B192C" opacity="0.7"/>
  <circle cx="42" cy="40" r="1.2" fill="#0B192C" opacity="0.7"/>
  <circle cx="23" cy="39" r="1.2" fill="#0B192C" opacity="0.7"/>
  <path d="M45 27 C48 24 49 22 51 23" stroke="#FEF08A" stroke-width="1.5" stroke-linecap="round" fill="none"/>
</svg>""",

    "corn.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="cornGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FDE047" />
      <stop offset="100%" stop-color="#EAB308" />
    </linearGradient>
    <linearGradient id="cornBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#cornBlue)" stroke="#D4AF37" stroke-width="1.5"/>
  <path d="M26 22 C26 15 38 15 38 22 L37 45 C37 49 27 49 27 45 Z" fill="url(#cornGold)" stroke="#CA8A04" stroke-width="1"/>
  <line x1="27" y1="25" x2="37" y2="25" stroke="#A16207" stroke-width="0.8" stroke-dasharray="2 1"/>
  <line x1="27" y1="30" x2="37" y2="30" stroke="#A16207" stroke-width="0.8" stroke-dasharray="2 1"/>
  <line x1="27" y1="35" x2="37" y2="35" stroke="#A16207" stroke-width="0.8" stroke-dasharray="2 1"/>
  <line x1="27" y1="40" x2="37" y2="40" stroke="#A16207" stroke-width="0.8" stroke-dasharray="2 1"/>
  <path d="M25 46 C20 40 16 30 18 24 C21 34 26 40 28 47" fill="#1E3E62" stroke="#D4AF37" stroke-width="1.2"/>
  <path d="M39 46 C44 40 48 30 46 24 C43 34 38 40 36 47" fill="#1E3E62" stroke="#D4AF37" stroke-width="1.2"/>
  <path d="M31 16 C30 11 29 10 28 8 M33 16 C34 11 36 9 37 8" stroke="#FEF08A" stroke-width="1" stroke-linecap="round"/>
</svg>""",

    "sunflower.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="sunGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FEF08A" />
      <stop offset="50%" stop-color="#F59E0B" />
      <stop offset="100%" stop-color="#D97706" />
    </linearGradient>
    <linearGradient id="sunBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#sunBlue)" stroke="#D4AF37" stroke-width="1.5"/>
  <g fill="url(#sunGold)" stroke="#B45309" stroke-width="0.5">
    <ellipse cx="32" cy="15" rx="4" ry="8" />
    <ellipse cx="32" cy="49" rx="4" ry="8" />
    <ellipse cx="15" cy="32" rx="8" ry="4" />
    <ellipse cx="49" cy="32" rx="8" ry="4" />
    <ellipse cx="20" cy="20" rx="4" ry="8" transform="rotate(-45 20 20)" />
    <ellipse cx="44" cy="44" rx="4" ry="8" transform="rotate(-45 44 44)" />
    <ellipse cx="44" cy="20" rx="4" ry="8" transform="rotate(45 44 20)" />
    <ellipse cx="20" cy="44" rx="4" ry="8" transform="rotate(45 20 44)" />
  </g>
  <circle cx="32" cy="32" r="12" fill="#0B192C" stroke="#D4AF37" stroke-width="1.8"/>
  <circle cx="32" cy="32" r="8" stroke="#F59E0B" stroke-width="0.8" stroke-dasharray="2 2" fill="none"/>
  <circle cx="32" cy="32" r="4" stroke="#FEF08A" stroke-width="0.8" stroke-dasharray="1.5 1.5" fill="none"/>
</svg>""",

    "cotton.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="cottonBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#cottonBlue)" stroke="#D4AF37" stroke-width="1.5"/>
  <circle cx="32" cy="26" r="9" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
  <circle cx="24" cy="33" r="8.5" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
  <circle cx="40" cy="33" r="8.5" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
  <circle cx="32" cy="37" r="8.5" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <path d="M18 36 C22 41 28 44 32 46 C36 44 42 41 46 36" stroke="#D4AF37" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M32 46 L32 54" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M32 43 L26 36 M32 43 L38 36 M32 43 L32 34" stroke="#CA8A04" stroke-width="1.5" stroke-linecap="round"/>
</svg>""",

    "apple.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="appleRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F87171" />
      <stop offset="60%" stop-color="#DC2626" />
      <stop offset="100%" stop-color="#991B1B" />
    </linearGradient>
    <linearGradient id="appleBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#appleBlue)" stroke="#D4AF37" stroke-width="1.5"/>
  <path d="M32 23 C28 20 18 20 16 32 C14 43 24 53 32 53 C40 53 50 43 48 32 C46 20 36 20 32 23 Z" fill="url(#appleRed)" stroke="#F59E0B" stroke-width="1"/>
  <ellipse cx="24" cy="31" rx="4" ry="2.5" transform="rotate(-30 24 31)" fill="#FFFFFF" opacity="0.45"/>
  <path d="M32 23 C32 17 35 13 38 11" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <path d="M34 16 C40 14 44 17 44 17 C44 17 43 22 36 21 Z" fill="#D4AF37" stroke="#FFFFFF" stroke-width="0.5"/>
</svg>""",

    "chilli.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="chilliRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EF4444" />
      <stop offset="70%" stop-color="#DC2626" />
      <stop offset="100%" stop-color="#991B1B" />
    </linearGradient>
    <linearGradient id="chilliBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#chilliBlue)" stroke="#D4AF37" stroke-width="1.5"/>
  <path d="M38 18 C36 26 38 36 34 45 C32 49 26 53 23 51 C21 49 22 44 26 38 C30 30 31 22 34 18 Z" fill="url(#chilliRed)" stroke="#F59E0B" stroke-width="1"/>
  <path d="M35 24 C36 30 34 38 30 43" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" opacity="0.4" fill="none"/>
  <path d="M34 18 C35 15 35 11 38 9" stroke="#D4AF37" stroke-width="2" stroke-linecap="round" fill="none"/>
  <path d="M32 19 L36 17 L38 21 L34 21 Z" fill="#D4AF37" stroke="#FEF08A" stroke-width="0.5"/>
</svg>""",

    "soil_probe.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="probeGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD700" />
      <stop offset="100%" stop-color="#D4AF37" />
    </linearGradient>
    <linearGradient id="probeBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="url(#probeBlue)" stroke="#D4AF37" stroke-width="1.5"/>
  <path d="M28 16 L36 16 L36 24 L44 38 C46 42 43 47 38 47 L26 47 C21 47 18 42 20 38 L28 24 Z" fill="#1E293B" stroke="#D4AF37" stroke-width="2"/>
  <path d="M23 37 L41 37 L43 41 C44 44 42 46 38 46 L26 46 C22 46 20 44 21 41 Z" fill="url(#probeGold)"/>
  <line x1="30" y1="28" x2="34" y2="28" stroke="#FFFFFF" stroke-width="1" opacity="0.7"/>
  <line x1="29" y1="32" x2="35" y2="32" stroke="#FFFFFF" stroke-width="1" opacity="0.7"/>
  <path d="M42 14 L49 21 L35 35 L32 32 Z" fill="#FEF08A" stroke="#CA8A04" stroke-width="1"/>
  <circle cx="51" cy="12" r="2.5" fill="#D4AF37" stroke="#FFFFFF" stroke-width="1"/>
</svg>""",

    "crop_doctor_shield.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="shieldGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD700" />
      <stop offset="100%" stop-color="#D4AF37" />
    </linearGradient>
    <linearGradient id="shieldNavy" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <path d="M32 8 C44 12 50 14 50 26 C50 42 38 52 32 56 C26 52 14 42 14 26 C14 14 20 12 32 8 Z" fill="url(#shieldNavy)" stroke="url(#shieldGold)" stroke-width="2.5"/>
  <path d="M32 20 C24 20 22 28 26 36 C29 42 32 46 32 46 C32 46 35 42 38 36 C42 28 40 20 32 20 Z" fill="url(#shieldGold)"/>
  <path d="M32 24 L32 44 M32 30 L28 27 M32 35 L36 32 M32 39 L29 37" stroke="#0B192C" stroke-width="1.2" stroke-linecap="round"/>
</svg>""",

    "navbar_emblem.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="none">
  <defs>
    <linearGradient id="navGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFDF78" />
      <stop offset="50%" stop-color="#D4AF37" />
      <stop offset="100%" stop-color="#AA7C11" />
    </linearGradient>
    <linearGradient id="navNavy" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3E62" />
      <stop offset="100%" stop-color="#0B192C" />
    </linearGradient>
  </defs>
  <rect width="48" height="48" rx="12" fill="url(#navNavy)" stroke="url(#navGold)" stroke-width="2"/>
  <!-- Two crossing golden sheaves and central sprouting leaf -->
  <path d="M24 38 C24 26 24 16 24 10" stroke="url(#navGold)" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M24 24 C18 20 16 14 24 12" fill="url(#navGold)"/>
  <path d="M24 24 C30 20 32 14 24 12" fill="url(#navGold)"/>
  <path d="M24 32 C17 28 15 22 24 20" fill="url(#navGold)"/>
  <path d="M24 32 C31 28 33 22 24 20" fill="url(#navGold)"/>
  <circle cx="24" cy="9" r="2.5" fill="#FFFFFF"/>
</svg>"""
}

if __name__ == "__main__":
    for name, content in svgs.items():
        p = os.path.join(svg_dir, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Generated: {name}")
