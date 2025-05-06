import markdown
from markupsafe import Markup
from portfolio.faq import faqs
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai
from portfolio.config import Config
from portfolio import data

model = SentenceTransformer("all-MiniLM-L6-v2")
genai.configure(api_key=Config.API_KEY)

def load_all_text():

    faqs_text = [f"Q: {f['question']}\nA: {f['answer']}" for f in faqs]

    def extract_strings(obj):
        strings = []
        if isinstance(obj, str):
            strings.append(obj)
        elif isinstance(obj, dict):
            for v in obj.values():
                strings.extend(extract_strings(v))
        elif isinstance(obj, list):
            for item in obj:
                strings.extend(extract_strings(item))
        return strings

    data_text = extract_strings(data)

    return faqs_text + data_text

sentences_cache = load_all_text()
embeddings_cache = model.encode(sentences_cache, convert_to_tensor=True)

def get_relevant_context(user_input, k=5):
    query_embedding = model.encode(user_input, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, embeddings_cache, top_k=k)[0]
    return "\n".join([sentences_cache[hit['corpus_id']] for hit in hits])

def render_markdown(text):
    html = markdown.markdown(text)
    return Markup(html)

def ask_gemini(user_input, history, context):
    prompt = f"""
You are a helpful chatbot for a developer portfolio website. Use the context to answer accurately. In case of ambiguity, ask clarifying questions. If the user asks about a specific project, provide details about that project. If the user asks about a technology, provide a brief overview of that technology. If the user asks about a specific topic, provide relevant information from the context. If the user asks about a specific person, provide relevant information from the context. If the user asks about a specific date, provide relevant information from the context. If the user asks about a specific location, provide relevant information from the context. If the user asks about a specific technology stack, provide relevant information from the context. If you can't answer, ask user to contact the developer directly.

Context:
{context}

Chat History:
{history}

User: {user_input}
"""

    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    response = model.generate_content(prompt)
    markdown_response = render_markdown(response.text.strip())
    return markdown_response
