def extract_year(group_name: str) -> int:
    # Извлекаем год из названия группы и преобразуем его в полный год
    year_part = group_name[1:3]  # Берем символы с 1 по 2
    return int(year_part) + 2000  # Преобразуем в полный год