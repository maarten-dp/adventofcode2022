from runner_utils import expected_test_result


class Tree:
    def __init__(self, height):
        self.height = height
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None

    def add_left(self, neighbour):
        self.left = neighbour
        neighbour.right = self

    def add_top(self, neighbour):
        self.top = neighbour
        neighbour.bottom = self

    def is_visible(self):
        from_top = self.is_visible_in_line("top", self.height)
        from_bottom = self.is_visible_in_line("bottom", self.height)
        from_left = self.is_visible_in_line("left", self.height)
        from_right = self.is_visible_in_line("right", self.height)
        return from_top or from_bottom or from_left or from_right

    def is_visible_in_line(self, orientation, height):
        tree = getattr(self, orientation)
        if tree is None:
            return True
        if tree.height < height:
            return tree.is_visible_in_line(orientation, height)
        return False

    def get_scenic_score(self):
        score_top = self.line_score("top", self.height)
        score_bottom = self.line_score("bottom", self.height)
        score_left = self.line_score("left", self.height)
        score_right = self.line_score("right", self.height)
        return score_top * score_bottom * score_left * score_right

    def line_score(self, orientation, height):
        tree = getattr(self, orientation)
        if tree is None:
            return 0
        if tree.height >= height:
            return 1
        return 1 + tree.line_score(orientation, height)


class Forest:
    def __init__(self, input):
        grid = []
        self.trees = []
        for column_idx, line in enumerate(input.strip().splitlines()):
            row = []
            for row_idx, tree_height in enumerate(map(int, line)):
                tree = Tree(tree_height)
                self.trees.append(tree)
                row.append(tree)
                if row_idx > 0:
                    row[row_idx - 1].add_left(tree)
                if column_idx > 0:
                    grid[column_idx - 1][row_idx].add_top(tree)
            grid.append(row)


@expected_test_result(21)
def solve1(input):
    forest = Forest(input)

    visible_trees = 0
    for tree in forest.trees:
        visible_trees += tree.is_visible()
    return visible_trees


@expected_test_result(8)
def solve2(input):
    forest = Forest(input)

    scenic_score = 0
    for tree in forest.trees:
        scenic_score = max(scenic_score, tree.get_scenic_score())
    return scenic_score
