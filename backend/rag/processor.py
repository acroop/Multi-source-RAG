# import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
import json
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import List


def create_chunk_by_title(elements) :
    """Create intelligent chunks using title-based strategy."""
    print("Chunking document by titles...")

    chunks = chunk_by_title(
        elements,
        max_characters=3000,
        new_after_n_chars=2400,
        combine_text_under_n_chars=500
    )    

    print(f"Created {len(chunks)} chunks from the document.")
    return chunks




def separate_content_types(chunk):
    """Analyze what types of content are in a chunk"""
    content_data = {
        'text': chunk.text,
        'tables': [],
        'images': [],
        'types': ['text']
    }
    
    # Check for tables and images in original elements
    if hasattr(chunk, 'metadata') and hasattr(chunk.metadata, 'orig_elements'):
        for element in chunk.metadata.orig_elements:
            element_type = type(element).__name__
            
            # Handle tables
            if element_type == 'Table':
                content_data['types'].append('table')
                table_html = getattr(element.metadata, 'text_as_html', element.text)
                content_data['tables'].append(table_html)
            
            # Handle images
            elif element_type == 'Image':
                if hasattr(element, 'metadata') and hasattr(element.metadata, 'image_base64'):
                    content_data['types'].append('image')
                    content_data['images'].append(element.metadata.image_base64)
    
    content_data['types'] = list(set(content_data['types']))
    return content_data

def create_ai_enhanced_summary(text: str, tables: List[str], images: List[str]) -> str:
    """Create AI-enhanced summary for mixed content (TEXT-ONLY LLM SAFE)"""

    try:
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

        prompt_text = f"""
You are creating a searchable description for document content retrieval.

TEXT CONTENT:
{text}
"""

        # Add tables
        if tables:
            prompt_text += "\nTABLES:\n"
            for i, table in enumerate(tables):
                prompt_text += f"\nTable {i+1}:\n{table}\n"

        # Add image placeholders (IMPORTANT)
        if images:
            prompt_text += f"""
IMAGES:
This section contains {len(images)} image(s) such as figures, diagrams, charts, or visual explanations.
Analyze the surrounding text to infer what the images likely represent.
"""

        prompt_text += """
YOUR TASK:
1. Extract key facts, numbers, and findings
2. Identify main topics and concepts
3. List questions this content can answer
4. Infer what images/figures likely explain
5. Add alternative search keywords

Generate a detailed, searchable description.
"""

        response = llm.invoke(prompt_text)
        return response.content

    except Exception as e:
        print(f" AI summary failed: {e}")
        summary = text[:300] + "..."
        if tables:
            summary += f" [Contains {len(tables)} table(s)]"
        if images:
            summary += f" [Contains {len(images)} image(s)]"
        return summary

def summarise_chunks(chunks):
    """Process all chunks with AI Summaries"""
    print(" Processing chunks with AI Summaries...")
    
    langchain_documents = []
    total_chunks = len(chunks)
    
    for i, chunk in enumerate(chunks):
        current_chunk = i + 1
        print(f"   Processing chunk {current_chunk}/{total_chunks}")
        
        # Analyze chunk content
        content_data = separate_content_types(chunk)
        
        # Debug prints
        print(f"     Types found: {content_data['types']}")
        print(f"     Tables: {len(content_data['tables'])}, Images: {len(content_data['images'])}")
        
        # Create AI-enhanced summary if chunk has tables/images
        if content_data['tables'] or content_data['images']:
            print(f"     → Creating AI summary for mixed content...")
            try:
                enhanced_content = create_ai_enhanced_summary(
                    content_data['text'],
                    content_data['tables'], 
                    content_data['images']
                )
                print(f"     → AI summary created successfully")
                print(f"     → Enhanced content preview: {enhanced_content[:200]}...")
            except Exception as e:
                print(f"      AI summary failed: {e}")
                enhanced_content = content_data['text']
        else:
            print(f"     → Using raw text (no tables/images)")
            enhanced_content = content_data['text']
             # Create LangChain Document with rich metadata
        doc = Document(
            page_content=enhanced_content,
            metadata={
                "original_content": json.dumps({
                    "raw_text": content_data['text'],
                    "tables_html": content_data['tables'],
                    "images_base64": content_data['images']
                })
            }
        )
        
        langchain_documents.append(doc)
    
    print(f"Processed {len(langchain_documents)} chunks")
    return langchain_documents

