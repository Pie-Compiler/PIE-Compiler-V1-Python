from dataclasses import dataclass

CANONICAL_MAP = {
    'KEYWORD_INT': 'int', 'int': 'int',
    'KEYWORD_FLOAT': 'float', 'float': 'float',
    'KEYWORD_CHAR': 'char', 'char': 'char',
    'KEYWORD_STRING': 'string', 'string': 'string',
    'KEYWORD_BOOL': 'bool', 'bool': 'bool', 'boolean': 'bool',
    'KEYWORD_VOID': 'void', 'void': 'void',
    'KEYWORD_FILE': 'file', 'file': 'file',
    'KEYWORD_SOCKET': 'socket', 'socket': 'socket',
    'KEYWORD_DICT': 'dict', 'dict': 'dict',
    'KEYWORD_NULL': 'null', 'null': 'null',
    'KEYWORD_ARRAY': 'array', 'array': 'array'
}

def canonicalize(type_token: str) -> str:
    return CANONICAL_MAP.get(type_token, type_token)

@dataclass
class TypeInfo:
    base: str                 # canonical base type (int,float,char,string,bool,file,socket,dict)
    is_array: bool = False    # static array flag
    is_dynamic: bool = False  # dynamic array flag ([] form)
    size: int | None = None   # static size if known

    @property
    def kind(self):
        if self.is_array or self.is_dynamic:
            return 'array'
        return 'scalar'

    def element_base(self):
        return self.base if self.kind == 'array' else None

    def describe(self):
        if self.kind == 'array':
            if self.is_dynamic:
                return f"dynamic {self.base}[]"
            return f"{self.base}[{self.size if self.size is not None else '?'}]"
        return self.base
