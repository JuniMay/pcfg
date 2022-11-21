from typing import Dict, Tuple
from pcfg import BaseStructureCollector, TerminalCollector, PreTerminalStructure, Segment
from queue import PriorityQueue
from copy import deepcopy


class Guesser:

    def __init__(
        self,
        base_structure_path: str,
        terminal_dir: str,
    ) -> None:

        self.base_collector = BaseStructureCollector()
        self.base_collector.from_file(base_structure_path)
        self.terminal_collector = TerminalCollector()
        self.terminal_collector.from_dir(terminal_dir)

        self.priority_queue: PriorityQueue[Tuple[float, PreTerminalStructure,
                                                 int]] = PriorityQueue()

    def initialize(self) -> None:
        for structure, prob in self.base_collector.base_structure_prob.items():
            insert_guess = PreTerminalStructure(prob)
            for segment_tuple in structure.segments:
                insert_guess.push(
                    Segment(self.terminal_collector.best_of(segment_tuple)[1],
                            terminal_str=self.terminal_collector.best_of(
                                segment_tuple)[0]))

            self.priority_queue.put((1 - insert_guess.prob(), insert_guess, 0))

        # for elem in self.priority_queue.queue:
        #     print(str(elem[0]), elem[1])

    def next(self) -> PreTerminalStructure:

        prob, next_guess, pivot = self.priority_queue.get()

        for i in range(pivot, len(next_guess)):
            working_guess = deepcopy(next_guess)
            if working_guess.segments[i].is_terminal():
                terminal_str = working_guess.segments[i].terminal_str
                next_terminal = self.terminal_collector.next_of(terminal_str)
                if next_terminal is None:
                    continue
                working_guess.segments[i] = Segment(
                    next_terminal[1], terminal_str=next_terminal[0])

            self.priority_queue.put(
                (1 - working_guess.prob(), working_guess, i))

        return str(next_guess), 1 - prob
