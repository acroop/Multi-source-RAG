from langchain_groq import ChatGroq
import json
from dotenv import load_dotenv
load_dotenv()


def generate_final_answer(chunks, query):
    """Generate final answer using text-only compatible prompt"""

    try:
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

        prompt_text = f"""
Based on the following documents, answer the question:

QUESTION:
{query}

DOCUMENTS:
"""

        for i, chunk in enumerate(chunks):
            prompt_text += f"\n--- Document {i+1} ---\n"

            if "original_content" in chunk.metadata:
                original_data = json.loads(chunk.metadata["original_content"])

                # Raw text
                raw_text = original_data.get("raw_text", "")
                if raw_text:
                    prompt_text += f"TEXT:\n{raw_text}\n"

                # Tables
                tables_html = original_data.get("tables_html", [])
                if tables_html:
                    prompt_text += "\nTABLES:\n"
                    for j, table in enumerate(tables_html):
                        prompt_text += f"Table {j+1}:\n{table}\n"

                # Images → TEXT description
                images_base64 = original_data.get("images_base64", [])
                if images_base64:
                    prompt_text += f"""
IMAGES:
This document contains {len(images_base64)} image(s) such as figures, diagrams, or charts.
Use the surrounding text to infer what these images explain.
"""

        prompt_text += """
INSTRUCTIONS:
- Answer strictly based on the documents above
- If the answer is not present, say you do not have enough information
- Be concise and factual

FINAL ANSWER:
"""

        response = llm.invoke(prompt_text)
        return response.content

    except Exception as e:
        print(f" Answer generation failed: {e}")
        return "Sorry, I encountered an error while generating the answer."
