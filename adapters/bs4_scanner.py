import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from domain.ports.scanner_port import ScannerPort
from domain.models import DocumentChunk

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

                # Find all internal links and add to queue
                for tag in soup.find_all("a", href=True):
                    href = tag["href"]
                    full_url = urljoin(url, href)
                    parsed = urlparse(full_url)

                    # Only follow links on the same domain
                    if parsed.netloc == base_domain and full_url not in visited:
                        # Skip non-content pages
                        skip = [".pdf", ".jpg", ".png", ".zip", 
                                "#", "mailto:", "tel:", "javascript:"]
                        if not any(s in full_url for s in skip):
                            to_visit.append(full_url)

                # Remove noise tags
                for tag in soup(["script", "style", "nav", 
                                 "footer", "header", "meta"]):
                    tag.decompose()

                text = soup.get_text(separator=" ", strip=True)

                # Split into chunks
                words = text.split()
                chunk_size = 150
                for i in range(0, len(words), chunk_size):
                    chunk_text = " ".join(words[i:i + chunk_size])
                    if len(chunk_text.strip()) < 50:
                        continue
                    all_chunks.append(DocumentChunk(
                        content=chunk_text,
                        source=current_url,
                        chunk_index=chunk_index
                    ))
                    chunk_index += 1

                print(f"  ✓ Scraped {current_url} — {len(visited)} pages so far")

            except Exception as e:
                print(f"  ✗ Could not fetch {current_url}: {e}")
                continue

        return all_chunks