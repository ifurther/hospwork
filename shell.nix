{ pkgs ? import (builtins.fetchTarball {
    url = https://github.com/nixos/nixpkgs/archive/a7ecde854aee5c4c7cd6177f54a99d2c1ff28a31.tar.gz;
    sha256 = "93941a4edb270f434b87b712bb13620a87d6d91f80f70e908a8bf27fd3ec5d58";
  }) {}
}:


let
  r_pkgs = with pkgs.rPackages; [
    # rmarkdown-related packages.
    knitr
    rmarkdown
    tidyverse
    viridis
    tinytex
    # Rstudio-related packages.
    # servr

    # Uncomment to add RStudio in your environment.
    # (pkgs.rstudioWrapper.override {
    #  packages = r_pkgs;
    # })

  ];
in
pkgs.mkShell {
  name = "dev-shell";
  buildInputs = [ 
    pkgs.python38Full
    pkgs.pipenv
    pkgs.jupyter

    (pkgs.rWrapper.override {
      packages = r_pkgs;
    })
  ];
}
