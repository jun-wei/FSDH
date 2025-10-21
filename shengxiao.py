# zodiac_compatibility.py

from datas import shengxiaos, zhi_atts

def get_zodiac_attribute(zodiac, attribute):
    return zhi_atts[zodiac][attribute]

def get_compatible_zodiacs(zodiac):
    compatible_zodiacs = {
        '?': get_zodiac_attribute(zodiac, '?'),
        '?': get_zodiac_attribute(zodiac, '?'),
        '?': get_zodiac_attribute(zodiac, '?'),
    }
    return compatible_zodiacs

def get_incompatible_zodiacs(zodiac):
    incompatible_zodiacs = {
        '?': get_zodiac_attribute(zodiac, '?'),
        '?': get_zodiac_attribute(zodiac, '?'),
        '??': get_zodiac_attribute(zodiac, '??'),
        '?': get_zodiac_attribute(zodiac, '?'),
        '?': get_zodiac_attribute(zodiac, '?'),
    }
    return incompatible_zodiacs

def calculate_zodiac_compatibility(shengxiao):
    if shengxiao not in shengxiaos.inverse:
        return None

    zodiac = shengxiaos.inverse[shengxiao]
    compatible_zodiacs = get_compatible_zodiacs(zodiac)
    incompatible_zodiacs = get_incompatible_zodiacs(zodiac)

    return {
        'compatible_zodiacs': compatible_zodiacs,
        'incompatible_zodiacs': incompatible_zodiacs,
    }

# Example usage:
shengxiao = '?'
result = calculate_zodiac_compatibility(shengxiao)
if result:
    print('Compatible zodiacs:')
    for attribute, zodiacs in result['compatible_zodiacs'].items():
        print(f'{attribute}: {", ".join([shengxiaos[zodiac] for zodiac in zodiacs])}')

    print('Incompatible zodiacs:')
    for attribute, zodiacs in result['incompatible_zodiacs'].items():
        print(f'{attribute}: {", ".join([shengxiaos[zodiac] for zodiac in zodiacs])}')
