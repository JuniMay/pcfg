from pcfg import BaseStructureCollector
from pcfg import TerminalCollector, Guesser

if __name__ == '__main__':
    bcollector = BaseStructureCollector()
    bcollector.derive('data/myspace.txt')
    bcollector.dump('model/base.csv')

    tcollector = TerminalCollector()
    tcollector.derive('data/myspace.txt')
    tcollector.dump('model/terminal')

    guesser = Guesser('model/base.csv', 'model/terminal', use_preterminal=True)
    guesser.initialize()

    while True:
        input("")
        print(guesser.next())
