import unittest
from os.path import splitext
from HamsterMaze import parse_maze, search_path, draw_path


def solve_maze(maze_name):
    draw_path(maze_name, search_path(parse_maze(maze_name, False), False), False)
    solved_maze_name = '{}_solved.txt'.format(splitext(maze_name)[0])
    with open(solved_maze_name, 'r') as solved_maze_file:
        solved_maze_data = solved_maze_file.read()
    return solved_maze_data


class MazeTest(unittest.TestCase):
    def test_different_line_lengths(self):
        self.assertEqual(solve_maze('MazeTest/maze0.txt'), '"S**xx__xxx"\n'
                                                           '"__*xx__xx_"\n'
                                                           '"xx*_x******x__"\n'
                                                           '"_**_x*xxx_*x__"\n'
                                                           '"_*xx**xxxx***F"\n'
                                                           '"_****_x_x_"\n'
                                                           '"xx___xx__x"')

    def test_different_column_lengths(self):
        self.assertEqual(solve_maze('MazeTest/maze1.txt'), '"S__xx__xxx"\n'
                                                           '"***xx__xx_"\n'
                                                           '"xx*_x__x__"\n'
                                                           '"_**____x__"\n'
                                                           '"_*xx__x___"\n'
                                                           '"_**___x_x_"\n'
                                                           '"xx*__xx__x"\n'
                                                           '"F**_"')

    def test_different_column_and_lines_lengths(self):
        self.assertEqual(solve_maze('MazeTest/maze2.txt'), '"_"\n'
                                                           '"S__xx__xxx"\n'
                                                           '"***xx****_"\n'
                                                           '"xx*_x*_x*_"\n'
                                                           '"***_x*_x*____"\n'
                                                           '"*xxx**x**_xx_"\n'
                                                           '"*****xx*x____"\n'
                                                           '"xxxxxxx*___"\n'
                                                           '"F*******"')

    @unittest.expectedFailure
    def test_many_finishes(self):
        self.assertEqual(solve_maze('MazeTest/maze3.txt'), '')

    @unittest.expectedFailure
    def test_many_starts(self):
        self.assertEqual(solve_maze('MazeTest/maze4.txt'), '')

    def test_big_maze(self):
        self.assertEqual(solve_maze('MazeTest/maze5.txt'), '"_xxxx____xxx___xxxxxx_**********xx__xxx"\n'
                                                           '"___xx__xx_x_xxx******x*x__x_x_x*x_x****F__xxx_____x"\n'
                                                           '"___x__x_x_x___x*x___***x____xxx*****__xxxxx____xx"\n'
                                                           '"xx___xx__x******x___xx"\n'
                                                           '"xxx********xxxxxxxxxxxxx_____xxxx_xxx___"\n'
                                                           '"_x**"\n'
                                                           '"***___xxxx___xxxxxx_xxxxx_____xxx__xxx_______"\n'
                                                           '"*___xxxx_______xxxxx______xxxx____xxx____xx"\n'
                                                           '"*__xxxxx_xxxxx"\n'
                                                           '"*xxxxxxx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"\n'
                                                           '"*******x********xxxx*****xxx____________________xxx__xxxx____xxx"\n'
                                                           '"x___xx***_xxx__******_xx****___xx___xx_______xxx______xx____"\n'
                                                           '"__xxxxxxxxxxxxxxxxxxxxxxxxx*xxxxxxxxxxxxxxxxxxxxxx__xxx______x_"\n'
                                                           '"x_x___x___x___x___x___x___x***x***x***x***x***x***x"\n'
                                                           '"x_x_x_x_x_x_x_x_x_x_x_x_x_x_x*x*x*x*x*x*x*x*x*x*x*x"\n'
                                                           '"x_x_x_x_x_x_x_x_x_x_x_x_x_x_x*x*x*x*x*x*x*x*x*x*x*x"\n'
                                                           '"x_x_x_x_x_x_x_x_x_x_x_x_x_x_x*x*x*x*x*x*x*x*x*x*x*x"\n'
                                                           '"x_x_x_x_x_x_x_x_x_x_x_x_x_x_x*x*x*x*x*x*x*x*x*x*x*x"\n'
                                                           '"x_x_x_x_x_x_x_x_x_x_x_x_x_x_x*x*x*x*x*x*x*x*x*x*x*x"\n'
                                                           '"x_x_x_x_x_x_x_x_x_x_x_x_x_x_x*x*x*x*x*x*x*x*x*x*x*x"\n'
                                                           '"x___x___x___x___x___x___x___x***x***x***x***x***x***_"\n'
                                                           '"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*"\n'
                                                           '"_____________________*******************************"\n'
                                                           '"xxx___xx__xx___xxxxx_*xxxxx"\n'
                                                           '"xxxx__xx______xx_____*xx_S**"\n'
                                                           '"xx_xx_xx__xx__xx_____*xxxxx*"\n'
                                                           '"xx__xxxx__xx__xx_____*xx___*"\n'
                                                           '"xx___xxx__xx___xxxxx_*xxxxx*_"\n'
                                                           '"_____________________*******_"')

    def test_first_small_maze(self):
        self.assertEqual(solve_maze('MazeTest/maze6.txt'), '"S"\n'
                                                           '"F"')

    def test_second_small_maze(self):
        self.assertEqual(solve_maze('MazeTest/maze7.txt'), '"*S"\n'
                                                           '"F"')

    @unittest.expectedFailure
    def test_closed_maze(self):
        self.assertEqual(solve_maze('MazeTest/maze8.txt'), '')

    @unittest.expectedFailure
    def test_empty_file(self):
        self.assertEqual(solve_maze('MazeTest/maze9.txt'), '')

    def test_wall_maze(self):
        self.assertEqual(solve_maze('MazeTest/maze10.txt'), '"_____xx****S"\n'
                                                            '"_____xx*____"\n'
                                                            '"_____xx*____"\n'
                                                            '"********____"\n'
                                                            '"*____xx_____"\n'
                                                            '"*____xx_____"\n'
                                                            '"F____xx_____"')

    def test_ladder_maze(self):
        self.assertEqual(solve_maze('MazeTest/maze11.txt'), '"F*****__"\n'
                                                            '"____x*_x"\n'
                                                            '"___x**x_"\n'
                                                            '"__x_*x__"\n'
                                                            '"__x_*x__"\n'
                                                            '"___x**x_"\n'
                                                            '"____x**x"\n'
                                                            '"_____x*S"')

    def test_back_maze(self):
        self.assertEqual(solve_maze('MazeTest/maze12.txt'), '"_*******__"\n'
                                                            '"_*xxxxx*_x"\n'
                                                            '"_*x__***____________________________________"\n'
                                                            '"_*x_S*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_"\n'
                                                            '"_*x___x_____________________________________"\n'
                                                            '"_*xxxxx___"\n'
                                                            '"_********F"')

    def test_hole_maze(self):
        self.assertEqual(solve_maze('MazeTest/maze13.txt'), '"xxxxxxx"\n'
                                                            '"xx****S"\n'
                                                            '"xx*xxxx"\n'
                                                            '"xx***xx"\n'
                                                            '"xxxx*xx"\n'
                                                            '"xxF**xx"')


if __name__ == '__main__':
    unittest.main()
