{ substituteAll, curl, jq, bash, coreutils, shellcheck }:

substituteAll {
  src = ./fetch-pypi-hash;
  isExecutable = true;
  dir = "bin";
  inherit curl jq bash coreutils;
  nativeBuildInputs = [ shellcheck ];
  postInstall = ''
    shellcheck $out/bin/fetch-pypi-hash
  '';
}
