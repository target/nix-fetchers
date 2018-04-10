{ callPackage, writeTextDir, buildEnv }:
{ fetchers }: let
  add-fetcher = { programs ? [], fetcher-snippets ? [] }: name: let
    dir = fetchers.${name};
  in {
    programs = programs ++ [ (callPackage (dir + "/build.nix") {}) ];
    fetcher-snippets = fetcher-snippets ++ [
      "${name} = import ${dir + "/run.nix"} exec fetcher-programs;"
    ];
  };
  inherit (builtins.foldl' add-fetcher {} (builtins.attrNames fetchers))
    programs fetcher-snippets;
  fetcher-programs = buildEnv {
    name = "fetcher-programs";
    paths = programs;
  };
in writeTextDir "extra-builtins.nix" ''
{ exec, ... }: let
  fetcher-programs = builtins.storePath ${fetcher-programs};
in {
  ${builtins.concatStringsSep "\n  " fetcher-snippets}
}
''
