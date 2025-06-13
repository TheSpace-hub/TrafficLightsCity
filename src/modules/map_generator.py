from typing import TYPE_CHECKING
from src.sprites import TileTexture


class MapGenerator:
    @classmethod
    def generate_map(cls) -> dict[tuple[int, int], TileTexture]:
        field: dict[tuple[int, int], TileTexture] = {}

        size: tuple[int, int] = (30, 30)
        for x in range(size[0]):
            for y in range(size[1]):
                field[(x, y)] = TileTexture.GRASS
        field[(size[0] // 2, size[1] // 2)] = TileTexture.ASPHALT

        return field
