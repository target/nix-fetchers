{ runCommand, testlib, all-fetchers, git }:
runCommand "test-fetch-midle-commit" {
  buildInputs = [ git ];
  src = all-fetchers.fetch-git rec {
    url = testlib.makeGitRepo {
      commits = 8;
    };
    branch = "master";
    revision = builtins.elemAt (testlib.listAllCommits url) 4;
  };
}
''
  cd $src
  if [ "$(cat contents)" = "4" ]; then
    echo success | tee $out
  else
    echo "4" | diff contents -
  fi

''
