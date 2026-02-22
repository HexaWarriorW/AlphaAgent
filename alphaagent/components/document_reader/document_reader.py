from __future__ import annotations

import io
from pathlib import Path
from typing import TYPE_CHECKING

import fitz
import requests
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from PIL import Image

if TYPE_CHECKING:
    from langchain_core.documents import Document


def load_documents_by_langchain(path: str) -> list:
    """Load documents from the specified path.

    Args:
        path (str): The path to the directory or file containing the documents.

    Returns:
        list: A list of loaded documents.
    """
    if Path(path).is_dir():
        loader = PyPDFDirectoryLoader(path, silent_errors=True)
    else:
        loader = PyPDFLoader(path)
    return loader.load()


def process_documents_by_langchain(docs: list[Document]) -> dict[str, str]:
    """Process a list of documents and group them by document name.

    Args:
        docs (list): A list of documents.

    Returns:
        dict: A dictionary where the keys are document names and the values are
        the concatenated content of the documents.
    """
    content_dict = {}

    for doc in docs:
        if Path(doc.metadata["source"]).exists():
            doc_name = str(Path(doc.metadata["source"]).resolve())
        else:
            doc_name = doc.metadata["source"]
        doc_content = doc.page_content

        if doc_name not in content_dict:
            content_dict[str(doc_name)] = doc_content
        else:
            content_dict[str(doc_name)] += doc_content

    return content_dict


def load_and_process_pdfs_by_langchain(path: str) -> dict[str, str]:
    return process_documents_by_langchain(load_documents_by_langchain(path))



def extract_first_page_screenshot_from_pdf(pdf_path: str) -> Image:
    if not Path(pdf_path).exists():
        doc = fitz.open(stream=io.BytesIO(requests.get(pdf_path).content), filetype="pdf")
    else:
        doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    return image
