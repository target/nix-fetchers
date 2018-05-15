{ runCommand, testlib, lib, all-fetchers, git }:
runCommand "test-filter-source" {
  src = builtins.filterSource
    (path: type: (builtins.baseNameOf path) == "keep")
    (all-fetchers.fetch-git rec {
      url = testlib.makeGitRepo {
        commits = 1;
        finalizingCommand = ''
          touch keep
          git add keep
          git commit -m "keep should be in the results when we filter it"
        '';
      };
      branch = "master";
      revision = testlib.latestCommit url;
  });
}
''
  cd $src
  if [ -f ./contents ]; then
    echo "Found ./contents! failure!"
    exit 1
  fi

  if [ -f ./keep ]; then
    echo success > $out
  else
    echo "the file ./keep does not exist"
  fi
''
