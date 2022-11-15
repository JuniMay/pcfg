from pcfg import BaseStructureCollector
from pcfg import TerminalCollector

if __name__ == '__main__':
    bcollector = BaseStructureCollector('data/myspace.txt')
    bcollector.derive()
    bcollector.dump('model/base.csv')

    tcollector = TerminalCollector('data/myspace.txt')
    tcollector.derive()
    tcollector.dump('model/terminal')