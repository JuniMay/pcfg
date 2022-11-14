from pcfg import BaseStructureCollector

if __name__ == '__main__':
    collector = BaseStructureCollector('data/myspace.txt')
    collector.derive()
    collector.dump('model/base.csv')