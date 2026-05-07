import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from ports.outbound.scanner_port import ScannerPort
from domain.entities.chunk import DocumentChunk

class BS4Scanner(ScannerPort):
    def scan(self, url: str, max_pages: int) -> list[DocumentChunk]:
        base_domain = urlparse(url).netloc
        to_visit = [url]
        visited = set()
        all_chunks = []
        chunk_index = 0

        while to_visit and len(visited) < max_pages:
            current_url = to_visit.pop(0)
            if current_url in visited:
                continue
            visited.add(current_url)

            try:
                response = requests.get(current_url, timeout=8)
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                for tag in soup.find_all("a", href=True):
                    full_url = urljoin(url, tag["href"])
                    parsed = urlparse(full_url)
                    skip = [".pdf", ".jpg", ".png", ".zip", "#", "mailto:", "tel:"]
                    if parsed.netloc == base_domain and full_url not in visited:
                        if not any(s in full_url for s in skip):
                            to_visit.append(full_url)

                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()

                words = soup.get_text(separator=" ", strip=True).split()
                for i in range(0, len(words), 150):
                    chunk_text = " ".join(words[i:i + 150])
                    if len(chunk_text.strip()) < 50:
                        continue
                    all_chunks.append(DocumentChunk(
                        content=chunk_text,
                        source=current_url,
                        chunk_index=chunk_index
                    ))
                    chunk_index += 1

                print(f"  ✓ {current_url}")

            except Exception as e:
                print(f"  ✗ {current_url}: {e}")

        return all_chunks