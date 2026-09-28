"""
Web directory and endpoint enumeration module.
"""

import http.client
import ssl
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional

STATUS_DESCRIPTIONS = {
    200: "OK",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    307: "Temporary Redirect",
    401: "Unauthorized",
    403: "Forbidden",
    500: "Internal Server Error"
}

def check_endpoint(base_url: str, path: str, timeout: float = 3.0) -> Optional[Dict[str, any]]:
    """
    Checks if an HTTP/HTTPS endpoint exists on the target.
    """
    path = "/" + path.lstrip("/")
    url = f"{base_url.rstrip('/')}{path}"
    parsed = urllib.parse.urlparse(url)

    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)

    try:
        if parsed.scheme == "https":
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            conn = http.client.HTTPSConnection(host, port, timeout=timeout, context=context)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=timeout)

        conn.request("GET", path, headers={"User-Agent": "ReconX/1.0"})
        response = conn.getresponse()
        status = response.status
        conn.close()

        # Report interesting HTTP statuses (success, redirects, auth boundaries)
        if status in (200, 204, 301, 302, 307, 401, 403):
            return {
                "path": path,
                "url": url,
                "status": status,
                "reason": response.reason or STATUS_DESCRIPTIONS.get(status, "")
            }
    except (http.client.HTTPException, OSError):
        return None
    except KeyboardInterrupt:
        raise
    return None

def run_dir_scan(
    target: str,
    wordlist_path: str,
    use_https: bool = False,
    port: Optional[int] = None,
    max_workers: int = 20,
    timeout: float = 3.0
) -> List[Dict[str, any]]:
    """
    Runs directory enumeration using paths from wordlist.
    """
    scheme = "https" if use_https or port == 443 else "http"
    if port and port not in (80, 443):
        base_url = f"{scheme}://{target}:{port}"
    else:
        base_url = f"{scheme}://{target}"

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            paths = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

    discovered = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_endpoint, base_url, p, timeout): p for p in paths}
        for future in futures:
            try:
                res = future.result()
                if res:
                    discovered.append(res)
            except KeyboardInterrupt:
                executor.shutdown(wait=False, cancel_futures=True)
                raise

    return discovered
