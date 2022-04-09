{ pkgs ? import (builtins.fetchTarball {
    url = https://github.com/nixos/nixpkgs/archive/a7ecde854aee5c4c7cd6177f54a99d2c1ff28a31.tar.gz;
    sha256="162dywda2dvfj1248afxc45kcrg83appjd0nmdb541hl7rnncf02";
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
  python_pkgs = withpython38Packages; [
    pipenv
    jupyter
    ];
in
pkgs.mkShell {
  name = "dev-shell";
  buildInputs = [ 
    python_pkgs

    (pkgs.rWrapper.override {
      packages = r_pkgs;
    })
  ];
}
