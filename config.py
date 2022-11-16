from configparser import SafeConfigParser

section_names = ['official']

class Config(object):
    def __init__(self, *file_names):
        config = SafeConfigParser()

        found = config.read(file_names)

        if not found:
            raise ValueError('No config file found!')
        
        for name in section_names:
            self.__dict__.update(config.items(name))
        
