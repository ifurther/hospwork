{ pkgs ? import (builtins.fetchTarball {
    url = https://github.com/nixos/nixpkgs/archive/f67c61e0d507ed352e33be64d0d02b9d6be0488b.tar.gz;
    sha256="162dywda2dvfj1248afxc45kcrg83appjd0nmdb541hl7rnncf02";
  }) {}
}:


let
  r_pkgs = with pkgs.rPackages; [
    # rmarkdown-related packages.
    ggplot2
    dplyr
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
}
