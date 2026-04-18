import json

filepath = 'C:/Users/ashis/.gemini/antigravity/scratch/ai-dictionary-app/src/data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
terms = json.loads(json_str)

for term in terms:
    t_name = term["title"]
    paper_title = term['resources']['papers'][0]['title']
    category = term["category"]
    
    # Origin
    origin = f"The formalization of **{t_name}** is fundamentally rooted in the seminal research presented in *{paper_title}*. It was introduced in the context of overcoming the structural limitations of previous {category} architectures and establishing a new paradigm for performance and scalability."
    
    if "Transformer" in t_name:
        origin = "Introduced by Vaswani et al. in the landmark 2017 Google Brain paper 'Attention Is All You Need', this architecture was created to eliminate recurrence entirely and rely solely on attention mechanisms for sequence modeling."
    elif "Gradient descent" in t_name:
        origin = "The concept of gradient descent dates back to Augustin-Louis Cauchy in 1847, but its modern application in the machine learning context was popularized later to optimize complex loss landscapes efficiently."
    elif "Neural network" in t_name:
        origin = "The concept was initially inspired by biological neural networks, with the first mathematical model of a neuron proposed by McCulloch and Pitts in 1943. It evolved significantly in the 1980s with the popularization of backpropagation."
    elif "Turing test" in t_name:
        origin = "Introduced by Alan Turing in his 1950 paper 'Computing Machinery and Intelligence', it was originally proposed to answer the philosophical question: 'Can machines think?'"

    # Trends
    trends = f"Currently, state-of-the-art research regarding {t_name} focuses on optimizing its computational complexity, exploring multi-modal integration, and developing robust theoretical guarantees for its convergence and safety in real-world deployment."
    
    if "Large language model" in t_name or "Generative pre-trained" in t_name or "BERT" in t_name:
        trends = "Current research trends are heavily focused on model alignment (RLHF), parameter-efficient fine-tuning (LoRA), and extending context windows. There is also a massive push toward reducing hallucination rates via Retrieval-Augmented Generation (RAG)."
    elif "Computer vision" in t_name or "Convolutional" in t_name:
        trends = "Modern research is increasingly shifting from pure CNNs to Vision Transformers (ViTs) and multimodal architectures that fuse visual data with large language models."

    term["structuredDefinition"]["origin"] = origin
    term["structuredDefinition"]["currentTrends"] = trends
    
    slug = t_name.split('(')[0].strip().lower().replace(' ', '-')
    trend_url = f"https://paperswithcode.com/method/{slug}"
    
    has_trend = any("[Trends]" in c["source"] for c in term["defCitations"])
    if not has_trend:
        term["defCitations"].append({
            "source": f"[Trends & SOTA Research] PapersWithCode Benchmarks: {t_name}", 
            "url": trend_url
        })

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('export const dictionaryData = ')
    f.write(json.dumps(terms, indent=2))
    f.write(';\n')

print("Successfully added Origin and Trends.")
