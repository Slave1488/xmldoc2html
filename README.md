xmldoc2html
----------------

Версия 1.0

Автор: Рыльцов Дмитрий

github: https://github.com/Slave1488/xmldoc2html

--------

Описание
----------------

Компилирует исходный код на C# в документацию на XML и транслирует её в HTML

--------

Испльзование
----------------

Вход: файл content.txt в корневой папке программы

Выход: запись таблицы и стилей к ней в фале html.html в корневой папке программы

--------

В разработке (мечты)
----------------

Полноценный C# парсер и валидатор

--------

Состав
----------------

layout - описаниe гипертекстовой разметки

lineLexer - построковый лексер кода на C# (очень много упрощений)

xmlLexr - лексер для xml документации в коде

memberCompiler - сборщик member-тегов для xml формата / удобное представление данных об объектах

mapCreator - создатель карты тега (по ней можно объединять содержимое имеющее одинаковый путь)

tableCompiler - сборщик html-таблицы

И еще много впомогательных файлов

--------

Результаты тестирования
----------------

Name                              |Stmts   Miss  Cover   Missing
                                  |
----------------------------------|----------------------------
__main__.py                       |  29     29     0%   1-37
attributeCreator.py               |   3      0   100%
headerParser.py                   |  23      0   100%
layout.py                         |  63     18    71%   7-9, 16, 25, 39, 43-44, 58-59, 62-67, 86, 90-91, 94, 98
lineLexer.py                      |   5      0   100%
lineToken.py                      |  22      0   100%
mapCreator.py                     |  13      0   100%
memberCompiler.py                 |  15      4    73%   18-22
memberID.py                       |   8      0   100%
reader.py                         |   5      0   100%
styleCreator.py                   |   5      5     0%   1-7
tableCompile.py                   |  30     30     0%   1-36
tagDecorator.py                   |   6      6     0%   1-8
tagMap.py                         |  30      7    77%   10, 35-40
tests\test_attribute_creator.py   |   8      1    88%   12
tests\test_layout.py              |  44      1    98%   63
tests\test_line_lexer.py          |  32      1    97%   51
tests\test_map_creator.py         |  17      1    94%   24
tests\test_member_compiler.py     |  24      1    96%   47
tests\test_reader.py              |  10      1    90%   14
xmlCompiler.py                    |  18      0   100%
xmlLexer.py                       |   4      0   100%
xmlToken.py                       |  15      1    93%   25
                                  |
----------------------------------|----------------------------
TOTAL                             | 429    106    75%
