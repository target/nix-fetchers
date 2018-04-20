{ runCommand, bash, git, gnutar, python3, python3Packages, makeWrapper }:

runCommand "fetch-git" {
  src = ./src;
  inherit git gnutar python3;
  nativeBuildInputs = [ makeWrapper python3Packages.flake8 ];
}
''
    flake8 $src/*.py

    mkdir -p $out/bin $out/lib

    cp $src/*.py $out/lib
    chmod +x $out/lib/fetch-git.py

    ln -s $out/lib/fetch-git.py $out/bin/fetch-git

    patchShebangs $out/lib/fetch-git.py
    wrapProgram $out/bin/fetch-git \
      --set PATH "${git}/bin:${gnutar}/bin:${bash}/bin"
''
