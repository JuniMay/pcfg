from typing import List, Self
from pcfg import Segment


class PreTerminalStructure:

    def __init__(self, base_structure_prob: float) -> None:
        """Pre-Terminal Structure
        
        """
        self.segments: List[Segment] = []
        self.base_structure_prob = base_structure_prob

    def __str__(self) -> str:
        res = ""
        for segment in self.segments:
            res = res + segment.terminal_str  # TODO: non-terminal in segment

        return res

    def __eq__(self, __o: Self) -> bool:
        return self.prob() == __o.prob()

    def __gt__(self, __o: Self) -> bool:
        return self.prob() > __o.prob()

    def __lt__(self, __o: Self) -> bool:
        return self.prob() < __o.prob()

    def __len__(self) -> int:
        return len(self.segments)

    def push(self, segment: Segment) -> None:
        self.segments.append(segment)

    def prob(self) -> float:
        res = self.base_structure_prob
        for segment in self.segments:
            res *= segment.prob

        return res

    def is_terminal(self) -> bool:
        for segment in self.segments:
            if segment.non_terminal is not None:
                return False

        return True
