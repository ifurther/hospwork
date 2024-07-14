{
  description = "Python application hospwork flake file";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = input @ {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
    ...
    }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python_pkgs = pkgs.python310.withPackages (ps: with ps; [
          pyflakes
          pytest

          setuptools
          wheel

          venvShellHook
          pipenv-poetry-migrate

          numpy
          pandas
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
            packages = [
              pkgs.autoPatchelfHook
              pkgs.pipenv
              pkgs.zlib
              pkgs.glibc
              pkgs.postgresql
              pkgs.poetry
              python_pkgs
              #(pkgs.rWrapper.override {
              #  packages = r_pkgs;
              #})
            ];
            # Set Environment Variables
            shellHook = ''
              SOURCE_DATE_EPOCH=$(date +%s) # required for python wheels
              export PATH=${python_pkgs.python.interpreter}:$PATH
              venv=$(pipenv --bare --venv &>> /dev/null)

              if [[ -z $venv || ! -d $venv ]]; then
                pipenv install --dev &>> /dev/null
              fi

              autoPatchelf venv

              export VIRTUAL_ENV=$(pipenv --venv)
              export PIPENV_ACTIVE=1
              export PYTHONPATH="$VIRTUAL_ENV/${python_pkgs.sitePackages}:$PYTHONPATH"
              export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib.outPath}/lib:$LD_LIBRARY_PATH"
              export PATH="$VIRTUAL_ENV/bin:$PATH"
              export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${pkgs.lib.makeLibraryPath [ pkgs.zlib ]}"
            '';
      };
    });
}
