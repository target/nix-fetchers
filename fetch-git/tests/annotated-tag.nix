{ runCommand, testlib, all-fetchers, git }:
runCommand "test-fetch-tag" {
  buildInputs = [ git ];
  src = all-fetchers.fetch-git {
    url = testlib.makeGitRepo {
      commits = 3;
      finalizingCommand = ''
        git tag -a v1.4 -m "my version 1.4"
        echo 4 > contents
        git commit -am "commit #4"
      '';
    };
    tag = "v1.4";
  };
}
''
  cd $src
  if [ "$(cat contents)" = "3" ]; then
    echo success | tee $out
  else
    echo "3" | diff contents -
  fi

''
