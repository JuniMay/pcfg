from typing import List, Tuple, Optional, Self, Dict
import re
import os


class BaseStructure:
    def __init__(self) -> None:
        self.non_terminals: List[Tuple[str, int]] = []

    def __str__(self) -> str:
        s = ""
        for typ, count in self.non_terminals:
            s = s + typ + str(count)
        return s

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o)

    def is_empty(self) -> bool:
        return len(self.non_terminals) == 0

    def derive(self, s: str) -> Self:
        if s == '':
            return self

        self.non_terminals = []
        state = 'Any'

        count = 0
        index = 0

        while index < len(s):
            c = s[index]
            match state:
                case 'Any':
                    if c.islower():
                        state = 'Lower'
                        count = 0
                    elif c.isupper():
                        state = 'Upper'
                        count = 0
                    elif c.isdigit():
                        state = 'Digit'
                        count = 0
                    else:
                        state = 'Special'
                        count = 0
                case 'Lower':
                    if c.islower():
                        count = count + 1
                        index = index + 1
                    else:
                        self.non_terminals.append(('L', count))
                        state = 'Any'
                case 'Upper':
                    if c.isupper():
                        count = count + 1
                        index = index + 1
                    else:
                        self.non_terminals.append(('U', count))
                        state = 'Any'
                case 'Digit':
                    if c.isdigit():
                        count = count + 1
                        index = index + 1
                    else:
                        self.non_terminals.append(('D', count))
                        state = 'Any'
                case 'Special':
                    if not c.isupper() and not c.islower() and not c.isdigit():
                        count = count + 1
                        index = index + 1
                    else:
                        self.non_terminals.append(('S', count))
                        state = 'Any'
                case other:
                    raise RuntimeError(f'Unknown state `{other}`.')

        match state:
            case 'Lower':
                self.non_terminals.append(('L', count))
            case 'Upper':
                self.non_terminals.append(('U', count))
            case 'Digit':
                self.non_terminals.append(('D', count))
            case 'Special':
                self.non_terminals.append(('S', count))
            case other:
                raise RuntimeError(f'Unknown state `{other}`.')

        return self

    def from_str(self, s: str) -> Self:
        m = re.findall('(L|U|D|S)([0-9]+)', s)
        if len(m) == 0:
            return self

        for typ, count_str in m:
            self.non_terminals.append((typ, int(count_str)))

        return self


class BaseStructureCollector:
    def __init__(self) -> None:
        self.base_structure_prob: Dict[BaseStructure, float] = {}

    def derive(self, train_data_path: str) -> None:
        base_structure_count = dict()
        base_structure_total = 0
        with open(train_data_path, 'r', encoding='utf-8') as f:
            for s in f.readlines():
                base_structure = BaseStructure().derive(s.strip())
                if base_structure.is_empty():
                    continue
                if base_structure not in base_structure_count:
                    base_structure_count[base_structure] = 0
                base_structure_count[base_structure] += 1
                base_structure_total += 1

        for structure, count in dict(
            sorted(
                base_structure_count.items(),
                key=lambda item: item[1],
                reverse=True)).items():
            self.base_structure_prob[structure] = count / base_structure_total

    def from_file(self, filename) -> None:
        with open(filename, 'r', encoding='utf-8') as f:
            for s in f.readlines():
                structure_str, prob_str = s.strip().split(',')
                self.base_structure_prob[BaseStructure().from_str(
                    structure_str)] = float(prob_str.strip())

    def dump(self, filename) -> None:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            for structure, prob in self.base_structure_prob.items():
                f.write(f'{structure}, {prob}\n')
