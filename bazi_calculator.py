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

    def get_pillar(self, index):
        stem = self.heavenly_stems[index % 10]
        branch = self.earthly_branches[index % 12]
        return f"{stem[0]}{branch[0]}", stem[1], branch[1]

    def calculate_bazi(self, year, month, day, hour, minute):
        # Simplified BaZi computation using cyclical indexes
        year_index = (year - 4) % 60
        month_index = (year_index * 12 + month) % 60
        day_index = (year_index * 30 + day) % 60
        hour_index = (year_index * 24 + hour) % 60

        year_pillar, y_s, y_b = self.get_pillar(year_index)
        month_pillar, m_s, m_b = self.get_pillar(month_index)
        day_pillar, d_s, d_b = self.get_pillar(day_index)
        hour_pillar, h_s, h_b = self.get_pillar(hour_index)

        pillars = {
            "year_pillar": year_pillar,
            "month_pillar": month_pillar,
            "day_pillar": day_pillar,
            "hour_pillar": hour_pillar
        }

        scores = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        for e in [y_s, y_b, m_s, m_b, d_s, d_b, h_s, h_b]:
            scores[e] += 1

        ranked, missing, strategies = self.rank_five_elements(scores)

        return {
            "bazi": pillars,
            "five_elements_scores": scores,
            "ranked_elements": ranked,
            "weak_elements": missing,
            "balance_strategies": strategies
        }

    # --- Core Element Ranking Logic ---
    def rank_five_elements(self, scores):
        elements_scores = list(scores.items())
        ranked_elements = sorted(elements_scores, key=lambda x: x[1], reverse=True)
        total_score = sum(score for _, score in ranked_elements)
        average_score = total_score / 5

        # Determine missing or weak elements
        missing_elements = [e for e, v in ranked_elements if v <= math.floor(average_score * 0.6)]

        element_relationships = {
            '金': {'generates': '水', 'controls': '木', 'generated_by': '土', 'controlled_by': '火'},
            '木': {'generates': '火', 'controls': '土', 'generated_by': '水', 'controlled_by': '金'},
            '水': {'generates': '木', 'controls': '火', 'generated_by': '金', 'controlled_by': '土'},
            '火': {'generates': '土', 'controls': '金', 'generated_by': '木', 'controlled_by': '水'},
            '土': {'generates': '金', 'controls': '水', 'generated_by': '火', 'controlled_by': '木'}
        }

        strategies = self.balance_elements(scores, missing_elements, element_relationships)
        ranked_output = [{"element": e, "score": s} for e, s in ranked_elements]
        return ranked_output, missing_elements, strategies

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


def calculate_bazi(year, month, day, hour, minute):
    calculator = BaziCalculator()
    return calculator.calculate_bazi(year, month, day, hour, minute)
