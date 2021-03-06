{ pkgs ? import (builtins.fetchTarball {
    url = https://github.com/nixos/nixpkgs/archive/0d95d03c98f2ecef7c721cb6e0a638bbbff44d0a.tar.gz;
    sha256="162dywda2dvfj1248afxc45kcrg83appjd0nmdb541hl7rnncf02";
  }) {}
}:
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
  ]);
in
pkgs.mkShell {
  name = "dev-shell";
  buildInputs = [ 
    pkgs.pipenv
    python_pkgs
    (pkgs.rWrapper.override {
      packages = r_pkgs;
    })
  ];
    # Set Environment Variables
  shellHook = ''
    SOURCE_DATE_EPOCH=$(date +%s) # required for python wheels

    local venv=$(pipenv --bare --venv &>> /dev/null)

    if [[ -z $venv || ! -d $venv ]]; then
      pipenv install --dev &>> /dev/null
    fi

    export VIRTUAL_ENV=$(pipenv --venv)
    export PIPENV_ACTIVE=1
    export PYTHONPATH="$VIRTUAL_ENV/${python38.sitePackages}:$PYTHONPATH"
    export PATH="$VIRTUAL_ENV/bin:$PATH"
  '';
}

