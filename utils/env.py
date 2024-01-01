import os

def env(name):
    val = os.getenv(name)
    if val != None:
        return val
    else: 
        return ""
