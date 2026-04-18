import json

filepath = 'C:/Users/ashis/.gemini/antigravity/scratch/ai-dictionary-app/src/data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace both em-dash and en-dash with commas/spaces to maintain grammatical flow
content = content.replace('—', ', ').replace('–', '-').replace('  ', ' ')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Emdashes removed.")
