# common.py

import collections
import pprint
import datetime

from bidict import bidict

from datas import *
from ganzhi import *
from sizi import summarys

def check_gan(gan, gans):
    """Check if a gan has any relationships with other gans"""
    result = ''
    if ten_deities[gan]['?'] in gans:
        result += f"?{ten_deities[gan]['?']}"
    if ten_deities[gan]['?'] in gans:
        result += f"?{ten_deities[gan]['?']}"
    return result

def yinyang(item):
    """Determine the yin/yang nature of an item"""
    if item in Gan:
        return '+' if Gan.index(item) % 2 == 0 else '-'
    else:
        return '+' if Zhi.index(item) % 2 == 0 else '-'

def yinyangs(zhis):
    """Determine the yin/yang nature of a list of zhis"""
    result = [yinyang(zhi) for zhi in zhis]
    if set(result) == {'+'}:
        print("????")
    elif set(result) == {'-'}:
        print("????")

def get_empty(zhu, zhi):
    """Check if a zhi is empty"""
    empty = empties[zhu]
    return "?" if zhi in empty else ""

def get_zhi_detail(zhi, me, multi=1):
    """Get detailed information about a zhi"""
    out = ''
    for gan in zhi5[zhi]:
        out += f"{gan}{gan5[gan]}{zhi5[zhi][gan]*multi}{ten_deities[me][gan]} "
    return out

def check_gong(zhis, n1, n2, me, hes, desc='???'):
    """Check for gong relationships between zhis"""
    result = ''
    if zhis[n1] + zhis[n2] in hes:
        gong = hes[zhis[n1] + zhis[n2]]
        if gong not in zhis:
            result += f"\t{desc}:{zhis[n1]}{zhis[n2]}-{gong}[{get_zhi_detail(gong, me)}]"
    return result
