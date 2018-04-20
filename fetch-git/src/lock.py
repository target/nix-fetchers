import os
import log
import time
import fcntl
import errno


class FileLock:
    fd = None

    def __init__(self, root):
        self.root = root
        self.lockfile = os.path.join(self.root, "lock")

    def __enter__(self):
        log.debug("About to lock {}".format(self.lockfile))

        if not self._acquire(block=False):
            log.warning("Retrying lock acquisition on {}.".format(
                self.lockfile
            ))
            self._acquire(block=True)

        log.debug("Received lock on {}".format(self.lockfile))

    def __exit__(self, *args):
        log.debug("Releasing lock {}".format(self.lockfile))
        self._release()

    def _acquire(self, block):
        try:
            self.fd = os.open(self.lockfile, os.O_CREAT)
            if block:
                fcntl.flock(self.fd, fcntl.LOCK_EX)
            else:
                fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except (IOError, OSError) as e:
            if e.errno != errno.EAGAIN:
                raise
            return False

    def _release(self):
        if self.fd is not None:
            try:
                os.unlink(self.lockfile)
            except:  # noqa: E722
                # Swallow any/all exceptions because it is immaterial
                # if we delete the file or not.
                pass

            fcntl.flock(self.fd, fcntl.LOCK_UN)
            os.close(self.fd)
            self.fd = None
