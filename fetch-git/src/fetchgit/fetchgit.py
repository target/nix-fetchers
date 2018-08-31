#!/usr/bin/env python3

import json
import argparse

import fetchgit.log
from fetchgit.archives import TagArchive, BranchArchive
from fetchgit.arguments import BranchRevisionAction
from fetchgit.repository import RepositoryCache
from fetchgit.nixerrors import NixError


def dont_break_out_of_double_single_quotes(msg):
    return msg.replace("''", '""')  # oh my word


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
          "debug": [dont_break_out_of_double_single_quotes(msg)
                    for msg in log.debug_msgs]
      })
    ))


parser = argparse.ArgumentParser(
    description="an improved evaluation-time Git fetcher for Nix",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""

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

def main():
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
                "debug": [dont_break_out_of_double_single_quotes(msg)
                    for msg in log.debug_msgs]
            })
        ))
