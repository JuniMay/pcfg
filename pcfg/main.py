from pcfg import BaseStructureCollector
from pcfg import TerminalCollector

if __name__ == '__main__':
    bcollector = BaseStructureCollector()
    bcollector.derive('data/myspace.txt')
    bcollector.dump('model/base.csv')

    tcollector = TerminalCollector()
    tcollector.derive('data/myspace.txt')
    tcollector.dump('model/terminal')

    bcollector = BaseStructureCollector()
    bcollector.from_file('model/base.csv')
    # print(bcollector.base_structure_prob)

    tcollector = TerminalCollector()
    tcollector.from_dir('model/terminal')
    # print(tcollector.segment_terminal_prob)
