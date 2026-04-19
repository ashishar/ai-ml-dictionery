with open('src/data.js', 'rb') as f:
    lines = f.readlines()
    line = lines[2794] # 0-indexed
    print(line)
