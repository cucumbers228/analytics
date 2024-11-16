import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
    
class Person:
    def __init__(self, cards_spread):
        """
        Инициализация объекта.
        :param cards_spread: Список из трех объектов TarotCard (расклад).
        """
    
        self.card1 = cards_spread[0]  
        self.card2 = cards_spread[1]  
        self.card3 = cards_spread[2]  

    def __repr__(self):
        return (f"card1={self.card1}, card2={self.card2}, card3={self.card3})")

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
    card3_number = card3_number % 22 
    card3 = cards_df[cards_df['number'] == card3_number].iloc[0]
    
    return [
        TarotCard(name=card1["name"], number=card1["number"], url='/Users/cylimka/git/toro/cards/' + card1["img"]),
        TarotCard(name=card2["name"], number=card2["number"]),
        TarotCard(name=card3["name"], number=card3["number"]),
    ]

def show_card_image(image_path):
    """
    Отображает изображение карты по указанному пути.
    :param image_path: Путь к изображению карты.
    """
    img = mpimg.imread(image_path)  
    plt.imshow(img)  
    plt.axis('off')  
    plt.title("Обложка карты")  
    plt.show() 
    
cards_df = load_cards_to_dataframe('/Users/cylimka/git/toro/tarot-images.json')

first_person = Person(calculate_three_card_spread('2000-05-30', cards_df))

show_card_image(first_person.card1.url)