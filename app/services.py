from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageOps


class ImageService:
    def __init__(self, resources_dir: Path) -> None:
        self.resources_dir = resources_dir
        self.product_dir = resources_dir / 'images' / 'products'
        self.product_dir.mkdir(parents=True, exist_ok=True)
        self.placeholder_path = resources_dir / 'images' / 'picture.png'

    def resolve_image(self, image_path: str | None) -> Path:
        if not image_path:
            return self.placeholder_path
        candidate = Path(image_path)
        if candidate.is_absolute() and candidate.exists():
            return candidate
        relative_candidate = self.resources_dir / image_path
        if relative_candidate.exists():
            return relative_candidate
        product_candidate = self.product_dir / Path(image_path).name
        if product_candidate.exists():
            return product_candidate
        return self.placeholder_path

    def save_product_image(self, source_path: Path) -> str:
        output_name = f'{uuid4().hex}.png'
        output_path = self.product_dir / output_name
        with Image.open(source_path) as image:
            prepared = ImageOps.contain(image.convert('RGB'), (300, 200))
            canvas = Image.new('RGB', (300, 200), 'white')
            x = (300 - prepared.width) // 2
            y = (200 - prepared.height) // 2
            canvas.paste(prepared, (x, y))
            canvas.save(output_path, format='PNG')
        return str(Path('images') / 'products' / output_name)

    def delete_if_managed(self, image_path: str | None) -> None:
        if not image_path:
            return
        candidate = self.resources_dir / image_path
        if candidate.exists() and self.product_dir in candidate.parents:
            candidate.unlink(missing_ok=True)
