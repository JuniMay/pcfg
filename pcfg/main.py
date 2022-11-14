from typing import List, Tuple

class BaseStructure:
    def __init__(self) -> None:
        self.segments: List[Tuple[str, int]] = []

    def __str__(self) -> str:
        s = ""
        for typ, count in self.segments:
            s = s + typ + str(count)

        return s

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o)

    def from_str(self, s: str) -> None:
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
    a = BaseStructure()
    a.from_str('AAAbbFF22232##&%^rtft$%ASs!')
    b = BaseStructure()
    b.from_str('ABCbaFX22232##&%^rtft$%ASs!')
    c = BaseStructure()
    c.from_str('123451#A')
    print(a, b, c)
    print(a == b)
    print(a == c)
    print(b == c)