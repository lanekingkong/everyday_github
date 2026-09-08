"""
Multi-threaded TCP Port Scanner with banner grabbing and service detection.
"""
import socket
import threading
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


COMMON_PORTS = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    465: "SMTPS", 587: "SMTP", 993: "IMAPS", 995: "POP3S",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 9090: "Prometheus", 27017: "MongoDB",
}

SERVICE_PROBES = {
    "HTTP": b"GET / HTTP/1.0\r\n\r\n",
    "SSH": b"",
    "SMTP": b"EHLO scanner\r\n",
    "FTP": b"",
}


def scan_port(host: str, port: int, timeout: float = 1.0) -> dict:
    """Scan a single port; return result dict."""
    result = {
        "host": host, "port": port,
        "service": COMMON_PORTS.get(port, "unknown"),
        "open": False, "banner": None,
    }
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        if sock.connect_ex((host, port)) == 0:
            result["open"] = True
            # Try banner grabbing
            service = COMMON_PORTS.get(port, "")
            probe = SERVICE_PROBES.get(service if service in SERVICE_PROBES else "", None)
            if probe:
                try:
                    sock.send(probe)
                    banner = sock.recv(1024)
                    result["banner"] = banner.decode("utf-8", errors="replace").strip()[:200]
                except Exception:
                    pass
            elif service == "SSH":
                try:
                    banner = sock.recv(256)
                    result["banner"] = banner.decode("utf-8", errors="replace").strip()
                except Exception:
                    pass
        sock.close()
    except Exception as e:
        result["error"] = str(e)
    return result


def scan_range(host: str, start: int = 1, end: int = 1024, workers: int = 100, timeout: float = 0.5):
    """Scan a range of ports with thread pool."""
    ports = list(range(start, end + 1))
    results = []
    total = len(ports)
    done = 0
    open_ports = []

    print(f"\n🔍 Scanning {host} — ports {start}-{end} ({total} ports, {workers} workers)\n")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(scan_port, host, p, timeout): p for p in ports}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result["open"]:
                open_ports.append(result)
                banner = f" [{result['banner'][:60]}]" if result["banner"] else ""
                print(f"  ✅ {result['port']:>5}/{result['service']:<15}{banner}")
            done += 1
            if done % 200 == 0:
                print(f"     ... {done}/{total} scanned, {len(open_ports)} open")

    return results


def export_results(results, filename: str, fmt: str = "json"):
    """Export results to JSON or HTML."""
    if fmt == "json":
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
    elif fmt == "html":
        open_ports = [r for r in results if r["open"]]
        html = f"""<!DOCTYPE html>
<html><head><title>Port Scan Results</title>
<style>
    body {{ font-family: system-ui; margin: 2rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #ddd; }}
    th {{ background: #2563eb; color: white; }}
    tr:hover {{ background: #f0f9ff; }}
</style></head><body>
<h1>Port Scan: {results[0]['host'] if results else ''}</h1>
<p>Scanned: {len(results)} ports | Open: {len(open_ports)} | {datetime.now().isoformat()}</p>
<table>
<tr><th>Port</th><th>Service</th><th>Banner</th></tr>
"""
        for r in open_ports:
            html += f"<tr><td>{r['port']}</td><td>{r['service']}</td><td>{r.get('banner', '') or ''}</td></tr>"
        html += "</table></body></html>"
        with open(filename, "w") as f:
            f.write(html)
    print(f"\n📄 Results exported to {filename}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Multi-threaded Port Scanner")
    parser.add_argument("host", nargs="?", default="127.0.0.1", help="Target host")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port")
    parser.add_argument("-w", "--workers", type=int, default=100, help="Thread count")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Timeout per port")
    parser.add_argument("-o", "--output", default="scan_results.json")
    parser.add_argument("--html", action="store_true", help="Export as HTML")
    args = parser.parse_args()

    results = scan_range(args.host, args.start, args.end, args.workers, args.timeout)
    open_ports = [r for r in results if r["open"]]

    print(f"\n{'='*50}")
    print(f"  Scan complete: {len(open_ports)}/{len(results)} ports open")
    print(f"{'='*50}\n")

    fmt = "html" if args.html else "json"
    export_results(results, args.output, fmt)
