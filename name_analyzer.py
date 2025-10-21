# name_analyzer.py

import collections
import csv

class NameAnalyzer:
    def __init__(self):
        self.lucky_numbers = {1, 3, 5, 6, 7, 8, 11, 13, 15, 16, 17, 18, 21, 23, 24, 25, 29, 31, 32, 33,
                             35, 37, 39, 41, 45, 47, 48, 52, 57, 61, 63, 65, 67, 68, 81}

    def calculate_structure(self, strokes):
        return strokes % 81

    def is_lucky(self, num):
        return num in self.lucky_numbers

    def get_best_characters(self, best_elements, csv_path, surname):
        result = {element: [] for element in best_elements}
        surname_strokes = None

        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row if it exists

            for row in csv_reader:
                if len(row) >= 4:  # Ensure the row has at least 4 columns
                    element = row[3]  # Assuming the element is in the 4th column
                    if element in best_elements:
                        result[element].append({
                            'character': row[1],  # 2nd column
                            'num': int(row[2]),   # 3rd column, convert to integer for proper sorting
                            'element': row[3]     # 4th column
                        })
                    if row[1] == surname:  # Ensure the row has at least 4 columns
                        surname_strokes = int(row[2])  # Assuming the stroke is in the 2rd column

        # Sort the results for each element
        for element in result:
            result[element] = sorted(result[element], key=lambda x: (x['num'], x['character']))

        return result, surname_strokes

    def calculate_san_cai_wu_ge(self, character_data, surname_strokes, desired_element=None):
        auspicious_combinations = []
        lucky_chars = {}  # Store characters for all 5 格 results with a lucky number

        # Generate single-character names
        for element, chars in character_data.items():
            if desired_element and element != desired_element:
                continue

            for char in chars:
                surname_num = int(surname_strokes)
                char_num = int(char.get('num'))
                # Five Structures calculation (single-character name)
                tian_ge = self.calculate_structure(surname_num + 1)
                ren_ge = self.calculate_structure(surname_num + char_num)
                di_ge = self.calculate_structure(char_num + 1)  # Single name adjustment
                wai_ge = self.calculate_structure(surname_num + 1)
                zong_ge = self.calculate_structure(surname_num + char_num)
                if self.is_lucky(tian_ge) and self.is_lucky(ren_ge) and self.is_lucky(di_ge) and self.is_lucky(wai_ge) and self.is_lucky(zong_ge):
                    auspicious_combinations.append({
                        'name': char['character'],
                        'structure': ('single', tian_ge, ren_ge, di_ge, wai_ge, zong_ge),
                        'elements': [char['element']],
                        'strokes': [char['num']]
                    })

        # Generate two-character names
        for el1, chars1 in character_data.items():
            for el2, chars2 in character_data.items():
                if desired_element and (el1 != desired_element or el2 != desired_element):
                    continue

                for char1 in chars1:
                    for char2 in chars2:
                        surname_num = int(surname_strokes)
                        char_num = int(char1.get('num'))
                        char2_num = int(char2.get('num'))

                        # Five Structures calculation (two-character name)
                        tian_ge = self.calculate_structure(surname_num + 1)
                        ren_ge = self.calculate_structure(surname_num + char_num)
                        di_ge = self.calculate_structure(char_num + char2_num)
                        wai_ge = self.calculate_structure(char2_num + 1)
                        zong_ge = self.calculate_structure(surname_num + char_num + char2_num)
                        if self.is_lucky(ren_ge) and self.is_lucky(di_ge) and self.is_lucky(wai_ge)
