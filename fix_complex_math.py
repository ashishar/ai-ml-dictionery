import json
import re

def fix_complex_math_notation():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_math_blocks(match):
        text = match.group(1)
        
        # 1. Protect existing $ content
        placeholders = []
        def save_placeholder(m):
            placeholders.append(m.group(0))
            return "__MATH_" + str(len(placeholders)-1) + "__"
        
        text = re.sub(r'\$[^\$]+\$', save_placeholder, text)

        # 2. Identify and wrap P(w_t | w_{1:t-1}) and similar
        text = re.sub(r'\bP\([a-zA-Z0-9_|:_{}\s-]+\)', lambda m: "$" + m.group(0) + "$", text)
        
        # 3. Identify words with subscripts/superscripts/braces
        text = re.sub(r'\b[a-zA-Z][a-zA-Z0-9_{}:^]*_[a-zA-Z0-9_{}:^]*\b', lambda m: "$" + m.group(0) + "$", text)
        text = re.sub(r'\b[a-zA-Z][a-zA-Z0-9_{}:^]*\^[a-zA-Z0-9_{}:^]*\b', lambda m: "$" + m.group(0) + "$", text)

        # 4. Restore placeholders
        for i, val in enumerate(placeholders):
            text = text.replace("__MATH_" + str(i) + "__", val)
            
        # 5. Clean up nesting
        text = text.replace('$$', '$')
        
        # 6. Specifically fix the P(w_t | w_{1:t-1}) issue
        # Using lambda to avoid backreference escape issues
        text = re.sub(r'\$P\(\$([^\$]+)\$\s?\|\s?([^\$]+)\)\$', 
                      lambda m: "$P(" + m.group(1) + " \\mid " + m.group(2) + ")$", text)
        text = re.sub(r'P\(\$([^\$]+)\$\s?\|\s?([^\$]+)\)', 
                      lambda m: "$P(" + m.group(1) + " \\mid " + m.group(2) + ")$", text)

        # 7. Final pass on | inside $ to turn into \mid
        text = re.sub(r'\$([^\$]+\|[^\$]+)\$', 
                      lambda m: "$" + m.group(1).replace('|', " \\mid ") + "$", text)

        # 8. Clean up double spaces and double $$
        text = text.replace('$$', '$')
        text = text.replace('  ', ' ')
        
        return '"equationVars": "' + text + '"'

    new_content = re.sub(r'"equationVars": "(.*?)"', replace_math_blocks, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_complex_math_notation()
print("Surgical fix for complex math notations applied with safe lambda replacements.")
