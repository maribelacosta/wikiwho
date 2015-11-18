import os
print(__file__)
print(os.path.realpath(__file__))
print(os.path.realpath(__file__)[:-1*len(__file__)])
