from superhero import get_tallest_hero

# Пример вызова функции
result = get_tallest_hero('male', True)
print(f"Самый высокий герой: {result['name']}") if result else print("Не найдено")