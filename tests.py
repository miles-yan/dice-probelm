from main import Dice
from main import Solution


def test_dice_move():
    # Init a Dice with top: 1, left: 4, front: 2
    d = Dice(1, 4, 2)

    d.move_down()
    # Dice move down
    assert d.state == (5, 4, 1)
    assert d.cost == d.bottom
    assert d.cost == 2

    # Dice move right
    d.move_right()
    assert d.state == (4, 2, 1)
    assert d.cost == 3 + 2

    # copied dice state and cost
    new_d = d.copy().move_right()
    assert new_d.state == (2, 3, 1)
    assert new_d.cost == 5 + new_d.bottom

    # origin Dice state should not change
    assert d.state == (4, 2, 1)


def test_dice_rotate():
    d = Dice(1,4,2)
    d.rotate_clockwise()
    assert d.state == (1, 2, 3)

    d.rotate_counterclockwise()
    assert d.state == (1, 4, 2)

    for _ in range(4):
        d.rotate_clockwise()
    assert d.state == (1, 4, 2)

    d.rotate_clockwise().rotate_clockwise()
    assert d.state == (1, 3, 5)


def test_rotate_dice_wisely():
    d = Dice(1, 4, 2)
    r = Solution().rotate_dice_wisely([0, 0], [8, 8], d)
    assert r[0], r[1] == (8, 8)
    assert r[2].state == (1, 4, 2)

    r = Solution().rotate_dice_wisely([8, 0], [0, 8], d)
    assert r[0], r[1] == (8, 8)
    assert r[2].state == (1, 2, 3)


def test_find_lowest_cost_MN():
    initial_dice = Dice(1, 4, 2)
    # if A, B in the same point, lowest cost is 0
    r1 = Solution().findLowestCostInMN(1, 1, initial_dice)
    assert r1 == 0

    # 1 * 3 area
    r2 = Solution().findLowestCostInMN(1, 3, initial_dice)
    # (1,4,2) -> +3 -> +1 = 4
    assert r2 == 4

    # 3 * 1 area
    r3 = Solution().findLowestCostInMN(3, 1, initial_dice)
    # (1,4,2) -> + 2 -> +1 = 3
    assert r3 == 3

    # 3 * 3 area
    r4 = Solution().findLowestCostInMN(3, 3, initial_dice)
    # (1,4,2) -> +3 + 1 + 2 +6 = 12
    # +3+2+1+4 = 10
    assert r4 == 10


def test_findABSteps():
    r = Solution().findABSteps([0, 0], [8, 8], Dice(1, 4, 2))
    assert r == 45

    r = Solution().findABSteps([3, 3], [0, 0], Dice(1, 4, 2))
    assert r == 12

    r = Solution().findABSteps([3, 3], [0, 0], Dice(1, 4, 2).rotate_clockwise().rotate_clockwise())
    assert r == 10


def test_findMinStepsForUnKnownState():
    r = Solution().findMinStepsForUnKnownState([0, 8], [8, 0])
    assert r == 45


if __name__ == '__main__':
    test_dice_move()
    test_dice_rotate()
    test_rotate_dice_wisely()
    test_find_lowest_cost_MN()
    test_findABSteps()
    test_findMinStepsForUnKnownState()
    print('All tests pass')
