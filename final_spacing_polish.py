import re

def final_spacing_polish():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add space after period if followed by $
    content = re.sub(r'\.([\$])', r'. \1', content)
    
    # 2. Add space after $...$ if followed by a letter
    content = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', content)
    
    # 3. Add space before $...$ if preceded by a letter (and not a $)
    content = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', content)

    # 4. Clean up the specific g(f(x)) issue if it exists
    content = content.replace('$g(f(x)$)', '$g(f(x))$')
    content = content.replace('$f(x)$)', '$f(x)$') # Cleanup potential artifacts

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

final_spacing_polish()
print("Final spacing polish applied.")
