class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent

    def get_child_nodes(self, capacities):
        a, b = self.state
        max_a, max_b = capacities
        children = []

        # Fill jugs
        children.append(Node((max_a, b), self))
        children.append(Node((a, max_b), self))

        # Empty jugs
        children.append(Node((0, b), self))
        children.append(Node((a, 0), self))

        # Pour from A to B
        if a + b >= max_b:
            children.append(Node((a - (max_b - b), max_b), self))
        else:
            children.append(Node((0, a + b), self))

        # Pour from B to A
        if a + b >= max_a:
            children.append(Node((max_a, b - (max_a - a)), self))
        else:
            children.append(Node((a + b, 0), self))

        return children


def dfs(start_state, goal_state, capacities):
    start_node = Node(start_state, None)
    visited = set()
    stack = [start_node]

    while stack:
        node = stack.pop()

        if node.state == goal_state:
            path = []
            while node.parent:
                path.append(node.state)
                node = node.parent
            path.append(start_state)
            path.reverse()
            return path

        if node.state not in visited:
            visited.add(node.state)
            for child in node.get_child_nodes(capacities):
                stack.append(child)

    return None


start_state = (0, 0)
a,b = map(int, input("Enter the capacities of jugs: ").split())
c,d = map(int, input("Enter the capacities of goal state: ").split())

goal_state = (c, d)
capacities = (a, b)

path = dfs(start_state, goal_state, capacities)
print(path)
