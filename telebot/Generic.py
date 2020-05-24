class Object(object):
    def __init__(self):
        self._attributes = []

    def __setitem__(self, key, value):
        if key not in self._attributes:
            self._attributes.append(key)
        self.__setattr__(key, value)

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __iter__(self):
        for item in self._attributes:
            yield item

    def __str__(self):
        result = "{"
        for attr in self._attributes:
            result += "'{key}': '{value}', ".format(key=attr, value=self.__getattribute__(attr))
        result += "}"
        return result
    pass


def RemoveFormatName(text, format_name) -> str:
    remove_from_index = text.find('{' + format_name + ':')
    return text[:remove_from_index] + text[text.find('}', remove_from_index) + 1:]


def GetFormatNames(text) -> list:
    names = []
    start_index = text.find('{')
    end_index = text.find('}', start_index)
    while start_index != -1 and end_index != -1:
        names.append(text[start_index + 1:end_index])
        text = text[:start_index] + text[end_index + 1:]
        start_index = text.find('{')
        end_index = text.find('}', start_index)
    return names


def IsFormatNameInText(text: str, format_name: str) -> bool:
    names = GetFormatNames(text)
    return format_name in names


def GetFormatValues(text, format_name):
    start_index = text.find(':', text.find('{' + format_name + ':'))
    end_index = text.find('}', start_index)
    return text[start_index:end_index]


# format of this function is "'1','2':'3','4'" to [['1','2']['3','4']]
def ConvertStringToSquaredList(text):
    return [(eval("[" + row + "]")) for row in text.split(":")]
