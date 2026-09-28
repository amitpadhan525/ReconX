# ReconX

**ReconX** is a modular, multi-threaded network reconnaissance and asset discovery tool written in Python. It helps security analysts and network administrators identify exposed attack surfaces, open ports, running services, and web endpoints.

---

## ✨ Features

- **Port Scanning**: Multi-threaded TCP port scanner with flexible port definitions (single, ranges, lists, e.g. `80`, `1-1000`, `80,443,8000-8080`).
- **Service Banner Grabbing**: Identifies active services, software banners, and HTTP/HTTPS headers.
- **Web Directory Enumeration**: Discovers exposed endpoints and web directories using customizable wordlists.
- **Target Resolution**: Automatically validates and resolves hostnames/domains to IP addresses.
- **JSON Export**: Automatically outputs structured scan results to a JSON file for downstream tools or reporting.
- **ANSI Color Terminal Output**: Clear, color-coded terminal interface with banner formatting.

---

## 📦 Requirements

- Python 3.8+ (Uses standard library; no external dependencies required)

---

## 🚀 Installation

```bash
git clone https://github.com/amitpadhan525/ReconX.git
cd ReconX
```

---

## 🛠️ Usage

```bash
python3 reconx.py -t <target> [options]
```

### Options:

| Flag | Argument | Description |
| :--- | :--- | :--- |
| `-t`, `--target` | `<host/ip>` | **(Required)** Target hostname or IP address |
| `-p`, `--ports` | `<ports>` | Ports to scan (e.g., `80`, `80,443`, `1-1000`, `21,22,80-100`) |
| `-d`, `--dir` | `[wordlist]` | Wordlist for web directory scan (default: `wordlists/common.txt`) |
| `--ssl` | - | Force HTTPS for directory scanning |
| `-o`, `--output` | `<file>` | Output JSON results path (default: `output/results.json`) |
| `-w`, `--workers` | `<num>` | Concurrency worker threads (default: `150`) |
| `--timeout` | `<sec>` | Socket timeout in seconds (default: `1.0`) |

---

### 📖 Examples

#### 1. Quick Port Scan & Banner Grabbing
```bash
python3 reconx.py -t 192.168.1.1 -p 1-1000
```

#### 2. Specific Ports Scan
```bash
python3 reconx.py -t example.com -p 21,22,80,443,8080
```

#### 3. Web Directory Enumeration
```bash
python3 reconx.py -t example.com -d wordlists/common.txt --ssl
```

#### 4. Full Reconnaissance with Custom Output
```bash
python3 reconx.py -t example.com -p 80,443,8000-8080 -d -o output/scan.json
```

---

## 📂 Project Structure

```
ReconX/
├── reconx.py                  # Main CLI entrypoint
├── modules/
│   ├── port_scanner.py        # Multi-threaded TCP port scanner
│   ├── banner_grabber.py      # Banner & service identifier
│   └── dir_scanner.py         # HTTP/HTTPS directory enumerator
├── utils/
│   ├── helpers.py             # Target resolution, port parsing, and export utils
│   └── logger.py              # Colored terminal output and ASCII banner
├── wordlists/
│   └── common.txt             # Built-in directory wordlist
├── output/
│   └── results.json           # Output scan report
└── README.md
```
