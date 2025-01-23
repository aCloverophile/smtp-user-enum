# SMTP Username Enumeration Tool

## Description
The **SMTP Username Enumeration Tool**, is a Python-based utility designed to enumerate SMTP server usernames using the VRFY command. The tool attempts to verify a list of usernames against a specified SMTP server and port, providing insights into valid, doubtful, or invalid usernames.

**The tool has been developed to solve the SMTP username brute-force exercise in the "Footprinting" module of HTB Academy.**

**Disclaimer:** This tool may produce false positives and should not be relied upon entirely. Always double-check results manually.

## Requirements
- Python 3.x
- Required Python libraries:
  - `smtplib`
  - `argparse`
  - `os`
  - `re`
  - `socket`
  - `threading`
  - `time`
  - `queue`
  - `termcolor`

Install required dependencies using:
```bash
pip install termcolor
```

## Usage
### Command-line Arguments
```bash
python3 smtp_user_enum.py -s <SMTP_SERVER_IP> -p <SMTP_PORT> -w <WORDLIST_FILE> [-t <NUM_THREADS>]
```

### Options
| Argument          | Description                              | Required | Example               |
|------------------|------------------------------------------|----------|-----------------------|
| `-s`, `--server`  | SMTP server IP address                   | Yes      | `192.168.1.100`        |
| `-p`, `--port`    | SMTP server port (1-65535)               | Yes      | `25`                   |
| `-w`, `--wordlist`| Path to the username wordlist file       | Yes      | `usernames.txt`        |
| `-t`, `--threads` | Number of concurrent threads (default 5) | No       | `10`                   |

### Example Usage
```bash
python3 smtp_user_enum.py -s 192.168.1.100 -p 25 -w usernames.txt -t 10
```

## Output
The tool provides color-coded output for different verification responses:
- **Green ([+])**: Verified username (code 250)
- **Cyan ([?])**: Doubtful response (code 252)
- **Red ([-])**: Invalid username
- **Yellow ([!])**: Errors encountered

## License
This project is for educational purposes only. The author is not responsible for any misuse.