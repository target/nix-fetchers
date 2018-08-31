{ bash, git, gnutar, python3, python3Packages, makeWrapper }:

python3Packages.buildPythonPackage {
  pname = "target-nix-fetchers-fetch-git";
  version = "1.0.0";

  src = ./src;

  postFixup = ''
    wrapProgram $out/bin/fetch-git \
      --set PATH "${git}/bin:${gnutar}/bin:${bash}/bin"
  '';
}
