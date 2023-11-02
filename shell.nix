{ pkgs ? import <nixpkgs> {} }:
let
  r_pkgs = with pkgs.rPackages; [
    # rmarkdown-related packages.
    ggplot2
    dplyr
    #knitr
    #rmarkdown
    #tidyverse
    #viridis
    #tinytex
    # Rstudio-related packages.
    # servr
    # Uncomment to add RStudio in your environment.
    # (pkgs.rstudioWrapper.override {
    #  packages = r_pkgs;
    # })
  ];
  python_pkgs = pkgs.python38.withPackages (ps: with ps; [
    pyflakes
    pytest
    venvShellHook
  ]);
in
pkgs.mkShell {
  name = "dev-shell";
  buildInputs = [ 
    pkgs.pipenv
    pkgs.zlib
    pkgs.postgresql
    pkgs.autoPatchelfHook
    python_pkgs
    #(pkgs.rWrapper.override {
    #  packages = r_pkgs;
    #})
  ];
    # Set Environment Variables
  shellHook = ''
    SOURCE_DATE_EPOCH=$(date +%s) # required for python wheels

    local venv=$(pipenv --bare --venv &>> /dev/null)

    if [[ -z $venv || ! -d $venv ]]; then
      pipenv install --dev &>> /dev/null
    fi

    autopatchelf venv

    export VIRTUAL_ENV=$(pipenv --venv)
    export PIPENV_ACTIVE=1
    export PYTHONPATH="$VIRTUAL_ENV/${python_pkgs.sitePackages}:$PYTHONPATH"
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib.outPath}/lib:$LD_LIBRARY_PATH"
    export PATH="$VIRTUAL_ENV/bin:$PATH"
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${pkgs.lib.makeLibraryPath [ pkgs.zlib ]}"
  '';
}

