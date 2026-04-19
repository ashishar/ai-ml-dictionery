import re

def fix_syntax_error():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue is '\u' followed by a space or something that isn't 4 hex digits.
    # We should probably just replace these corrupted sequences with their intended LaTeX or characters.
    
    # Common corrupted patterns from my previous scripts
    content = content.replace(r'\u $ 03b', r'\lambda') # Elastic Net often uses lambda
    content = content.replace(r'\u $03b', r'\lambda')
    content = content.replace(r'\u ', r'\\u ') # Escape it so it's a literal backslash u
    
    # Also fix the equation field that had a $ at the start
    content = re.sub(r'"equation": "\$(.*?)\$"', r'"equation": "\1"', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_syntax_error()
print("Syntax error fix applied.")
