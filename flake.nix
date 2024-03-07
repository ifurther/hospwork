{
  description = "Python application hospwork flake file";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = input @ {
    self,
    nixpkgs,
    flake-utils,
    ...
    }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python_pkgs = pkgs.python38.withPackages (ps: with ps; [
          pyflakes
          pytest
          venvShellHook
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
              python_pkgs
              #(pkgs.rWrapper.override {
              #  packages = r_pkgs;
              #})
            ];
            # Set Environment Variables
            shellHook = ''
              SOURCE_DATE_EPOCH=$(date +%s) # required for python wheels

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
