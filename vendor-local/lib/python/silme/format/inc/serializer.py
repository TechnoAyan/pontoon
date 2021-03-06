from ...core import EntityList, Entity, Comment
from .structure import IncStructure
from .parser import IncParser as Parser
import re

class IncSerializer():
    @classmethod
    def serialize(cls, l10nobject, fallback=None):
        if not fallback:
            fallback = l10nobject.fallback
        string = u''.join([cls.dump_element(element, fallback) for element in l10nobject])
        return string

    @classmethod
    def dump_element(cls, element, fallback=None):
        if isinstance(element, Entity):
            return cls.dump_entity(element, fallback=fallback)
        elif isinstance(element,Comment):
            return cls.dump_comment(element)
        else:
            return element

    @classmethod
    def dump_entity (cls, entity, fallback=None):
        if entity.params.has_key('source') and entity.params['source']['type']=='properties':
            match = Parser.patterns['entity'].match(entity.params['source']['string'])
            string = entity.params['source']['string'][0:match.start(1)]
            string += entity.id
            string += entity.params['source']['string'][match.end(1):match.start(2)]
            string += entity.get_value(fallback)
            string += entity.params['source']['string'][match.end(2):]
        else:
            string = u'#define %s %s' % (entity.id, entity.get_value(fallback))
        return string

    @classmethod
    def dump_entitylist(cls, elist, fallback=None):
        if not fallback:
            fallback = elist.fallback
        string = u''.join([cls.dump_entity(entity, fallback)+'\n' for entity in elist.get_entities()])
        return string

    @classmethod
    def dump_comment (cls, comment):
        string = u''
        for element in comment:
            string += cls.dump_element(element)
        if string:
            pattern = re.compile('\n')
            string = pattern.sub('\n# ', string)
            string = '# ' + string
            if string.endswith('# '):
                string = string[:-2]
        return string
