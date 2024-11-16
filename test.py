import pandas as pd
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import Counter

class TarotCard:
    """
    Класс для представления карты Таро.
    """
    def __init__(self, name, number, meanings_shadow=None, meanings_light=None, url=None):
        self.name = name
        self.number = number
        self.url = url
        self.meanings_shadow = meanings_shadow
        self.meanings_light = meanings_light
    def __repr__(self):
        return f"TarotCard(name='{self.name}', number={self.number})"

def load_cards_to_dataframe(file_path):
    """
    Загружает карты из JSON-файла и возвращает данные в формате DataFrame.
    :param file_path: Путь к JSON-файлу.
    :return: DataFrame с данными о картах.
    """
    data = pd.read_json(file_path)
    cards_data = pd.json_normalize(data['cards'])
    cards_data['number'] = cards_data['number'].astype(int)
    return cards_data

def generate_birthdate(start_year=1924, end_year=2024):
    """
    Генерирует случайную дату рождения в заданном диапазоне лет.
    :param start_year: Начальный год диапазона (по умолчанию 1900).
    :param end_year: Конечный год диапазона (по умолчанию 2023).
    :return: Строка с датой рождения в формате YYYY-MM-DD.
    """
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    
    return random_date.strftime("%Y-%m-%d")

def raspr_three_positions(n=10000):
    """
    Генерирует распределение для 3 типов карт в раскладе.
    :param n: Количество генераций дат для анализа распределения.
    """
    position1_cards = []
    position2_cards = []
    position3_cards = []

    for _ in range(n):
        birthdate = generate_birthdate()
        cards_spread = calculate_three_card_spread(birthdate, cards)
        
        position1_cards.append(cards_spread[0].number)
        position2_cards.append(cards_spread[1].number)
        position3_cards.append(cards_spread[2].number)

    frequency1 = Counter(position1_cards)
    frequency2 = Counter(position2_cards)
    frequency3 = Counter(position3_cards)

    plt.bar(frequency1.keys(), frequency1.values())
    plt.title("Распределение Аркана 1-й позиции (Базовый архетип)")
    plt.xlabel("Число")
    plt.ylabel("Частота")
    plt.xticks(range(0, 22))  
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    plt.bar(frequency2.keys(), frequency2.values())
    plt.title("Распределение Аркана 2-й позиции (Навыки и развитие)")
    plt.xlabel("Число")
    plt.ylabel("Частота")
    plt.xticks(range(0, 22)) 
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    plt.bar(frequency3.keys(), frequency3.values())
    plt.title("Распределение Аркана 3-й позиции (Страхи и комплексы)")
    plt.xlabel("Число")
    plt.ylabel("Частота")
    plt.xticks(range(0, 22))  
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def calculate_three_card_spread(birthdate, cards_df):
    """
    Рассчитывает расклад по 3 картам на основе даты рождения.
    :param birthdate: Дата рождения в формате "YYYY-MM-DD".
    :param cards_df: DataFrame с данными о картах.
    :return: Список из 3 объектов TarotCard.
    """
    year, month, day = map(int, birthdate.split("-"))
    
    card1_number = day if day <= 21 else day - 22
    card1 = cards_df[cards_df['number'] == card1_number].iloc[0]
    
    card2_number = month if month <= 21 else month - 22
    card2 = cards_df[cards_df['number'] == card2_number].iloc[0]
    
    card3_number = card1_number + card2_number
    card3_number = card3_number % 21 
    card3 = cards_df[cards_df['number'] == card3_number].iloc[0]
    
    return [
        TarotCard(name=card1["name"], number=card1["number"]),
        TarotCard(name=card2["name"], number=card2["number"]),
        TarotCard(name=card3["name"], number=card3["number"]),
    ]

def one_choise(date):
    birthdate = date  
    three_card_spread = calculate_three_card_spread(birthdate, cards)
    print(f"Расклад по 3 картам для даты рождения {birthdate}:")
    for i, card in enumerate(three_card_spread, start=1):
        print(f"Аркан {i}-й позиции: {card}")
    
cards = load_cards_to_dataframe('/Users/cylimka/git/toro/tarot-images.json')
one_choise('2003-05-03')
