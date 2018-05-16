import os
import subprocess
import log
from paths import sanitize_path_segment
from command import cmd
from nixerrors import NixError


def setup_bare(path):
    if not os.path.isdir(path):
        log.debug("About to init a bare repository at {}".format(path))
        cmd(None, ["git", "init", "--bare", path])


def archive_ref(source, ref, destination):
    try:
        os.makedirs(destination)
    except FileExistsError:
        pass

    cmd(source,
        [
            "bash",
            # Bash will run the following safe bash, and accept the defs
            # of $1 and $2 via the following -s
            "-c", "git archive --format=tar \"$1\" | tar -x -C \"$2\"",

            # Passing ref and destination this way is much safer than
            # using interpolation
            "-s", ref, destination
        ])


class BranchArchive:
    cache = None
    branch = None
    revision = None
    name = None

    def __init__(self, cache, branch, revision, name):
        self.cache = cache
        self.branch = branch
        self.revision = revision
        self.name = name

    def make_archive(self):
        if not self.__exists():
            log.warning("Fetching branch '{}' at rev '{}' from {}".format(
                self.branch,
                self.revision,
                self.cache.repository
            ))
            with self.cache.lock():
                bare_path = self.__bare_path()

                if not os.path.isdir(bare_path):
                    setup_bare(bare_path)

                self.__fetch_depth(1)

                if not self.__commit_exists() and not self.__is_massive():
                    # So 1000 is just a "good start", subsequent fetches are
                    # pretty expensive. Thus, my hope is that we can get a
                    # nice fetch chunk here and maximize the odds we receive
                    # the revision we need, without doing a fancy backoff
                    # which is very slow and re-downloads quite a lot of data.
                    self.__deepen(1000)

                if not self.__commit_exists():
                    self.__fetch_all()

                if not self.__commit_exists():
                    raise NixError(
                        "commit-not-found",
                        "Commit {} not found after fetching {}.".format(
                            self.revision,
                            self.__ref()
                        )
                    )

                archive_ref(bare_path, self.revision, self.__archive_path())

        return self.__archive_path()

    def __is_massive(self):
        return "nixpkgs" in self.cache.repository.lower()

    def __ref(self):
        return "refs/heads/{}".format(self.branch)

    def __commit_exists(self):
        try:
            cmd(self.__bare_path(), ["git", "cat-file", "-e",
                                     "{}^{{commit}}".format(self.revision)])
            return True
        except subprocess.CalledProcessError:
            return False

    def __fetch_depth(self, depth):
        cmd(self.__bare_path(), ["git",
                                 "fetch",
                                 "--depth",
                                 str(depth),
                                 self.cache.repository,
                                 self.__ref()])

    def __deepen(self, depth):
        cmd(self.__bare_path(), ["git",
                                 "fetch",
                                 "--deepen",
                                 str(depth),
                                 self.cache.repository,
                                 self.__ref()])

    def __fetch_all(self):
        try:
            cmd(self.__bare_path(), ["git",
                                     "fetch",
                                     "--unshallow",
                                     self.cache.repository,
                                     self.__ref()])
        except subprocess.CalledProcessError:
            # We may already have unshallowed this repository
            pass

    def __bare_path(self):
        return os.path.join(
            self.cache.root_directory(),
            'bare'
        )

    def __archive_path(self):
        return os.path.join(
            self.cache.root_directory(),
            'branch-archives',
            sanitize_path_segment(self.branch),
            sanitize_path_segment(self.revision),
            sanitize_path_segment(self.name)
        )

    def __exists(self):
        return os.path.isdir(self.__archive_path())


class TagArchive:
    cache = None
    tag = None
    name = None

    def __init__(self, cache, tag, name):
        self.cache = cache
        self.tag = tag
        self.name = name

    def make_archive(self):
        if not self.__exists():
            log.warning("Fetching tag '{}' from {}".format(
                self.tag,
                self.cache.repository
                ))
            with self.cache.lock():
                bare_path = self.__bare_path()
                ref = "refs/tags/{}".format(self.tag)
                setup_bare(bare_path)

                try:
                    cmd(bare_path, ["git",
                                    "fetch",
                                    "--depth=1",
                                    self.cache.repository,
                                    ref])
                except subprocess.CalledProcessError:
                    raise NixError(
                        "tag-not-found",
                        "Tag {} not found".format(self.tag)
                    )

                archive_ref(bare_path, "FETCH_HEAD", self.__archive_path())

        return self.__archive_path()

    def __bare_path(self):
        return os.path.join(
            self.cache.root_directory(),
            'bare'
        )

    def __archive_path(self):
        return os.path.join(
            self.cache.root_directory(),
            'tag-archives',
            sanitize_path_segment(self.tag),
            sanitize_path_segment(self.name)
        )

    def __exists(self):
        return os.path.isdir(self.__archive_path())
