
import sys

debug_msgs = []


def debug(msg):
    debug_msgs.append(msg)


def warning(msg):
    print(msg, file=sys.stderr)
    debug(msg)
