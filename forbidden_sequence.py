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

        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                vertexes = []
                prev_edge = None
                oriented = False
                skip_line = False

                for el in line.split():
                    edge_id = int(el)

                    if edge_id not in graph.edges:
                        skip_line = True
                        break
                    
                    edge = graph.edges[edge_id]
                    u = edge.start.id
                    v = edge.end.id

                    if prev_edge is None:
                        prev_edge = (u, v)
                        continue

                    if not oriented:
                        pu, pv = prev_edge
                        common = {pu, pv} & {u, v}

                        if not common:
                            skip_line = True
                            break

                        mid = common.pop()
                        first = pu if pv == mid else pv
                        last = u if v == mid else v

                        vertexes = [first, mid, last]
                        oriented = True

                    else:
                        seq_last = vertexes[-1]
                        if u == seq_last:
                            new_vertex = v
                        elif v == seq_last:
                            new_vertex = u
                        else:
                            skip_line = True
                            break

                        vertexes.append(new_vertex)

                    prev_edge = (u, v)

                if not skip_line and vertexes:
                    all_sequences.append(vertexes)

        return cls(all_sequences)