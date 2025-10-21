# bazi_calculator.py

from name_analyzer import NameAnalyzer

class BaziCalculator:
    def __init__(self):
        self.name_analyzer = NameAnalyzer()

    def calculate_bazi(self, year, month, day, hour, surname, csv_path, best_elements=None):
        bazi = {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour
        }

        best_elements = best_elements or ["Wood", "Fire", "Earth", "Metal", "Water"]
        character_data, surname_strokes = self.name_analyzer.get_best_characters(
            best_elements, csv_path, surname
        )
        if surname_strokes is None:
            surname_strokes = 0

        auspicious_names = self.name_analyzer.calculate_san_cai_wu_ge(character_data, surname_strokes)
        return {
            "bazi": bazi,
            "surname": surname,
            "surname_strokes": surname_strokes,
            "auspicious_names": auspicious_names
        }

def calculate_bazi(year, month, day, hour, surname, csv_path, best_elements=None):
    calculator = BaziCalculator()
    return calculator.calculate_bazi(year, month, day, hour, surname, csv_path, best_elements)
