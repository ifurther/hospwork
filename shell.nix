{ pkgs ? import (builtins.fetchTarball {
    url = https://github.com/nixos/nixpkgs/archive/0af613569c9056b2fa1c95b4a99dcb41219bb6dd.tar.gz;
    sha256 = "07g3mlh0vfbz24v1dqwa0b72wkqky5zjp5yvbmy5cflirz12izzs";
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

with import <nixpkgs> {};
sedenv.mkDerivation {
  name = "hospwork-env";
  buildInputs = [ python38 pipenv ];
}
