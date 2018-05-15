

class ScaryPathSegmentException(Exception):
    pass


def sanitize_path_segment(segment):
    # Path names in Linux can contain anything except a nul byte and /
    # Note this causes collisions on cases like
    #
    # git@myhost.com/foo/bar
    # git@myhost.com/foo_bar
    #
    # but honestly.
    #
    # An alternative would be to base64 or sha256sum the input but
    # that seems a bit unfriendly by default.
    #
    # Python strings can't contain a nul byte, so we don't have to
    # guard against it.

    sanitized = segment.replace("/", "_")

    if sanitized == "..":
        raise ScaryPathSegmentException("Repository cannot be named '..'")
    elif sanitized == ".":
        raise ScaryPathSegmentException("Repository cannot be named '.'")
    elif sanitized == "":
        raise ScaryPathSegmentException("Repository name cannot be an empty"
                                        " string")
    else:
        return sanitized
