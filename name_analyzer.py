# name_analyzer.py

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
            next(csv_reader)  # skip header
            for row in csv_reader:
                if len(row) >= 4:
                    element = row[3]
                    if element in best_elements:
                        result[element].append({
                            'character': row[1],
                            'num': int(row[2]),
                            'element': row[3]
                        })
                    if row[1] == surname:
                        surname_strokes = int(row[2])

        # sort characters by strokes then name
        for element in result:
            result[element] = sorted(result[element], key=lambda x: (x['num'], x['character']))

        return result, surname_strokes

    def calculate_san_cai_wu_ge(self, character_data, surname_strokes, desired_element=None):
        auspicious_combinations = []

        # single character names
        for element, chars in character_data.items():
            if desired_element and element != desired_element:
                continue
            for char in chars:
                surname_num = int(surname_strokes)
                char_num = int(char['num'])
                tian_ge = self.calculate_structure(surname_num + 1)
                ren_ge = self.calculate_structure(surname_num + char_num)
                di_ge = self.calculate_structure(char_num + 1)
                wai_ge = self.calculate_structure(surname_num + 1)
                zong_ge = self.calculate_structure(surname_num + char_num)
                if all(self.is_lucky(x) for x in [tian_ge, ren_ge, di_ge, wai_ge, zong_ge]):
                    auspicious_combinations.append({
                        'name': char['character'],
                        'structure': (tian_ge, ren_ge, di_ge, wai_ge, zong_ge),
                        'elements': [char['element']],
                        'strokes': [char_num]
                    })

        # two-character names
        for el1, chars1 in character_data.items():
            for el2, chars2 in character_data.items():
                if desired_element and (el1 != desired_element or el2 != desired_element):
                    continue
                for char1 in chars1:
                    for char2 in chars2:
                        surname_num = int(surname_strokes)
                        char1_num = int(char1['num'])
                        char2_num = int(char2['num'])
                        tian_ge = self.calculate_structure(surname_num + 1)
                        ren_ge = self.calculate_structure(surname_num + char1_num)
                        di_ge = self.calculate_structure(char1_num + char2_num)
                        wai_ge = self.calculate_structure(char2_num + 1)
                        zong_ge = self.calculate_structure(surname_num + char1_num + char2_num)
                        if all(self.is_lucky(x) for x in [ren_ge, di_ge, wai_ge]):
                            auspicious_combinations.append({
                                'name': char1['character'] + char2['character'],
                                'structure': (tian_ge, ren_ge, di_ge, wai_ge, zong_ge),
                                'elements': [char1['element'], char2['element']],
                                'strokes': [char1_num, char2_num]
                            })
        return auspicious_combinations
