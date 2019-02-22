class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = "z"


class EventGet:
    def __init__(self, type):
        self._type = type


class EventSet:
    def __init__(self, value):
        self._value = value


class NullHandler:
    def __init__(self, node=None):
        self.__node = node

    def handle(self, obj, event):
        if self.__node is not None:
            return self.__node.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventSet) and type(event._value).__name__ == 'int':
                obj.integer_field = event._value
                return
        elif isinstance(event, EventGet) and event._type.__name__ == 'int':
            return obj.integer_field

        print('pass on')
        return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventSet) and type(event._value).__name__ == 'float':
            obj.float_field = event._value
            return
        elif isinstance(event, EventGet) and event._type.__name__ == 'float':
            return obj.float_field

        print('pass on')
        return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventSet) and type(event._value).__name__ == 'str':
                obj.string_field = event._value
                return
        elif isinstance(event, EventGet) and event._type.__name__ == 'str':
            return obj.string_field

        print('pass on')
        return super().handle(obj, event)



chain = IntHandler(FloatHandler(StrHandler(NullHandler())))


obj = SomeObject()
print(chain.handle(obj, EventGet(int)), end='\n\n')
print(chain.handle(obj, EventGet(str)), end='\n\n')
print(chain.handle(obj, EventGet(float)), end='\n\n')

chain.handle(obj, EventSet(1))
print('int', obj.integer_field)
print('float', obj.float_field)
print('str', obj.string_field)

chain.handle(obj, EventSet(1.1))
print('int', obj.integer_field)
print('float', obj.float_field)
print('str', obj.string_field)

chain.handle(obj, EventSet('str'))
print('int', obj.integer_field)
print('float', obj.float_field)
print('str', obj.string_field)