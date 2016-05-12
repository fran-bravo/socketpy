import re


class Analyzer:
    c_built_ins = ["int", "uint8_t", "uint16_t", "uint32_t", "void", "char"]
    c_ptr_types = list(map(lambda string: string + "*", c_built_ins))
    c_array_types = r'^[' + '|'.join(c_built_ins + c_ptr_types)+ ']'

    def analyze_type(self, tipo):
        return tipo in self.c_built_ins or tipo in self.c_ptr_types or self._match_array(tipo)

    def _match_array(self, tipo):
        if re.match(self.c_array_types, tipo) and re.match('^\\[[0-9]+\\]', tipo[-4:]):
            return True
        else:
            return False