import requests
import os
from tempfile import NamedTemporaryFile
from unstructured.partition.pdf import partition_pdf

def partition_document_from_url(pdf_url: str):
    response = requests.get(pdf_url)
    response.raise_for_status()

    tmp = NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        tmp.write(response.content)
        tmp.close() 

        elements = partition_pdf(
            filename=tmp.name,
            strategy="hi_res",
            infer_table_structure=True,
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
        )

        return elements

    finally:
        os.remove(tmp.name)  # cleanup
