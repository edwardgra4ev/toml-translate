from pathlib import Path

import argostranslate.translate
from tomlkit import dumps, parse

LIST_KEY = ["display_name", "description"]
SOURCE_ROOT = Path("./StreamingAssets")
TARGET_ROOT = Path("./StreamingAssets_ru")

cache = {}


def translate(text: str) -> str:
    if not text.strip():
        return text

    if text in cache:
        return cache[text]

    translated = argostranslate.translate.translate(
        text,
        "en",
        "ru",
    )

    cache[text] = translated

    print(f"EN: {text}")
    print(f"RU: {translated}")
    print()

    return translated


def walk(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in LIST_KEY and isinstance(value, str):
                node[key] = translate(value)
            else:
                walk(value)

    elif isinstance(node, list):
        for item in node:
            walk(item)


def process_file(path: Path):
    print(f"Обработка {path}")

    with path.open("r", encoding="utf-8-sig") as f:
        doc = parse(f.read())

    walk(doc)

    relative_path = path.relative_to(SOURCE_ROOT)

    target_path = TARGET_ROOT / relative_path

    target_path.parent.mkdir(parents=True, exist_ok=True)

    with target_path.open("w", encoding="utf-8-sig") as f:
        f.write(dumps(doc))


def main():
    files = list(SOURCE_ROOT.rglob("*.toml"))

    print(f"Найдено {len(files)} TOML файлов")

    for file in files:
        process_file(file)


if __name__ == "__main__":
    main()
