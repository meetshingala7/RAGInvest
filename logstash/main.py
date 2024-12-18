import socket
import json


def send_log_to_logstash(log_message):
    logstash_host = "localhost"
    logstash_port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((logstash_host, logstash_port))
        log_entry = json.dumps(log_message) + "\n"
        sock.sendall(log_entry.encode("utf-8"))
    finally:
        sock.close()


# Example log message
log_message = {
    "level": "INFO",
    "message": "This is message from logstash",
    "timestamp": "2024-12-17T12:34:56.789Z"
}
send_log_to_logstash(log_message)
