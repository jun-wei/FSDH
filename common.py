"""
common.py
---------
Utility functions for BaZi (Four Pillars of Destiny) calculations.
Handles Yin-Yang, Gan-Zhi relationships, Empty Branch, and Three-Combination checks.

This version is standalone (no external dependencies like datas/ganzhi/sizi).
"""

import datetime
from bidict import bidict

# --------------------------------------------------------
# 1?? Define core data (Heavenly Stems, Earthly Branches)
# --------------------------------------------------------

Gan = ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?']
Zhi = ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?']

# Element mapping
gan5 = {
    '?': 'Wood', '?': 'Wood',
    '?': 'Fire', '?': 'Fire',
    '?': 'Earth', '?': 'Earth',
    '?': 'Metal', '?': 'Metal',
    '?': 'Water', '?': 'Water'
}

zhi5 = {
    '?': {'?': 1},
    '?': {'?': 1, '?': 1, '?': 1},
    '?': {'?': 1, '?': 1, '?': 1},
    '?': {'?': 1},
    '?': {'?': 1, '?': 1, '?': 1},
    '?': {'?': 1, '?': 1, '?': 1},
    '?': {'?': 1, '?': 1},
    '?': {'?': 1, '?': 1, '?': 1},
    '?': {'?': 1, '?': 1},
    '?': {'?': 1},
    '?': {'?': 1, '?': 1, '?': 1},
    '?': {'?': 1, '?': 1}
}

# Ten Deities - simplified representation
ten_deities = {
    gan: {'?': Gan[(Gan.index(gan) + 5) % 10],
          '?': Gan[(Gan.index(gan) + 6) % 10]}
    for gan in Gan
}

# ?? ("Empty Branch") mapping - simplified
empties = {
    '??': ['?', '?'],
    '??': ['?', '?'],
    '??': ['?', '?'],
    '??': ['?', '?'],
    '??': ['?', '?'],
    '??': ['?', '?'],
    '??': ['?', '?'],
    '??': ['?', '?'],
    '??': ['?', '?'],
    '??': ['?', '?']
}

# ??? relationships (Three-Combination)
hes = bidict({
    '??': '?', '??': '?', '??': '?',   # Water Trine
    '??': '?', '??': '?', '??': '?',   # Fire Trine
    '??': '?', '??': '?', '??': '?',   # Wood Trine
    '??': '?', '??': '?', '??': '?'    # Metal Trine
})

# --------------------------------------------------------
# 2?? Core Relationship Functions
# --------------------------------------------------------

def check_gan(gan, gans):
    """Check if a gan has any relationships with other gans."""
    result = ''
    if ten_deities[gan]['?'] in gans:
        result += f"?{ten_deities[gan]['?']}"
    if ten_deities[gan]['?'] in gans:
        result += f"?{ten_deities[gan]['?']}"
    return result


def yinyang(item):
    """Determine Yin (-) or Yang (+) nature of a Gan/Zhi."""
    if item in Gan:
        return '+' if Gan.index(item) % 2 == 0 else '-'
    elif item in Zhi:
        return '+' if Zhi.index(item) % 2 == 0 else '-'
    else:
        return '?'


def yinyangs(zhis):
    """Check if four pillars are all Yin or all Yang."""
    result = [yinyang(z) for z in zhis]
    if set(result) == {'+'}:
        print("???? (All Yang)")
    elif set(result) == {'-'}:
        print("???? (All Yin)")
    else:
        print("???? (Balanced)")


def get_empty(zhu, zhi):
    """Check if a zhi is empty based on pillar."""
    empty = empties.get(zhu, [])
    return "?" if zhi in empty else ""


def get_zhi_detail(zhi, me, multi=1):
    """Return element details of a branch (?) including ten deities."""
    out = ''
    for gan, weight in zhi5.get(zhi, {}).items():
        deity = ten_deities.get(me, {}).get(gan, '')
        out += f"{gan}{gan5.get(gan, '')}{weight * multi}{deity} "
    return out.strip()


def check_gong(zhis, n1, n2, me, hes_map=hes, desc='???'):
    """Check for ??? (three-combination) between two zhis."""
    result = ''
    combo_key = zhis[n1] + zhis[n2]
    if combo_key in hes_map:
        gong = hes_map[combo_key]
        if gong not in zhis:
            result += f"\t{desc}:{zhis[n1]}{zhis[n2]}-{gong} [{get_zhi_detail(gong, me)}]"
    return result

# --------------------------------------------------------
# Example (run standalone)
# --------------------------------------------------------
if __name__ == "__main__":
    gans = ['?', '?', '?', '?']
    zhis = ['?', '?', '?', '?']
    me = '?'

    print("Gan relationships:")
    for g in gans:
        print(f"{g}: {check_gan(g, gans)}")

    print("\nYin/Yang check:")
    yinyangs(zhis)

    print("\nZhi details:")
    for z in zhis:
        print(f"{z}: {get_zhi_detail(z, me)}")

    print("\nGong check example:")
    print(check_gong(zhis, 0, 2, me))
