{ runCommand, testlib, all-fetchers, git }:
runCommand "test-fetch-branch" {
  buildInputs = [ git ];
  src = all-fetchers.fetch-git rec {
    url = testlib.makeGitRepo {
      commits = 5;
    };
    branch = "master";
    revision = testlib.latestCommit url;
  };
}
''
  cd $src
  if [ "$(cat contents)" = "5" ]; then
    echo success | tee $out
  else
    echo "5" | diff contents -
  fi

''
