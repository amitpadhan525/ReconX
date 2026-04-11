# ReconX

ReconX is an advanced reconnaissance tool written in Python. It is designed to perform network scanning and enumerate services effectively.

## Features

- **Port Scanning**: Scan a target IP or domain for open ports within a specified range.
- **Banner Grabbing**: Automatically attempt to grab the banner/service information of any discovered open ports.

## Requirements

- Python 3.x

## Installation

Clone the repository:

```bash
git clone https://github.com/amitpadhan525/ReconX.git
cd ReconX
```

## Usage

```bash
python3 reconx.py -t <target> -p <port_range>
```

### Arguments:
- `-t`, `--target`: Target IP or domain to scan (Required)
- `-p`, `--ports`: Port range to scan (e.g., `1-1000`)

### Example:

```bash
python3 reconx.py -t 192.168.185.128 -p 1-100000
```

### Output Example:
```text
Target: 192.168.185.128

[PORT SCAN]
21    -> OPEN | 220 (vsFTPd 2.3.4)
22    -> OPEN | SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1
80    -> OPEN | HTTP/1.1 200 OK
1524  -> OPEN | root@metasploitable:/#
Total OPEN ports 4
```

## Planned Features
- Directory Scanning / Fuzzing
