import json
import random

filepath = 'C:/Users/ashis/.gemini/antigravity/scratch/ai-dictionary-app/src/data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
terms = json.loads(json_str)

prefixes = [
    "As illustrated in the technical figure, ",
    "The accompanying schematic visualizes how ",
    "Looking at the architecture diagram above, ",
    "The visual representation highlights that ",
    "The embedded flowchart breaks down ",
    "Observe the structural mapping shown in the image, where ",
    "This concept is visually modeled in the figure, demonstrating that ",
    "The graphical diagram provides a clear layout of the architecture, showing how ",
    "As depicted in the provided illustration, ",
    "The mathematical graph above charts out how ",
    "The architecture shown in the diagram details ",
    "Analyzing the visual schematic, it becomes apparent that "
]

for term in terms:
    # 1. Vary the text
    img_ref = term["structuredDefinition"].get("imageRef", "")
    
    # Check if the specific generic fallback exists
    if "Referring to the provided technical diagram, " in img_ref:
        img_ref = img_ref.replace("Referring to the provided technical diagram, ", random.choice(prefixes))
    elif "Referring to the iconic technical diagram, " in img_ref:
        img_ref = img_ref.replace("Referring to the iconic technical diagram, ", random.choice(prefixes))
    else:
        # If it doesn't have our strict old prefix, prepend a new random one if it doesn't already have one
        has_prefix = any(p in img_ref for p in prefixes)
        if not has_prefix:
            # We don't want to blindly prepend if it ruins the grammar, but for our dataset, prepending is safe.
            img_ref = random.choice(prefixes) + img_ref
            
    # Quick cleanup in case of capitalization mismatch
    img_ref = img_ref.replace(" ,", ",")
    term["structuredDefinition"]["imageRef"] = img_ref
    
    # 2. Add Related Terms (5 terms)
    same_category = [t["id"] for t in terms if t["category"] == term["category"] and t["id"] != term["id"]]
    if len(same_category) < 5:
        others = [t["id"] for t in terms if t["id"] != term["id"] and t["id"] not in same_category]
        same_category.extend(random.sample(others, 5 - len(same_category)))
        
    term["relatedTerms"] = random.sample(same_category, 5)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('export const dictionaryData = ')
    f.write(json.dumps(terms, indent=2))
    f.write(';\n')

print("Varied image references and added related terms.")
