from typing import Tuple
from copy import deepcopy
import os

class TerminalCollector:
    def __init__(self, train_data_path) -> None:
        self.train_data_path = train_data_path
        self.segment_terminal_count = {}
        self.segment_terminal_prob = {}
        self.segment_count = {}

    def add(self, segment: Tuple[str, int], terminal: str) -> None:
        if segment not in self.segment_terminal_count:
            self.segment_terminal_count[segment] = {}
        
        if segment not in self.segment_count:
            self.segment_count[segment] = 0

        if terminal not in self.segment_terminal_count[segment]:
            self.segment_terminal_count[segment][terminal] = 0

        self.segment_terminal_count[segment][terminal] += 1
        self.segment_count[segment] += 1
        
    
    def derive_single(self, s) -> None:
        if s == '':
            return

        self.segments = []
        state = 'Any'

        count = 0
        index = 0
        start_index = 0

        while index < len(s):
            c = s[index]
            match state:
                case 'Any':
                    if c.islower():
                        state = 'Lower'
                        count = 0
                        start_index = index
                    elif c.isupper():
                        state = 'Upper'
                        count = 0
                        start_index = index
                    elif c.isdigit():
                        state = 'Digit'
                        count = 0
                        start_index = index
                    else:
                        state = 'Special'
                        count = 0
                        start_index = index
                case 'Lower':
                    if c.islower():
                        count = count + 1
                        index = index + 1
                    else:
                        self.add(('L', count), s[start_index:index])
                        start_index = index
                        state = 'Any'
                case 'Upper':
                    if c.isupper():
                        count = count + 1
                        index = index + 1
                    else:
                        self.add(('U', count), s[start_index:index])
                        start_index = index
                        state = 'Any'
                case 'Digit':
                    if c.isdigit():
                        count = count + 1
                        index = index + 1
                    else:
                        self.add(('D', count), s[start_index:index])
                        start_index = index
                        state = 'Any'
                case 'Special':
                    if not c.isupper() and not c.islower() and not c.isdigit():
                        count = count + 1
                        index = index + 1
                    else:
                        self.add(('S', count), s[start_index:index])
                        start_index = index
                        state = 'Any'
                case other:
                    raise RuntimeError(f'Unknown state `{other}`.')
        
        match state:
            case 'Lower':
                self.add(('L', count), s[start_index:index])
            case 'Upper':
                self.add(('U', count), s[start_index:index])
            case 'Digit':
                self.add(('D', count), s[start_index:index])
            case 'Special':
                self.add(('S', count), s[start_index:index])
            case other:
                raise RuntimeError(f'Unknown state `{other}`.')


    def derive(self) -> None:
        with open(self.train_data_path, 'r', encoding='utf-8') as f:
            for s in f.readlines():
                self.derive_single(s)
        
        self.segment_terminal_prob = deepcopy(self.segment_terminal_count)
        for segment, tc in self.segment_terminal_count.items():
            for terminal, count in tc.items():
                self.segment_terminal_prob[segment][terminal] = (
                    count / self.segment_count[segment])
                
    def dump(self, dir) -> None:
        os.makedirs(dir, exist_ok=True)
        for segment, tp in self.segment_terminal_prob.items():
            tp = dict(sorted(tp.items(), key=lambda item: item[1], reverse=True))
            with open(f'{dir}/{segment[0]}{segment[1]}.csv', 'w', encoding='utf-8') as f:
                for terminal, prob in tp.items():
                    f.write(f'{terminal}, {prob}\n')

