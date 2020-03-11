from typing import Tuple, List

class Dice:
    def __init__(self, top, left, front, cost=0):
        self.top = top
        self.bottom = 7 - top
        self.left = left
        self.right = 7 - left
        self.front = front
        self.back = 7 - front

        self.cost = cost

    def __repr__(self):
        return f'Dice(top: {self.top}, left: {self.left}, front: {self.front}, cost: {self.cost})'

    @property
    def state(self):
        return self.top, self.left, self.front

    def move_down(self):
        # left, right does not change
        self.top, self.bottom, self.front, self.back = \
            self.back, self.front, self.top, self.bottom
        self.cost += self.bottom
        return self

    def move_right(self):
        # front, end does not change
        self.top, self.bottom, self.left, self.right = \
            self.left, self.right, self.bottom, self.top
        self.cost += self.bottom
        return self

    def copy(self):
        return Dice(self.top, self.left, self.front, self.cost)

    def rotate_clockwise(self):
        self.left, self.right, self.back, self.front = \
            self.front, self.back, self.left, self.right
        return self

    def rotate_counterclockwise(self):
        self.left, self.right, self.back, self.front = \
            self.back, self.front, self.right, self.left
        return self


class Solution:
    def findMinStepsForUnKnownState(self, A: Tuple[int, int], B: Tuple[int, int]):
        all_possible = [Dice(1, 2, 3), Dice(2, 6, 3), Dice(3, 5, 1), Dice(4, 6, 2), Dice(5, 4, 1), Dice(6, 4, 5)]
        res = []
        for p in all_possible:
            res.append(self.findABSteps(A, B, p))
            res.append(self.findABSteps(A, B, p.rotate_clockwise()))
            res.append(self.findABSteps(A, B, p.rotate_clockwise().rotate_clockwise()))
            res.append(self.findABSteps(A, B, p.rotate_counterclockwise()))

        return min(res)

    def findABSteps(self, A: Tuple[int, int], B: Tuple[int, int], dice_state):
        # if the dice is in a given state
        M, N, new_dice_state = self.rotate_dice_wisely(A, B, dice_state)

        return self.findLowestCostInMN(M, N, new_dice_state)

    def rotate_dice_wisely(self, A: Tuple[int, int], B: Tuple[int, int], dice_state: Dice):
        # B is same as A or B is in bottom-right direction: no need to rotate
        if A[0] <= B[0] and A[1] <= B[1]:
            return B[0] - A[0], B[1] - A[1], dice_state.copy()

        # B is in top-right, rotate clockwise
        if A[0] > B[0] and A[1] < B[1]:
            return A[0] - B[0], B[1] - A[1], dice_state.copy().rotate_clockwise()

        # B is in bottom-left,
        if A[0] < B[0] and A[1] > B[1]:
            return B[0] - A[0], A[1] - B[1], dice_state.copy().rotate_counterclockwise()

        # B is in top-left:
        if A[0] > B[0] and A[1] > B[1]:
            return A[0] - B[0], A[1] - B[1], dice_state.copy().rotate_clockwise().rotate_clockwise()

    def findLowestCostInMN(self, M: int, N: int, initial_dice: Dice):
        dp: List[List[List[Dice]]] = [[None] * N for _ in range(M)]
        for i in range(M):
            for j in range(N):
                if i == 0 and j == 0:
                    dp[0][0] = [initial_dice]
                elif i == 0:
                    dp[0][j] = [x.copy().move_right() for x in dp[0][j-1]]
                elif j == 0:
                    dp[i][0] = [x.copy().move_down() for x in dp[i-1][0]]
                else:
                    tmp_all_states = [x.copy().move_down() for x in dp[i-1][j]] + [x.copy().move_right() for x in dp[i][j-1]]
                    unique_states = set(x.state for x in tmp_all_states)
                    filtered_states = []
                    for state in unique_states:
                        state_with_min_cost = min([s for s in tmp_all_states if s.state == state], key=lambda x: x.cost)
                        filtered_states.append(state_with_min_cost)
                    dp[i][j] = filtered_states

        # print('last state', dp[-1][-1])
        return min(x.cost for x in dp[-1][-1])


if __name__ == '__main__':
    # If the Dice state is given
    ans1 = Solution().findABSteps([2, 8], [3, 1], Dice(6, 2, 4))
    print(f'Answer for given state between [2, 8] and [3, 1] is {ans1}')

    # If the Dice state is not given
    ans2 = Solution().findMinStepsForUnKnownState([0, 0], [8, 8])
    print(f'Answer for unknown dice state is {ans2}')
