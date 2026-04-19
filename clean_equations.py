import re

def clean_equations():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove all $ from "equation" values
    def remove_dollars(match):
        eq = match.group(1)
        clean_eq = eq.replace('$', '')
        return f'"equation": "{clean_eq}"'

    content = re.sub(r'"equation": "(.*?)"', remove_dollars, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

clean_equations()
print("Equation field cleanup completed.")
