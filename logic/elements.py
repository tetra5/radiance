# -*- coding: utf-8 -*-


"""
Created on 13.10.2010

@author: vda
"""


from settings import settings


class ElementNotFound(Exception): pass


ELEMENTS = [
    (1, 'H', 'Hydrogen', u'Водород'),
    (2, 'He', 'Helium', u'Гелий'),
    (3, 'Li', 'Lithium', u'Литий'),
    (4, 'Be', 'Beryllium', u'Бериллий'),
    (5, 'B', 'Boron', u'Бор'),
    (6, 'C', 'Carbon', u'Углерод'),
    (7, 'N', 'Nitrogen', u'Азот'),
    (8, 'O', 'Oxygen', u'Кислород'),
    (9, 'F', 'Fluorine', u'Фтор'),
    (10, 'Ne', 'Neon', u'Неон'),
    (11, 'Na', 'Sodium', u'Натрий'),
    (12, 'Mg', 'Magnesium', u'Магний'),
    (13, 'Al', 'Aluminium', u'Алюминий'),
    (14, 'Si', 'Silicon', u'Кремний'),
    (15, 'P', 'Phosphorus', u'Фосфор'),
    (16, 'S', 'Sulfur', u'Сера'),
    (17, 'Cl', 'Chlorine', u'Хлор'),
    (18, 'Ar', 'Argon', u'Аргон'),
    (19, 'K', 'Potassium', u'Калий'),
    (20, 'Ca', 'Calcium', u'Кальций'),
    (21, 'Sc', 'Scandium', u'Скандий'),
    (22, 'Ti', 'Titanium', u'Титан'),
    (23, 'V', 'Vanadium', u'Ванадий'),
    (24, 'Cr', 'Chromium', u'Хром'),
    (25, 'Mn', 'Manganese', u'Марганец'),
    (26, 'Fe', 'Iron', u'Железо'),
    (27, 'Co', 'Cobalt', u'Кобальт'),
    (28, 'Ni', 'Nickel', u'Никель'),
    (29, 'Cu', 'Copper', u'Медь'),
    (30, 'Zn', 'Zinc', u'Цинк'),
    (31, 'Ga', 'Gallium', u'Галлий'),
    (32, 'Ge', 'Germanium', u'Германий'),
    (33, 'As', 'Arsenic', u'Мышьяк'),
    (34, 'Se', 'Selenium', u'Селен'),
    (35, 'Br', 'Bromine', u'Бром'),
    (36, 'Kr', 'Krypton', u'Криптон'),
    (37, 'Rb', 'Rubidium', u'Рубидий'),
    (38, 'Sr', 'Strontium', u'Стронций'),
    (39, 'Y', 'Yttrium', u'Иттрий'),
    (40, 'Zr', 'Zirconium', u'Цирконий'),
    (41, 'Nb', 'Niobium', u'Ниобий'),
    (42, 'Mo', 'Molybdenum', u'Молибден'),
    (43, 'Tc', 'Technetium', u'Технеций'),
    (44, 'Ru', 'Ruthenium', u'Рутений'),
    (45, 'Rh', 'Rhodium', u'Родий'),
    (46, 'Pd', 'Palladium', u'Палладий'),
    (47, 'Ag', 'Silver', u'Серебро'),
    (48, 'Cd', 'Cadmium', u'Кадмий'),
    (49, 'In', 'Indium', u'Индий'),
    (50, 'Sn', 'Tin', u'Олово'),
    (51, 'Sb', 'Antimony', u'Сурьма'),
    (52, 'Te', 'Tellurium', u'Теллур'),
    (53, 'I', 'Iodine', u'Йод'),
    (54, 'Xe', 'Xenon', u'Ксенон'),
    (55, 'Cs', 'Caesium', u'Цезий'),
    (56, 'Ba', 'Barium', u'Барий'),
    (57, 'La', 'Lanthanum', u'Лантан'),
    (58, 'Ce', 'Cerium', u'Церий'),
    (59, 'Pr', 'Praseodymium', u'Празеодим'),
    (60, 'Nd', 'Neodymium', u'Неодим'),
    (61, 'Pm', 'Promethium', u'Прометий'),
    (62, 'Sm', 'Samarium', u'Самарий'),
    (63, 'Eu', 'Europium', u'Европий'),
    (64, 'Gd', 'Gadolinium', u'Гадолиний'),
    (65, 'Tb', 'Terbium', u'Тербий'),
    (66, 'Dy', 'Dysprosium', u'Диспрозий'),
    (67, 'Ho', 'Holmium', u'Гольмий'),
    (68, 'Er', 'Erbium', u'Эрбий'),
    (69, 'Tm', 'Thulium', u'Тулий'),
    (70, 'Yb', 'Ytterbium', u'Иттербий'),
    (71, 'Lu', 'Lutetium', u'Лютеций'),
    (72, 'Hf', 'Hafnium', u'Гафний'),
    (73, 'Ta', 'Tantalum', u'Танталий'),
    (74, 'W', 'Tungsten', u'Вольфрам'),
    (75, 'Re', 'Rhenium', u'Рений'),
    (76, 'Os', 'Osmium', u'Осмий'),
    (77, 'Ir', 'Iridium', u'Иридий'),
    (78, 'Pt', 'Platinum', u'Платина'),
    (79, 'Au', 'Gold', u'Золото'),
    (80, 'Hg', 'Mercury', u'Ртуть'),
    (81, 'Tl', 'Thallium', u'Таллий'),
    (82, 'Pb', 'Lead', u'Свинец'),
    (83, 'Bi', 'Bismuth', u'Висмут'),
    (84, 'Po', 'Polonium', u'Полоний'),
    (85, 'At', 'Astatine', u'Астат'),
    (86, 'Rn', 'Radon', u'Радон'),
    (87, 'Fr', 'Francium', u'Франций'),
    (88, 'Ra', 'Radium', u'Радий'),
    (89, 'Ac', 'Actinium', u'Актиний'),
    (90, 'Th', 'Thorium', u'Торий'),
    (91, 'Pa', 'Protactinium', u'Протактиний'),
    (92, 'U', 'Uranium', u'Уран'),
    (93, 'Np', 'Neptunium', u'Нептуний'),
    (94, 'Pu', 'Plutonium', u'Плутоний'),
    (95, 'Am', 'Americium', u'Америций'),
    (96, 'Cm', 'Curium', u'Кюрий'),
    (97, 'Bk', 'Berkelium', u'Берклий'),
    (98, 'Cf', 'Californium', u'Калифорний'),
    (99, 'Es', 'Einsteinium', u'Эйнштейний'),
    (100, 'Fm', 'Fermium', u'Фермий'),
    (101, 'Md', 'Mendelevium', u'Менделевий'),
    (102, 'No', 'Nobelium', u'Нобелий'),
    (103, 'Lr', 'Lawrencium', u'Лоуренсий'),
    (104, 'Rf', 'Rutherfordium', u'Резерфордий'),
    (105, 'Db', 'Dubnium', u'Дубний'),
    (106, 'Sg', 'Seaborgium', u'Сиборгий'),
    (107, 'Bh', 'Bohrium', u'Борий'),
    (108, 'Hs', 'Hassium', u'Хассий'),
    (109, 'Mt', 'Meitnerium', u'Мейтнерий'),
    (110, 'Ds', 'Darmstadtium', u'Дармштадтий'),
    (111, 'Rg', 'Roentgenium', u'Рентгений'),
    (112, 'Cn', 'Copernicium', u'Копернеций'),
    (113, 'Uut', 'Ununtrium', u'Унунтрий'),
    (114, 'Uuq', 'Ununquadium', u'Унунквадий'),
    (115, 'Uup', 'Ununpentium', u'Унунпентий'),
    (116, 'Uuh', 'Ununhexium', u'Унунгексий'),
    (117, 'Uus', 'Ununseptium', u'Унунсептий'),
    (118, 'Uuo', 'Ununoctium', u'Унуноктий'),
    ]


def get_element(element):
    """
    >>> get_element('Pb')
    (82, 'Pb', 'Lead', u'\u0421\u0432\u0438\u043d\u0435\u0446')
    
    >>> get_element('Lead')
    (82, 'Pb', 'Lead', u'\u0421\u0432\u0438\u043d\u0435\u0446')
    
    >>> get_element('Свинец')
    (82, 'Pb', 'Lead', u'\u0421\u0432\u0438\u043d\u0435\u0446')
    
    """
    for e in ELEMENTS:
        a_num, lat, eng, rus = e
        if element in [eng, rus]:
            return (a_num, lat, eng, unicode(rus))
    raise ElementNotFound, "Element '%s' cannot be found." % element


def get_elements_names_list():
    if settings.get('locale') == 'ru_RU':
        return [e[3] for e in ELEMENTS]
    return [e[2] for e in ELEMENTS]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
