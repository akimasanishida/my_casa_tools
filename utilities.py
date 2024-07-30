import math
import os

unitConvDict = {
    ('rad', 'rad'): 1,
    ('arcsec', 'arcsec'): 1,
    ('rad', 'arcsec'): (3600 * 180) / math.pi,
    ('arcsec', 'rad'): math.pi / (3600 * 180),
}

unitDict = {
    'rad': '',
    'arcsec': '"'
}

siPrefixDict = {
    'peta': { 'symbol': 'P', 'base10': 1e-15 },
    'tera': { 'symbol': 'T', 'base10': 1e-12 },
    'giga': { 'symbol': 'G', 'base10': 1e-9 },
    'mega': { 'symbol': 'M', 'base10': 1e-6 },
    'kilo': { 'symbol': 'k', 'base10': 1e-3 },
    'hecto': { 'symbol': 'h', 'base10': 1e-2 },
    'deca': { 'symbol': 'da', 'base10': 1e-1 },
    'None': { 'symbol': '', 'base10': 1 },
    'deci': { 'symbol': 'd', 'base10': 1e1 },
    'centi': { 'symbol': 'c', 'base10': 1e2 },
    'milli': { 'symbol': 'm', 'base10': 1e3 },
    'micro': { 'symbol': 'μ', 'symbol_alt': 'u', 'base10': 1e6 },
    'nano': { 'symbol': 'n', 'base10': 1e9 },
    'pico': { 'symbol': 'p', 'base10': 1e12 },
}

def get_si_prefix_symbol(prefix: str) -> str:
    """
    Returns the SI prefix symbol for a given prefix string.

    Args:
        prefix (str): The SI prefix string.

    Returns:
        str: The symbol associated with the given prefix.
    """
    try :
        return siPrefixDict[prefix]['symbol']
    except KeyError:
        return siPrefixDict['None']['symbol']

def get_si_prefix_base10(prefix: str) -> float:
    """
    Returns the base 10 multiplier for a given SI prefix string.

    Args:
        prefix (str): The SI prefix string.

    Returns:
        float: The base 10 multiplier associated with the given prefix.
    """
    try :
        return siPrefixDict[prefix]['base10']
    except KeyError:
        return siPrefixDict['None']['base10']

# def get_pret_dir_name(dir: str) -> str:
#     """
#     Returns the last component of a directory path without trailing slashes.

#     Args:
#         dir (str): The directory path.

#     Returns:
#         str: The last component of the directory path.
#     """
#     return os.path.split(dir.rstrip('/'))[1]
