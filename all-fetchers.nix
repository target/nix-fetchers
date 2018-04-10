builtins.listToAttrs (map (name: {
  inherit name;
  value = ./. + "/${name}";
}) [
  "fetch-pypi-hash"
])
