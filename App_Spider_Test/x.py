import json
x = str([{'x':'y'}])
y = json.loads(x)
print(y)
print(type(y))