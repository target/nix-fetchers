{ seed ? "stable-seed" }:
# Run with: ./run
let
  comparison-tests = {
    fetch-pypi-hash = {
      value = all-fetchers.fetch-pypi-hash {
        name = "Pillow";
        version = "5.0.0";
      };
      expected = {
        sha256 = "12f29d6c23424f704c66b5b68c02fe0b571504459605cfe36ab8158359b0e1bb";
      };
    };
    fetch-pypi-hash-bad-filename = {
      value = all-fetchers.fetch-pypi-hash {
        name = "Pillow";
        version = "5.0.0";
        filename = "this-better-not-exist.tar.gz";
      };
      expected = {
        failure-type = "missing-filename";
      };
    };
    fetch-pypi-zip = {
      value = all-fetchers.fetch-pypi-hash rec {
        name = "recordclass";
        version = "0.5";
        filename = "${name}-${version}.zip";
      };
      expected = {
        sha256 = "4582ed9621846cd67c7647edaa2940ddaca75fda3ad5fd77616a347025e6fa78";
      };
    };
  } // (import ../fetch-git/tests { inherit pkgs all-fetchers seed; });

  ###
  nixpkgs = fetchGit { url = "git://github.com/NixOS/nixpkgs.git";
                       ref = "release-18.03";
                       rev = "03667476e330f91aefe717a3e36e56015d23f848";
                     };
  pkgs = import nixpkgs {};
  make-extra-builtins =
    pkgs.callPackage ../make-extra-builtins.nix {};
  # Simulate build/run staging
  extra-builtins = make-extra-builtins {
    fetchers = import ../all-fetchers.nix;
  };
  exec' = builtins.exec or
    (throw "Tests require the allow-unsafe-native-code-during-evaluation Nix setting to be true");
  all-fetchers = import "${extra-builtins}/extra-builtins.nix" {
    exec = exec';
  };

  run-test = acc: name: let
    inherit (comparison-tests.${name}) value expected;
  in if value != expected
    then builtins.trace "Test ${name} failed" (
         builtins.trace "Expected:" (
         builtins.trace expected (
         builtins.trace "Got: " (
         builtins.trace value "failure"))))
  else acc;
in builtins.foldl' run-test "success" (builtins.attrNames comparison-tests)
