import numpy as np
import markdown
from markupsafe import Markup
from portfolio.faq import faqs
from portfolio import data, genai, co
import re

def extract_raw_text(obj):
    """Recursively extract all keys and string values from nested dict/list."""
    lines = []
    def recurse(o):
        if isinstance(o, str):
            lines.append(o)
        elif isinstance(o, dict):
            for k, v in o.items():
                lines.append(str(k))
                recurse(v)
        elif isinstance(o, list):
            for item in o:
                recurse(item)
    recurse(obj)
    return "\n".join(lines)

def split_into_paragraphs(text):
    """Split text into paragraphs based on double newlines or periods + newline."""
    paragraphs = re.split(r'\n{2,}|(?<=\.)\n', text)
    return [p.strip() for p in paragraphs if p.strip()]

def load_corpus_text():
    faqs_text = "\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in faqs])
    data_text = extract_raw_text(data)
    full_text = faqs_text + "\n" + data_text
    return full_text

corpus_text = load_corpus_text()
corpus_chunks = split_into_paragraphs(corpus_text)

embeddings_cache = co.embed(
    texts=corpus_chunks,
    model="embed-english-v3.0",
    input_type="search_document"
).embeddings

def get_relevant_context(user_input, k=5):
    """Return top-k most relevant corpus chunks for the user query."""
    query_embedding = co.embed(
        texts=[user_input],
        model="embed-english-v3.0",
        input_type="search_query"
    ).embeddings[0]

    scores = np.dot(embeddings_cache, query_embedding)
    top_k_idx = np.argsort(scores)[-k:][::-1]
    return "\n\n".join([corpus_chunks[i] for i in top_k_idx])

def render_markdown(text):
    """Render markdown text to safe HTML for Flask/Jinja."""
    html = markdown.markdown(text)
    return Markup(html)

def ask_gemini(user_input, history, context):
    """Generate chatbot response from Gemini using user input, history, and relevant context."""
    prompt = f"""
You are a helpful chatbot for a developer portfolio website. Use the context to answer accurately. If the question is ambiguous or unclear, ask clarifying questions.

Context:
{context}

Chat History:
{history}

User: {user_input}
"""
    print("Using context for Gemini prompt:\n", context)
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    response = model.generate_content(prompt)
    return render_markdown(response.text.strip())
