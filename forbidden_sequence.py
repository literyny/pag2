from utils import orient_sequence

class ForbiddenSequences:
    def __init__(self, sequences):
        self.sequences = sequences

    def is_blocked(self, prev, u, v):
        for seq in self.sequences:
            k = len(seq)

            if seq[-1] != v:
                continue

            suffix = self.get_suffix(prev, u, k - 1) + [v]
            if suffix == seq:
                return True

        return False

    def get_suffix(self, prev, last_node, length):
        seq = [last_node]
        curr = last_node

        for _ in range(length - 1):
            if curr not in prev:
                break
            curr, _ = prev[curr]
            seq.append(curr)

        return seq[::-1]


    @classmethod
    def from_file(cls, file_path, graph):
        all_sequences = []
        f = open(file_path, "r")

        for line in f:
            line = line.strip()
            if not line:
                continue

            edge_ids = line.split()
            if len(edge_ids) < 2:
                continue

            edges = []
            skip_line = False
            for el in edge_ids:
                edge_id = int(el)
                if edge_id not in graph.edges:
                    skip_line = True
                    break
                e = graph.edges[edge_id]
                edges.append((e.start.id, e.end.id))

            if skip_line:
                continue

            oriented_vertices = orient_sequence(edges[0], edges[1])
            if oriented_vertices is None:
                continue

            for (u, v) in edges[2:]:
                seq_last = oriented_vertices[-1]
                if u == seq_last:
                    new_vertex = v
                elif v == seq_last:
                    new_vertex = u
                else:
                    skip_line = True
                    break

                oriented_vertices.append(new_vertex)

            if not skip_line:
                all_sequences.append(oriented_vertices)

        f.close()
        return cls(all_sequences)