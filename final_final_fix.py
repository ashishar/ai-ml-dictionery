import re

def final_final_fix():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Targeted regex for line 2394
    content = re.sub(r'max\s+\$\s+Q\(s\',a\'\)\$', r'$\\max_{a\'} Q(s\', a\')$', content)
    
    # Also fix the alpha spacing in 2394
    content = content.replace(r'$\alpha$ (alpha)', r'$\alpha$ (alpha)')
    
    # Fix 1322
    content = content.replace(r'$ F_m (x)', r'$F_m(x)$')
    
    # Ensure no $ in equations
    def clean_eq(match):
        eq = match.group(1)
        return f'"equation": "{eq.replace("$", "")}"'
    content = re.sub(r'"equation": "(.*?)"', clean_eq, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

final_final_fix()
print("Final final fix completed.")
