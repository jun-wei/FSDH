# bazi_calculator.py
import math

class BaziCalculator:
    def __init__(self):
        self.heavenly_stems = [
            ("甲", "木"), ("乙", "木"), ("丙", "火"), ("丁", "火"),
            ("戊", "土"), ("己", "土"), ("庚", "金"), ("辛", "金"),
            ("壬", "水"), ("癸", "水")
        ]
        self.earthly_branches = [
            ("子", "水"), ("丑", "土"), ("寅", "木"), ("卯", "木"),
            ("辰", "土"), ("巳", "火"), ("午", "火"), ("未", "土"),
            ("申", "金"), ("酉", "金"), ("戌", "土"), ("亥", "水")
        ]

        # English meaning and advice for each element
        self.element_meanings = {
            "木": {
                "name": "Wood",
                "traits": "Growth, creativity, expansion, leadership, and flexibility.",
                "advice": "You are visionary and ambitious. Stay grounded to avoid overextending."
            },
            "火": {
                "name": "Fire",
                "traits": "Passion, energy, motivation, inspiration, and visibility.",
                "advice": "You are charismatic and expressive. Balance intensity with patience."
            },
            "土": {
                "name": "Earth",
                "traits": "Stability, reliability, nurturing, practicality, and organization.",
                "advice": "You are dependable and thoughtful. Avoid being overly cautious or stagnant."
            },
            "金": {
                "name": "Metal",
                "traits": "Discipline, strength, precision, logic, and determination.",
                "advice": "You are principled and strong-willed. Loosen rigidity with empathy."
            },
            "水": {
                "name": "Water",
                "traits": "Wisdom, intuition, adaptability, and communication.",
                "advice": "You are reflective and insightful. Avoid overthinking or hesitation."
            }
        }

    # ------------------------------
    # Core BaZi Logic
    # ------------------------------
    def get_pillar(self, index):
        stem = self.heavenly_stems[index % 10]
        branch = self.earthly_branches[index % 12]
        return f"{stem[0]}{branch[0]}", stem[1], branch[1]

    def calculate_bazi(self, year, month, day, hour, minute):
        # Use lunar_python for accurate GanZhi calculation
        lunar = Lunar.fromYmdHms(year, month, day, hour, minute, 0)
        eight_char = lunar.getEightChar()

        year_pillar = eight_char.getYear()
        month_pillar = eight_char.getMonth()
        day_pillar = eight_char.getDay()
        hour_pillar = eight_char.getTime()

        pillars = {
            "year_pillar": year_pillar,
            "month_pillar": month_pillar,
            "day_pillar": day_pillar,
            "hour_pillar": hour_pillar
        }

        # Calculate element scores from the Heavenly Stems and Earthly Branches
        all_chars = [
            year_pillar[0], year_pillar[1],
            month_pillar[0], month_pillar[1],
            day_pillar[0], day_pillar[1],
            hour_pillar[0], hour_pillar[1]
        ]

        # Element mapping
        gan_element_map = {
            "甲": "木", "乙": "木",
            "丙": "火", "丁": "火",
            "戊": "土", "己": "土",
            "庚": "金", "辛": "金",
            "壬": "水", "癸": "水"
        }
        zhi_element_map = {
            "子": "水", "丑": "土", "寅": "木", "卯": "木",
            "辰": "土", "巳": "火", "午": "火", "未": "土",
            "申": "金", "酉": "金", "戌": "土", "亥": "水"
        }

        # Combine and count
        scores = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        for ch in all_chars:
            if ch in gan_element_map:
                scores[gan_element_map[ch]] += 1
            elif ch in zhi_element_map:
                scores[zhi_element_map[ch]] += 1

        ranked, missing, strategies, classification, interpretation = self.rank_five_elements(scores)

        return {
            "bazi": pillars,
            "classification": classification,
            "five_elements_scores": scores,
            "ranked_elements": ranked,
            "weak_elements": missing,
            "balance_strategies": strategies,
            "interpretation": interpretation
        }

    # ------------------------------
    # Element Ranking and Analysis
    # ------------------------------
    def rank_five_elements(self, scores):
        elements_scores = list(scores.items())
        ranked_elements = sorted(elements_scores, key=lambda x: x[1], reverse=True)
        total_score = sum(score for _, score in ranked_elements)
        average_score = total_score / 5 if total_score > 0 else 0

        # Normalize to percentage for charting
        percentages = {e: round((v / total_score) * 100, 2) if total_score > 0 else 0 for e, v in scores.items()}

        missing_elements = [e for e, v in ranked_elements if v <= math.floor(average_score * 0.6)]

        element_relationships = {
            '金': {'generates': '水', 'controls': '木', 'generated_by': '土', 'controlled_by': '火'},
            '木': {'generates': '火', 'controls': '土', 'generated_by': '水', 'controlled_by': '金'},
            '水': {'generates': '木', 'controls': '火', 'generated_by': '金', 'controlled_by': '土'},
            '火': {'generates': '土', 'controls': '金', 'generated_by': '木', 'controlled_by': '水'},
            '土': {'generates': '金', 'controls': '水', 'generated_by': '火', 'controlled_by': '木'}
        }

        strategies = self.balance_elements(scores, missing_elements, element_relationships)
        classification = self.classify_balance(percentages)
        interpretation = self.interpret_elements(classification)

        ranked_output = [{"element": e, "score": s} for e, s in ranked_elements]
        return ranked_output, missing_elements, strategies, classification, interpretation

    def balance_elements(self, scores, missing_elements, element_relationships):
        strategies = []
        for element in missing_elements:
            if element not in element_relationships:
                continue
            gen = element_relationships[element]['generated_by']
            if scores.get(gen, 0) >= 2:
                strategies.append(f"Strengthen {element} by enhancing {gen} ({gen}生{element})")
            else:
                strategies.append(f"Directly strengthen {element} through {element_relationships[element]['generates']} energy")
            ctrl = element_relationships[element]['controlled_by']
            strategies.append(f"Reduce excess influence from {ctrl} if too strong ({ctrl}克{element})")
        return strategies

    def classify_balance(self, percentages):
        dominant = max(percentages, key=percentages.get)
        weakest = min(percentages, key=percentages.get)
        dom_pct = percentages[dominant]
        weak_pct = percentages[weakest]

        if dom_pct >= 30:
            summary = f"{dominant}-dominant chart ({dominant}旺格局)"
        elif weak_pct <= 10:
            summary = f"{weakest}-weak chart ({weakest}弱格局)"
        elif all(15 <= p <= 25 for p in percentages.values()):
            summary = "Balanced chart (五行均衡)"
        else:
            summary = "Mixed balance chart (中庸格局)"

        return {
            "percentages": percentages,
            "dominant": dominant,
            "weakest": weakest,
            "summary": summary
        }

    def interpret_elements(self, classification):
        dominant = classification["dominant"]
        weakest = classification["weakest"]
        dom_meaning = self.element_meanings[dominant]
        weak_meaning = self.element_meanings[weakest]

        return {
            "dominant_element": {
                "element": dominant,
                "english_name": dom_meaning["name"],
                "traits": dom_meaning["traits"],
                "advice": dom_meaning["advice"]
            },
            "weakest_element": {
                "element": weakest,
                "english_name": weak_meaning["name"],
                "traits": weak_meaning["traits"],
                "advice": f"You need more {weak_meaning['name']} energy. {weak_meaning['advice']}"
            }
        }

def calculate_bazi(year, month, day, hour, minute):
    calculator = BaziCalculator()
    return calculator.calculate_bazi(year, month, day, hour, minute)