import subprocess
import log


def cmd(cwd, command):
    log.debug("Running {} in {}".format(
        " ".join(command),
        cwd
        ))

    return subprocess.run(command,
                          cwd=cwd,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          universal_newlines=True,
                          check=True)
