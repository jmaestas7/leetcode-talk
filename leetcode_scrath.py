import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import heapq
from collections import defaultdict, deque

class Solution:
    def __init__(self):
        self.test_cases = [
            ([[0,1,4],[0,2,2],[2,3,12],[2,4,6]], 2),
            ([[0,1,5],[1,2,10],[0,3,15],[3,4,20],[3,5,5],[0,6,10]], 3),
            ([[0,1,3],[0,2,4],[0,3,5],[0,4,6],[0,5,7]], 2),
            ([[0,1,1],[1,2,2],[2,3,3],[3,4,4],[4,5,5],[5,6,6],[6,7,7],[7,8,8],[8,9,9]], 2)
        ]
        for edges, k in self.test_cases:
            print(f"\nRunning test case with k = {k}")
            self.visualize_tree(edges, "Before Pruning")

            result, kept_edge_indices = self.maximizeSumOfWeights(edges, k)
            print(f"Maximum sum after pruning: {result}")

            pruned_edges = [edges[i] for i in sorted(kept_edge_indices)]
            removed_edges = [edges[i] for i in range(len(edges)) if i not in kept_edge_indices]

            self.visualize_tree(pruned_edges, "After Pruning", removed_edges=removed_edges)

    def maximizeSumOfWeights(self, edges, k):
        n = len(edges) + 1
        degree = [0] * n
        adj = defaultdict(list)
        edge_map = {}

        # Build graph
        for i, (u, v, w) in enumerate(edges):
            adj[u].append((v, w, i))
            adj[v].append((u, w, i))
            edge_map[i] = (u, v, w)
            degree[u] += 1
            degree[v] += 1

        keep = set(range(len(edges)))
        min_heap = [(w, i) for i, (_, _, w) in edge_map.items()]
        heapq.heapify(min_heap)

        while True:
            over = [i for i in range(n) if degree[i] > k]
            if not over:
                break

            while min_heap:
                w, i = heapq.heappop(min_heap)
                if i not in keep:
                    continue
                u, v, _ = edge_map[i]
                if degree[u] > k or degree[v] > k:
                    keep.remove(i)
                    degree[u] -= 1
                    degree[v] -= 1
                    break

        total = sum(edge_map[i][2] for i in keep)
        return total, keep

    def visualize_tree(self, edges, title, removed_edges=None):
        G = nx.Graph()
        for u, v, w in edges:
            G.add_edge(u, v, weight=w)

        if removed_edges:
            for u, v, w in removed_edges:
                G.add_edge(u, v, weight=f"{w}-deleted")
                G[u][v]['style'] = 'dashed'

        # Modified recursive layout with disconnected support
        pos = {}
        visited = set()
        x_offset = 0  # offset to separate disconnected components

        def build_tree_pos(node, parent, x=0, y=0, dx=2):
            nonlocal x_offset
            visited.add(node)
            pos[node] = (x + x_offset, y)
            children = [n for n in G.neighbors(node) if n != parent]
            width = dx * (len(children) - 1)
            next_x = x - width / 2
            for child in children:
                if child not in visited:
                    build_tree_pos(child, node, next_x, y - 3, dx)
                    next_x += dx

        # Layout all components
        for node in G.nodes:
            if node not in visited:
                build_tree_pos(node, None)
                x_offset += 10  # space between disconnected components

        edge_labels = nx.get_edge_attributes(G, 'weight')
        edge_styles = nx.get_edge_attributes(G, 'style')

        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightblue',
                node_size=1000, font_size=14)

        solid_edges = [(u, v) for u, v in G.edges() if G[u][v].get('style') != 'dashed']
        dashed_edges = [(u, v) for u, v in G.edges() if G[u][v].get('style') == 'dashed']

        nx.draw_networkx_edges(G, pos, edgelist=solid_edges, width=2)
        nx.draw_networkx_edges(G, pos, edgelist=dashed_edges, style='dashed', edge_color='gray')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

# To run:
if __name__ == "__main__":
    Solution()
