from grader.src.ged.classes.edit_path import EditPath


class SearchNode:
    def __init__(self, edit_path: EditPath = None, parent=None):
        self.edit_path = edit_path
        self.parent = parent
        self.children: list[SearchNode] = []
        self.sorted = False

    def add_child(self, child_edit_path: EditPath):
        self.sorted = False
        self.children.append(SearchNode(child_edit_path, self))
        return self.children[-1]

    def __sort_children(self):
        if not self.sorted:
            self.children.sort(key=lambda x: x.edit_path.predict_cost())
            self.children.reverse()
            self.sorted = True

    def remove_min_child(self):
        self.__sort_children()
        return self.children.pop()
