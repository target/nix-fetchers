{ runCommand, testlib, all-fetchers, git }:
runCommand "test-fetch-tag" {
  buildInputs = [ git ];
  src = all-fetchers.fetch-git {
    url = testlib.makeGitRepo {
      commits = 2;
      finalizingCommand = ''
        git tag v0.0.2
      '';
    };
    tag = "v0.0.2";
  };
}
''
  cd $src
  if [ "$(cat contents)" = "2" ]; then
    echo success | tee $out
  else
    echo "2" | diff contents -
  fi

''
