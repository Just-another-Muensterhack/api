{ pkgs ? import <nixpkgs> {} }:
let
  my-python = pkgs.python3;
  python-with-my-packages = my-python.withPackages (p: with p; [
    requests
    fastapi
    sqlalchemy
    python-jose
    uvicorn
    passlib
    psycopg2
  ]);
in
pkgs.mkShell {
  buildInputs = [
    python-with-my-packages
    pkgs.black
  ];
  shellHook = ''
    PYTHONPATH=${python-with-my-packages}/${python-with-my-packages.sitePackages}
  '';
}

