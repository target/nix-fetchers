{ runCommand, git, jq, lib, seed }:
rec {
  makeGitRepo = { commits ? 2,
    buildInputs ? [],
    finalizingCommand ? ""
  }: (runCommand "test-git-repo" {
    buildInputs = [ git ] ++ buildInputs;
    GIT_COMMITTER_NAME = "Bogus Committer";
    GIT_COMMITTER_EMAIL = "bogus-committer@example.com";
    GIT_AUTHOR_NAME = "Bogus Author";
    GIT_AUTHOR_EMAIL = "bogus-author@example.com";
    TEST_SEED = seed;
  } ''
    set -eu

    mkdir repo
    cd repo
    git init

    touch contents
    git add contents
    ${lib.concatMapStringsSep "\n" (x: ''
      echo "${toString x}" > contents
      git add contents
      git commit -m "Appending ${toString x} to contents"
    '') (lib.range 1 commits)}

    ${finalizingCommand}

    git init --bare $out
    git push --mirror $out
  '');

  loadJSONFile = f: builtins.fromJSON (builtins.readFile f);

  # Fetch a list of all commits in the repository from the default
  # current HEAD, the first (lib.head) in the list will be the most
  # recent. The last (lib.last) will be the oldest.
  listAllCommits = repo: loadJSONFile (runCommand "list-all-commits" {
    buildInputs = [ git jq ];
  } ''
    cd ${repo}
    git log --pretty=tformat:%H \
      | jq --raw-input --slurp 'split("\n") | .[0:-1]' > $out
  '');

  latestCommit = repo: lib.head (listAllCommits repo);
}
