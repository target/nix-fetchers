{ runCommand, testlib, lib, all-fetchers, git }:
runCommand "test-specify-name" {
  src = all-fetchers.fetch-git rec {
      url = testlib.makeGitRepo {
        commits = 1;
      };
      name = "my-cool-source-name";
      branch = "master";
      revision = testlib.latestCommit url;
  };
}
''
  if echo "$src" | grep -q "my-cool-source-name"; then
    echo success > $out
  fi
''
