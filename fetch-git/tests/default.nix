{ pkgs, all-fetchers, seed ? "stable-seed" }:
let
  testlib = pkgs.callPackage ./lib.nix { inherit seed; };

  callTest = file: let
    # built =
  in {
    value = let
      attempt = builtins.tryEval (builtins.readFile (pkgs.callPackage file { inherit testlib all-fetchers; }));
    in if attempt.success
      then attempt.value
      else "failure";
    expected = "success\n";
  };
in {
  test_fetch_tag = callTest ./fetch-tag.nix;
  test_annotated_tag = callTest ./annotated-tag.nix;
  test_fetch_branch = callTest ./fetch-branch.nix;
  test_fetch_middle_commit = callTest ./fetch-middle-commit.nix;
  test_filter_source = callTest ./filter-source.nix;
  test_fetch_specify_name = callTest ./fetch-specify-name.nix;
}
