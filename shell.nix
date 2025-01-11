let
  pkgs = import <nixpkgs> {};

in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      fastapi
      uvicorn
      httpx
      httpie
      python-dotenv
      aiohttp
      black
    ]))
  ];
}
