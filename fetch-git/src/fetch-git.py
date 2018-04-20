#!/usr/bin/env python3

import json
import argparse

import log
from archives import TagArchive, BranchArchive
from arguments import BranchRevisionAction
from repository import RepositoryCache
from nixerrors import NixError


def print_success(outPath):
    nixPattern = """
(let
  data = builtins.fromJSON ''{}'';
in data // {{
  outPath = /. + data.outPath;
}})
"""
    print(nixPattern.format(
      json.dumps({
          "outPath": archive.make_archive(),
          "debug": log.debug_msgs
      })
    ))


parser = argparse.ArgumentParser(
    description="an improved evaluation-time Git fetcher for Nix",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
DIFFERENCES FROM builtins.fetchGit

    * Morally pure, assuming good Git hygiene and tags are immutable

      Specifying a git commit and branch is effectively immutable and
      pure

      Specifying a tag name, in a team where you can trust all actors
      to behave responsibly, is also immutable and pure. Note: this
      can probably only be feasibly true in an organization with strict
      repository protection!


    * Uses separate Git repositories per upstream Git repository

      Sacrifices some caching possibilities for much faster initial
      syncs. Upstream's fetch-git uses a single Git repository for all
      cloned repos. This works great if all you're fetching is Nixpkgs,
      but is extremely slow for initial syncs of other, non-nixpkgs
      repositories.

ENVIRONMENT VARIABLES

    fetch-git caches repositories in:

    if XDG_CACHE_HOME is set:

        XDG_CACHE_HOME/nix-fetchers/fetch-git

    Failing that, if HOME is set, it will store it in:

        HOME/.cache/nix-fetchers/fetch-git

    Failing that, it will raise an error.

REPORTING BUGS

    https://github.com/target/nix-fetchers

AUTHORS

    Original work by Shea Levy <shea.levy@target.com>
    Subsequent work by Graham Christensen <graham.christensen@target.com>

"""
)

parser.add_argument('name', help="Name of the archive")
parser.add_argument('repo', help="git-compatible URL to the repository")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--tag", nargs=1, help="Name of the tag to archive")
group.add_argument("--branch", nargs=2, metavar=("branch", "revision"),
                   action=BranchRevisionAction,
                   help="Name and revision to archive")

args = parser.parse_args()

try:
    if args.tag is not None:
        c = RepositoryCache(args.repo)
        archive = TagArchive(
            c,
            args.tag[0],
            args.name
        )
        print_success(archive.make_archive())
    elif args.branch is not None:
        branch = args.branch
        commit = args.revision
        c = RepositoryCache(args.repo)
        archive = BranchArchive(
            c,
            branch,
            commit,
            args.name
        )
        print_success(archive.make_archive())
    else:
        parser.print_help()
        exit(2)
except NixError as e:
    error_fmt = """
      (let
        x = (builtins.fromJSON ''{}'');
      in builtins.trace x x)
    """
    print(error_fmt.format(
      json.dumps({
          "error": e.failure_type,
          "message": e.message,
          "debug": log.debug_msgs
      })
    ))
