import os
from fetchgit.paths import sanitize_path_segment
from fetchgit.lock import FileLock
from fetchgit.nixerrors import NixError


def cache_root(repository):
    xdg_cache_home = os.environ.get('XDG_CACHE_HOME')
    home = os.environ.get('HOME')

    cache_base = None
    if xdg_cache_home is not None:
        cache_base = xdg_cache_home
    elif home is not None:
        cache_base = os.path.join(home, '.cache')
    else:
        raise NixError("no-cache-directory",
                       "Specify XDG_CACHE_HOME or HOME env variables")

    return os.path.join(cache_base,
                        'nix-fetchers/fetch-git',
                        sanitize_path_segment(repository))


class RepositoryCache:
    repository = None

    def __init__(self, repository):
        self.repository = repository

    def root_directory(self):
        root = cache_root(self.repository)
        os.makedirs(root, exist_ok=True)
        return root

    def lock(self):
        return FileLock(self.root_directory())
