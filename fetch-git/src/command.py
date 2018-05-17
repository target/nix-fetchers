import subprocess
import log


def cmd(cwd, command):
    log.debug("Running {} in {}".format(
        " ".join(command),
        cwd
        ))

    result = subprocess.run(command,
                            cwd=cwd,
                            stdout=subprocess.PIPE,
                            universal_newlines=True,
                            check=True)
    log.debug("command output: {}".format(result.stdout))
    return result
