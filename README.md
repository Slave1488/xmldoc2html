xmldoc2html
----------------

Версия 1.1a

Автор: Рыльцов Дмитрий

github: https://github.com/Slave1488/xmldoc2html

--------

Описание
----------------

Компилирует исходный код на C# в документацию на XML и транслирует её в HTML

--------

Состав
----------------

cscode - модуль работы с C# кодом

layout - модуль рыботы с текстовой разметкой

myxml - модуль работы с xml текстом

filesup - вспомогательный модуль работы с файлами

htmlsup - вспомогательный модуль работы с html форматом

tests - тесты

compiler - основная логика

xth - запускаемое приложение

--------

Испльзование
----------------

Справка: ./xth.py --help

Пример запуска: ./xth.py source.cs --out index.html

--------

В разработке (мечты)
----------------

Полноценный C# парсер

--------

Подробности реализации:
----------------

Построчно обрабатывает код, производя поиск задокументированных объектов.
Найденные объекты формируются в соответствующие строки в html таблице.

--------

Результаты тестирования
----------------

    Name                              Stmts   Miss  Cover   Missing
    ---------------------------------------------------------------
    compiler.py                          27     27     0%   1-34
    cscode/linelexer.py                   5      0   100%
    cscode/lineparser.py                 23      0   100%
    cscode/linetoken.py                  22      0   100%
    filesup/reader.py                     5      0   100%
    layout/attributecreator.py            3      0   100%
    layout/description.py                63     18    71%   7-9, 16, 25, 39, 43-44, 58-59, 62-67, 86, 90-91, 94, 98
    layout/map/creator.py                13      0   100%
    layout/map/description.py            30      7    77%   10, 35-40
    myxml/compiler.py                    18      0   100%
    myxml/lexer.py                        4      0   100%
    myxml/member/compiler.py             15      4    73%   18-22
    myxml/member/id.py                    8      0   100%
    myxml/token.py                       15      1    93%   25
    tests/test_attribute_creator.py      15      4    73%   8-10, 20
    tests/test_layout.py                 51      4    92%   8-10, 72
    tests/test_line_lexer.py             36      4    89%   10-12, 56
    tests/test_map_creator.py            23      4    83%   9-11, 31
    tests/test_member_compiler.py        29      4    86%   11-13, 54
    tests/test_reader.py                 17      4    76%   8-10, 22
    xth.py                               16     16     0%   3-28
    ---------------------------------------------------------------
    TOTAL                               438     97    78%
