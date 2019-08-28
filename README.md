# HamsterMaze

Программа предназначена для поиска пути в лабиринте, который находится в текстовом файле и задан следующим образом:

- S = старт (должен быть единственным во всём лабиринте)
- _ = свободное пространство
- F = финиш (должен быть единственным во всём лабиринте)
- x = препятствие

Для нахождения пути в дефолтном файле (**maze.txt**) напишите

`python HamsterMaze.py`

Для нахождения пути в конкретном файле напишите

`python HamsterMaze.py ПУТЬ ДО ФАЙЛА С ЛАБИРИНТОМ`

Для запуска тестов напишите

`python MazeTest.py`

Найденный путь помещается рядом с файлом лабиринта в файл с названием **ИМЯ ФАЙЛА С ЛАБИРИНТОМ**_solved.txt

Программа написана на Python 3.7