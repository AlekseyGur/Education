import re


def clear_pos_int(input_str = 0) -> int:
    """Проверяет являются ли вводимые данные положительным целым числом.
    :param input_str: любой тип данных, который надо очистить
    :result: вернёт целое число или 0, если преобразование невозможно
    """
    try:
        i = int(re.sub('[^0-9]', '', str(input_str)))
        return i if str(i) == str(input_str) and i > 0 else 0
    except:
        return 0

def clear_bool(input_str = False) -> bool:
    """Проверяет являются ли вводимые данные положительным целым числом.
    :param input_str: любой тип данных, который надо очистить
    :result: вернёт bool значение или False, если преобразование невозможно
    """
    try:
        i = bool(input_str)
        return i if i == input_str else False
    except:
        return False

def clear_text(input_str = '') -> str:
    """Обеззараживает получаемые от пользователя данные.
    :param input_str: строка, из которой надо удалить опасные символы
    :result: вернёт целое число или 0, если преобразование невозможно
    """
    return re.sub('[^.,0-9a-zа-яё-]', '', str(input_str), flags=re.IGNORECASE)

def validate_clear():
    """Проверяет работу валиадторов"""
    assert clear_pos_int() == 0, 'clear_pos_int() != 0'
    assert clear_pos_int(2) == 2, 'clear_pos_int(2) != 2'
    assert clear_pos_int('2') == 2, 'clear_pos_int("2") != 2'
    assert clear_pos_int(-5) == 0, 'clear_pos_int(-5) != 0'
    assert clear_pos_int(1.2) == 0, 'clear_pos_int(1.2) != 0'
    assert clear_pos_int("1,5") == 0, 'clear_pos_int("1,5") != 0'
    assert clear_pos_int("asd") == 0, 'clear_pos_int("asd") != 0'
    assert clear_pos_int("фыв") == 0, 'clear_pos_int("фыв") != 0'
    assert clear_pos_int("a1s2d") == 0, 'clear_pos_int("asd1") != 0'
    assert clear_pos_int(False) == 0, 'clear_pos_int(False) != 0'
    assert clear_pos_int(True) == 0, 'clear_pos_int(True) != 0'

    assert clear_bool() == False, 'clear_bool() != False'
    assert clear_bool(2) == False, 'clear_bool(2) != False'
    assert clear_bool('2') == False, 'clear_bool(2) != False'
    assert clear_bool(-5) == False, 'clear_bool(-5) != False'
    assert clear_bool(1.2) == False, 'clear_bool(1.2) != False'
    assert clear_bool("1,5") == False, 'clear_bool("1,5") != False'
    assert clear_bool("asd") == False, 'clear_bool("asd") != False'
    assert clear_bool("фыв") == False, 'clear_bool("фыв") != False'
    assert clear_bool("a1s2d") == False, 'clear_bool("asd1") != False'
    assert clear_bool(False) == False, 'clear_bool(False) != False'
    assert clear_bool(True) == True, 'clear_bool(True) != True'

    assert clear_text() == "", 'clear_text() != ""'
    assert clear_text(2) == "2", 'clear_text(2) != "2"'
    assert clear_text('2') == "2", 'clear_text("2") != "2"'
    assert clear_text(-5) == "-5", 'clear_text(-5) != "-5"'
    assert clear_text(1.2) == "1.2", 'clear_text(1.2) != "1.2"'
    assert clear_text("1,5") == "1,5", 'clear_text("1,5") != "1,5"'
    assert clear_text("asd") == "asd", 'clear_text("asd") != "asd"'
    assert clear_text("фыв") == "фыв", 'clear_text("фыв") != "фыв"'
    assert clear_text("a1s2d") == "a1s2d", 'clear_text("asd1") != "asd1"'
    assert clear_text(False) == "False", 'clear_text(False) != "False"'
    assert clear_text(True) == "True", 'clear_text(True) != "True"'

    assert clear_text(">'<") == "", 'clear_text(">\'<") != ""'

    return True
