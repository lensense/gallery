import os
from pathlib import Path
from PIL import Image

# Папка с изображениями
base_image_dir = Path("images")

# Путь для index.html
output_html_path = Path("index.html")

# Собираем все папки-даты
date_dirs = sorted([d for d in base_image_dir.iterdir() if d.is_dir()])

html_sections = []

for date_dir in date_dirs:
    date_str = date_dir.name
    section = f'<section>\n  <h2>{date_str}</h2>\n  <div class="gallery">\n'
    
    for img_file in sorted(date_dir.glob("*")):
        if img_file.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
            continue
        try:
            with Image.open(img_file) as img:
                width, height = img.size
        except Exception:
            width, height = 1600, 1067  # fallback
        
        img_path = f"{date_dir}/{img_file.name}".replace("\\", "/")
        section += (
            f'    <a href="{img_path}" data-pswp-width="{width}" data-pswp-height="{height}" target="_blank">\n'
            f'      <img src="{img_path}" alt="">\n'
            f'    </a>\n'
        )
    
    section += "  </div>\n</section>\n"
    html_sections.append(section)

# HTML-шаблон с Masonry и PhotoSwipe
html_template = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Gallery</title>
  <link rel="stylesheet" href="https://unpkg.com/photoswipe@5/dist/photoswipe.css" />
  <style>
    body {{
      font-family: sans-serif;
      background: #111;
      color: #eee;
      padding: 20px;
    }}
    h2 {{
      border-bottom: 1px solid #444;
      padding-bottom: 5px;
    }}
    .gallery {{
      margin-top: 10px;
    }}
    .gallery a {{
      display: block;
      width: 200px;
      margin-bottom: 10px;
      border-radius: 8px;
      overflow: hidden;
      box-sizing: border-box;
      cursor: pointer;
      transition: transform 0.2s ease;
    }}
    .gallery a:hover {{
      transform: scale(1.05);
      z-index: 10;
      position: relative;
    }}
    .gallery img {{
      width: 100%;
      height: auto;
      display: block;
      border-radius: 8px;
    }}
  </style>
</head>
<body>

<h1>Lens gallery</h1>

{''.join(html_sections)}

<script src="https://unpkg.com/masonry-layout@4/dist/masonry.pkgd.min.js"></script>
<script type="module">
  import PhotoSwipeLightbox from 'https://unpkg.com/photoswipe@5/dist/photoswipe-lightbox.esm.js';

  document.querySelectorAll('.gallery').forEach(galleryEl => {{
    new Masonry(galleryEl, {{
      itemSelector: 'a',
      gutter: 10,
      fitWidth: true,
    }});
  }});

  const lightbox = new PhotoSwipeLightbox({{
    gallery: '.gallery',
    children: 'a',
    pswpModule: () => import('https://unpkg.com/photoswipe@5/dist/photoswipe.esm.js')
  }});
  lightbox.init();
</script>

</body>
</html>
"""

with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(html_template)
print("Галерея успешно сгенерирована!")
