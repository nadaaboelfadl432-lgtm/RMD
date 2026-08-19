import requests
import xml.etree.ElementTree as ET

from langchain_core.documents import Document


BASE_URL = "https://wsearch.nlm.nih.gov/ws/query"


def fetch_medlineplus(topic):
    params = {
        "db": "healthTopics",
        "term": topic,
        "rettype": "topic",
        "retmax": 5,
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def parse_medlineplus(xml_data):
    root = ET.fromstring(xml_data)

    documents = []

    for document in root.findall(".//document"):

        title = document.findtext("content[@name='title']", default="")

        url = document.findtext("content[@name='url']", default="")

        content_parts = []

        for content in document.findall("content"):
            name = content.get("name", "")

            if name not in ["title", "url"]:
                text = "".join(content.itertext()).strip()

                if text:
                    content_parts.append(text)

        page_content = "\n\n".join(content_parts)

        if page_content:
            doc = Document(
            page_content=page_content,
            metadata={
    "document_name": title or "MedlinePlus",
    "source": "MedlinePlus",
    "source_url": url,
    "section": "N/A",
}
)

            documents.append(doc)

    return documents


def main():

    print("Fetching MedlinePlus data...")

    xml_data = fetch_medlineplus("hypertension")

    documents = parse_medlineplus(xml_data)

    print(f"\nCreated {len(documents)} documents.\n")

    for i, doc in enumerate(documents, 1):

        print("=" * 60)
        print(f"Document {i}")
        print("=" * 60)

        print("Title:")
        print(doc.metadata["document_name"])

        print("\nURL:")
        print(doc.metadata["source_url"])

        print("\nContent:")
        print(doc.page_content[:1000])


if __name__ == "__main__":
    main()
    