from app.rag.retrieval import retrieve
from app.rag.database import LANGUAGE_MODEL
from collections import defaultdict
import ollama


def generate_response(query, top_n=5, strict_quotes=True, debug=False):
    """
    Generate a natural response from retrieved chunks.
    
    In conversational mode, uses an LLM to create human-friendly explanations.
    In strict mode, returns direct quotes formatted as numbered points.
    """
    retrieved = retrieve(query, top_n=top_n)
    
    if not retrieved:
        return "Sorry, I couldn't find relevant information for that question."

    # Debug mode shows raw chunks
    if debug:
        lines = []
        for idx, (chunk, score) in enumerate(retrieved, 1):
            lines.append(f"[Chunk {idx} | Score: {score:.3f}]\n{chunk.strip()}")
        return "DEBUG:\n\n" + "\n\n".join(lines)

    # Conversational mode: LLM generates natural response
    if not strict_quotes:
        source_material = "\n\n".join([f"- {chunk.strip()}" for chunk, _ in retrieved])
        
        system_prompt = f"""You are a Red Cross first aid assistant.
Answer using ONLY the source material below. Do not add external information.

When the source describes steps or procedures, format as clear numbered steps.
When explaining concepts, use natural paragraphs.
Be warm, clear, and professional. Never show chunk numbers.

SOURCE MATERIAL:
{source_material}
"""
        
        try:
            response = ollama.chat(
                model=LANGUAGE_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                options={"temperature": 0.3}
            )
            return response["message"]["content"].strip()
        except Exception as e:
            print(f"LLM error: {e}. Using strict mode.")
            return generate_response(query, top_n, strict_quotes=True, debug=False)

    # Strict mode: Extract relevant sentences
    query_terms = set(query.lower().split())
    chunk_sentences = defaultdict(list)

    for idx, (chunk, _) in enumerate(retrieved):
        for sentence in chunk.split('.'):
            sentence = sentence.strip()
            if not sentence:
                continue
            overlap = query_terms.intersection(sentence.lower().split())
            if overlap:
                chunk_sentences[idx].append(sentence + ".")

    if not chunk_sentences:
        return "No matching information found."
    
    # Format as numbered list
    steps = []
    for i, (chunk_idx, sentences) in enumerate(sorted(chunk_sentences.items()), 1):
        text = " ".join(sentences)
        steps.append(f"{i}. {text}")
    
    return "\n\n".join(steps)
