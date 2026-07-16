import argostranslate.package

print("Обновление индекса...")
argostranslate.package.update_package_index()

packages = argostranslate.package.get_available_packages()

for p in packages:
    print(f"{p.from_code} -> {p.to_code}")

package = next(p for p in packages if p.from_code == "en" and p.to_code == "ru")

print("Скачивание...")
download_path = package.download()

print("Установка...")
argostranslate.package.install_from_path(download_path)

print("Готово!")
