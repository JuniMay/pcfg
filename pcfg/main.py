from typing import List, Tuple, Optional

class BaseStructure:
    def __init__(self, s: Optional[str]=None) -> None:
        self.segments: List[Tuple[str, int]] = []

        if s is not None:
            self.derive(s)

    def __str__(self) -> str:
        s = ""
        for typ, count in self.segments:
            s = s + typ + str(count)

        return s

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o)

    def is_empty(self) -> bool:
        return len(self.segments) == 0

    def derive(self, s: str) -> None:
        if s == '':
            return

        self.segments = []
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
                        self.segments.append(('L', count))
                        state = 'Any'
                case 'Upper':
                    if c.isupper():
                        count = count + 1
                        index = index + 1
                    else:
                        self.segments.append(('U', count))
                        state = 'Any'
                case 'Digit':
                    if c.isdigit():
                        count = count + 1
                        index = index + 1
                    else:
                        self.segments.append(('D', count))
                        state = 'Any'
                case 'Special':
                    if not c.isupper() and not c.islower() and not c.isdigit():
                        count = count + 1
                        index = index + 1
                    else:
                        self.segments.append(('S', count))
                        state = 'Any'
                case other:
                    raise RuntimeError(f'Unknown state `{other}`.')
        
        match state:
            case 'Lower':
                self.segments.append(('L', count))
            case 'Upper':
                self.segments.append(('U', count))
            case 'Digit':
                self.segments.append(('D', count))
            case 'Special':
                self.segments.append(('S', count))
            case other:
                raise RuntimeError(f'Unknown state `{other}`.')


if __name__ == '__main__':
    base_structure_count = dict()
    sum = 0

    f = open('data/john.txt', 'r', encoding='utf-8')
    
    for s in f.readlines():
        base_structure = BaseStructure(s.strip())
        if base_structure.is_empty():
            continue

        if base_structure not in base_structure_count:
            base_structure_count[base_structure] = 0  
        base_structure_count[base_structure] += 1

        sum += 1


    print(len(base_structure_count))

    sorted_base_structures = dict(
        sorted(
            base_structure_count.items(), 
            key=lambda item: item[1], 
            reverse=True))

    for base_structure, count in sorted_base_structures.items():
        print(f'{str(base_structure):<20} {count / sum * 100 :<.3}%')