import re


def test(**kwargs) -> str:
    print(kwargs)
    return 1
t = test(a=1,b=2)
print(type(t))