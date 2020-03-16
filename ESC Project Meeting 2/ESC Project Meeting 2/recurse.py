def recurse(x):
    
    for i in range(70):
        x = x - 1
        recurse(x)
        i = i + 1

recurse(10)