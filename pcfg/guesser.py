from typing import Dict, Tuple
from pcfg import BaseStructureCollector, TerminalCollector
from pcfg import PreTerminalStructure, Segment
from queue import PriorityQueue
from copy import deepcopy


class Guesser:

    def __init__(self,
                 base_structure_path: str,
                 terminal_dir: str,
                 use_preterminal: bool = False) -> None:

        self.base_collector = BaseStructureCollector()
        self.base_collector.from_file(base_structure_path)
        self.terminal_collector = TerminalCollector()
        self.terminal_collector.from_dir(terminal_dir)

        self.priority_queue: PriorityQueue[Tuple[float, PreTerminalStructure,
                                                 int]] = PriorityQueue()

        self.use_preterminal = use_preterminal

    def initialize(self) -> None:
        for structure, prob in self.base_collector.base_structure_prob.items():
            insert_guess = PreTerminalStructure(prob)
            for non_terminal in structure.non_terminals:

                if self.use_preterminal and (non_terminal[0] == "L"
                                             or non_terminal[0] == 'U'):
                    insert_guess.push(Segment(1.0, non_terminal))
                else:
                    insert_guess.push(
                        Segment(
                            self.terminal_collector.best_of(non_terminal)[1],
                            terminal_str=self.terminal_collector.best_of(
                                non_terminal)[0]))

            self.priority_queue.put((1 - insert_guess.prob(), insert_guess, 0))

    def next(self) -> PreTerminalStructure:

        prob, next_guess, pivot = self.priority_queue.get()

        for i in range(pivot, len(next_guess)):
            if (not next_guess.segments[i].is_terminal()
                    and self.use_preterminal):
                continue

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
