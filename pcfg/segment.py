from typing import Tuple


class Segment:

    def __init__(self,
                 prob,
                 non_terminal: Tuple[str, int] = None,
                 terminal_str: str = None) -> None:
        self.prob = None
        self.non_terminal: Tuple[str, int] = non_terminal
        self.terminal_str: str = terminal_str
        self.prob = prob
        if self.non_terminal is None and self.terminal_str is None:
            raise ValueError(
                "Segment must be either terminal or non-terminal.")

    def __len__(self) -> int:
        if self.non_terminal is not None:
            return self.non_terminal[1]
        elif self.terminal_str is not None:
            return len(self.terminal_str)
        else:
            raise ValueError(
                "Segment must be either terminal or non-terminal (this shall not happen, check the code)."
            )

    def is_terminal(self) -> bool:
        return (self.terminal_str is not None)

    def set_prob(self, prob: float) -> None:
        self.prob = prob
