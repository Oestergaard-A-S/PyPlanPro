import networkx as nx


class TaskGraph:
    def __init__(self, tasks):
        self.tasks = {task.id: task for task in tasks}
        self.graph = self._create_task_graph()

    def _create_task_graph(self):
        """
        Creates a directed acyclic graph from the given tasks.
        """
        task_graph = nx.DiGraph()
        for task in self.tasks.values():
            task_graph.add_node(task.id, duration=task.duration, priority=task.priority)
            for predecessor in task.predecessors:
                task_graph.add_edge(predecessor.id, task.id)
        return task_graph

    def _compute_longest_paths(self):
        """
        Computes the longest path for each node in the task graph using a topological
        sort.
        """
        longest_path = {task_id: 0 for task_id in self.tasks}
        for task in nx.topological_sort(self.graph):
            duration = self.graph.nodes[task]["duration"]
            for predecessor in self.graph.predecessors(task):
                longest_path[task] = max(
                    longest_path[task], longest_path[predecessor] + duration
                )
        return longest_path

    def _custom_topological_sort(self, longest_path):
        """
        Performs a custom topological sort of tasks considering priority and longest
        path.
        """
        visited = set()
        result = []

        def visit(node):
            """
            Recursive function to traverse the task graph in the desired order.
            """
            if node not in visited:
                visited.add(node)
                predecessors = sorted(
                    self.graph.predecessors(node),
                    key=lambda n: (self.graph.nodes[n]["priority"], -longest_path[n]),
                )
                for predecessor in predecessors:
                    visit(predecessor)
                result.append(node)

        for task in sorted(
            self.tasks.values(),
            key=lambda t: (self.graph.nodes[t.id]["priority"], -longest_path[t.id]),
        ):
            visit(task.id)

        return result

    def get_task_order(self):
        """
        Returns a list of task IDs in the order required to complete them as quickly
        as possible while considering task priorities.
        """
        longest_path = self._compute_longest_paths()
        return self._custom_topological_sort(longest_path)
