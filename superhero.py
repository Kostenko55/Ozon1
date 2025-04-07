import requests

def get_tallest_hero(gender, work):
    try:
        response = requests.get('https://akabab.github.io/superhero-api/api/all.json')
        response.raise_for_status()
        heroes = response.json()
    except (requests.RequestException, ValueError):
        return None

    filtered_heroes = []
    for hero in heroes:
        # Check gender
        hero_gender = hero.get('appearance', {}).get('gender', '').lower()
        if hero_gender != gender.lower():
            continue

        # Check work
        occupation = hero.get('work', {}).get('occupation', '').strip()
        if work:
            if not occupation or occupation == '-':
                continue
        else:
            if occupation and occupation != '-':
                continue

        # Get height
        try:
            height_str = hero['appearance']['height'][1]
            height_cm = int(height_str.replace(' cm', ''))
        except (KeyError, IndexError, ValueError):
            continue

        filtered_heroes.append((hero, height_cm))

    if not filtered_heroes:
        return None

    tallest_hero = max(filtered_heroes, key=lambda x: x[1])
    return tallest_hero[0]