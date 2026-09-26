#!/bin/sh
# A whole NixOS system is one store path, computed from configuration.nix before anything is built.
# Evaluate a minimal configuration, then the same with one service switched on.
set -e
export NIX_PATH=nixpkgs=$NIXPKGS
W=$(mktemp -d); cd "$W"
cat > base.nix <<'NIX'
{ boot.loader.grub.device = "nodev";
  fileSystems."/".device = "/dev/sda1";
  system.stateVersion = "24.11"; }
NIX
cat > web.nix <<'NIX'
{ imports = [ ./base.nix ];
  services.nginx.enable = true; }
NIX
sys() { nix-instantiate --eval -E "(import <nixpkgs/nixos> { configuration = ./$1; }).config.system.build.toplevel.outPath" | tr -d '"'; }
echo "=== configuration.nix (base):"; cat base.nix
echo "system: $(sys base.nix)"
echo "=== the same, plus: services.nginx.enable = true;"
echo "system: $(sys web.nix)"
echo "=== evaluate base again"
echo "system: $(sys base.nix)"
