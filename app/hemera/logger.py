import logging

fmt = {
        1 : logging.Formatter('[%(asctime)s] %(name)s %(levelname)s: "%(message)s"', '%Y%m%d %H:%M:%S'),
        2 : logging.Formatter('%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s', '%a %d %b %Y %H:%M:%S'),
        3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        }

class Logger:
    def __init__(self, file, name=None, level=1):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        self.fh = logging.FileHandler(file)
        self.fh.setLevel(level)
        self.fh.setFormatter(fmt[int(level)])

        self.ch = logging.StreamHandler()
        self.ch.setLevel(level)
        self.ch.setFormatter(fmt[int(level)])

        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

    def getlog(self):
        return self.logger
