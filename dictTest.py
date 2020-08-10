
import json

# class DictWatch(dict):
#     def __init__(self, *args, **kwargs):
#         self.update(*args, **kwargs)

#     def __getitem__(self, key):
#         val = dict.__getitem__(self, key)
#         return val

#     def __setitem__(self, key, val):
#         dict.__setitem__(self, key, val)

#     def __repr__(self):
#         dictrepr = dict.__repr__(self)
#         return '%s(%s)' % (type(self).__name__, dictrepr)

#     def update(self, *args, **kwargs):
#         for k, v in dict(*args, **kwargs).items():
#             self[k] = v


# print(DictWatch(test1="1",test2="2",test3="3"))

x = [{"x":"1", "y": "2"},{"x":"1", "y": "2"}]


teststr = ""
pre = ""
for chunk in json.JSONEncoder().iterencode(x):

    if (chunk[0] == "," and pre[0] == "}"):
        teststr += chunk 
        teststr += '\n'
    else:
        teststr += chunk
    pre = chunk
    print (pre[0])


print(teststr)


# class JsonTest(json.JSONEncoder):
#     def default(self, o):
#         try:
#             iterable = iter(o)
#             print(o)
#         except TypeError:
#             pass
#         else:
#             return list(iterable)
#         # Let the base class default method raise the TypeError
#         return json.JSONEncoder.default(self, o)


# print(JsonTest().default(x))

