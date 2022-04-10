{ pkgs ? import (builtins.fetchTarball {
    url = https://github.com/nixos/nixpkgs/archive/0d95d03c98f2ecef7c721cb6e0a638bbbff44d0a.tar.gz;
    sha256="162dywda2dvfj1248afxc45kcrg83appjd0nmdb541hl7rnncf02";
  }) {}
}:


let

  jupyter = import (builtins.fetchGit {
    url = https://github.com/tweag/jupyterWith;
    # Example working revision, check out the latest one.
    rev = "45f9a774e981d3a3fb6a1e1269e33b4624f9740e";
  }) {};

  iPython = jupyter.kernels.iPythonWith {
    name = "python";
    packages = p: with p; [ python38 pytest pyflakes ];
  };

  irkernel = jupyter.kernels.iRWith {                
      name = "nixpkgs";                                                         
      # Libraries to be available to the kernel.                                
      packages = p: with p; [ 
        ggplot2
        dplyr
        knitr
        rmarkdown
        tidyverse
        viridis
        tinytex
      ];                                           
    };

  jupyterEnvironment = jupyter.jupyterlabWith {                                
      kernels = [ iPython irkernel ];             
    }; 
in

jupyterEnvironment.env
pkgs.mkShell {
  name = "dev-shell";
  buildInputs = [ 
    pkgs.pipenv
    #python_pkgs

    #(pkgs.rWrapper.override {
    #  packages = r_pkgs;
    #})
  ];
}
