
import sys

debug_msgs = []


def debug(msg):
    debug_msgs.append(msg)


def warning(msg):
    print(f"fetch-git: {msg}", file=sys.stderr)
    debug(msg)
