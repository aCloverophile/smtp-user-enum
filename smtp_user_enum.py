import smtplib
import argparse
import os
import re
import socket
import threading
import time
from queue import Queue
from termcolor import colored

def banner():
    print(r"""
        SMTP Username Enumeration Tool v1.0
        Author: Cloverophile
        Note: the script might lead to false positives or need some optimizations. 
              It is highly recommended not to rely on this tool completely 
              and double-check the results to be sure. 
    """)

def is_valid_ip(ip):
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    if re.match(pattern, ip):
        return all(0 <= int(octet) <= 255 for octet in ip.split('.'))
    return False

def is_valid_port(port):
    return 1 <= port <= 65535

def read_usernames(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

def verify_user(smtp_server, smtp_port, username, retries=3, delay=2):
    for attempt in range(retries):
        try:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=15) as server:
                server.ehlo()
                response_code, response_message = server.verify(username)

                if response_code == 250:
                    return username, True, response_message
                elif response_code == 252:
                    return username, "Doubtful", response_message
                else:
                    return username, False, response_message

        except (smtplib.SMTPConnectError, socket.timeout):
            print(f"[!] Connection timeout for {username}, retrying...")
            time.sleep(delay)
            delay *= 2
        except Exception as e:
            return username, None, str(e)

    return username, None, "Maximum retries reached"

def worker():
    while not queue.empty():
        username = queue.get()
        username, is_valid, response = verify_user(smtp_server, smtp_port, username)

        if is_valid is True:
            print(f"[+] {colored(username, 'green')} | Response: {response}")
        elif is_valid == "Doubtful":
            print(f"[?] {colored(username, 'cyan')} | Response: {response}")
        elif is_valid is False:
            print(f"[-] {colored(username, 'red')}")
        else:
            print(f"[!] Error checking {username}: {response}")

        queue.task_done()

def main():
    banner()

    parser = argparse.ArgumentParser(description="SMTP Username Enumeration Tool")
    parser.add_argument("-s", "--server", required=True, help="SMTP server IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="SMTP server port (1-65535)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of concurrent threads (default: 5)")

    args = parser.parse_args()

    global smtp_server, smtp_port, queue

    smtp_server = args.server
    smtp_port = args.port
    wordlist_file = args.wordlist
    num_threads = args.threads

    if not is_valid_ip(smtp_server):
        print(f"Error: Invalid IP address '{smtp_server}'.")
        return

    if not is_valid_port(smtp_port):
        print(f"Error: Invalid port number '{smtp_port}'. Must be between 1 and 65535.")
        return

    if not os.path.isfile(wordlist_file):
        print(f"Error: The file '{wordlist_file}' does not exist.")
        return

    try:
        queue = Queue()

        for username in read_usernames(wordlist_file):
            queue.put(username)

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)

        queue.join()

        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print("\n[!] User interrupted the process.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()