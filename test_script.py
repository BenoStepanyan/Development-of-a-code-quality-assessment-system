import os
# ՍԽԱԼ 1: Wildcard import (արգելված է PEP8-ով)
from math import * 

# ՍԽԱԼ 2: Դասի անունը սկսվում է փոքրատառով
class badNamedClass:
    def __init__(self):
        self.data = []

# ՍԽԱԼ 3 և 4: Ֆունկցիան շատ երկար է և ունի բարձր բարդություն
def complex_and_long_function(x):
    print('Start process')
    result = 0
    
    # Արհեստականորեն ավելացված բարդություն (if/else)
    if x > 0:
        result += 1
    elif x < 0:
        result -= 1
    
    if x == 10:
        print("Ten")
    if x == 20:
        print("Twenty")
    
    for i in range(5):
        result += i
        if result > 100:
            print("Overflow")
            
    while result < 50:
        result += 1
        if result == 40:
            break
            
    # Ավելորդ տողեր՝ երկարությունը 20-ից ավել դարձնելու համար
    print("Step 1 complete")
    print("Step 2 complete")
    print("Step 3 complete")
    print("Step 4 complete")
    print("Step 5 complete")
    print("Step 6 complete")
    return result
