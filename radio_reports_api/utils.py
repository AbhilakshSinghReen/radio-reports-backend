from uuid import uuid4
from time import time


def unique_str():
    return f"{uuid4()}--{round(time() * 1000)}" 
