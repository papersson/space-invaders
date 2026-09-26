#!/bin/sh
# Real Nix runs behind the numbers and paths in the lesson. Nixpkgs is pinned to one revision.
# Usage: NIXPKGS=/path/to/nixpkgs sims/demo.sh > data/nix_demo.txt
set -e
export NIX_PATH=nixpkgs=$NIXPKGS
W=$(mktemp -d); cd "$W"
cat > pkgs.nix <<'NIX'
let
  pkgs = import <nixpkgs> {};
  greet = hello: pkgs.writeShellScriptBin "greet" "exec ${hello}/bin/hello --greeting='hi'";
  hello2 = pkgs.hello.overrideAttrs (old: { doCheck = false; });   # one small change to hello's build
in {
  hello = pkgs.hello;  cowsay = pkgs.cowsay;
  greet = greet pkgs.hello;
  hello2 = hello2;  greet2 = greet hello2;
}
NIX
path() { nix-instantiate --eval --strict -E "(import ./pkgs.nix).$1.outPath" | tr -d '"'; }
echo "=== nixpkgs: $(cat $NIXPKGS/.git-revision 2>/dev/null || basename $NIXPKGS)"
echo "=== output paths, computed before anything is built"
for p in hello greet cowsay; do echo "$p: $(path $p)"; done
echo "=== change one input of hello (doCheck = false), recompute"
for p in hello2 greet2 cowsay; do echo "$p: $(path $p)"; done
echo "=== build hello (fetched from the binary cache) and run it"
H=$(nix-build --no-out-link -A hello ./pkgs.nix 2>/dev/null); echo "$H"; $H/bin/hello
echo "=== its closure: everything it needs at run time"
nix-store -qR "$H"
echo "=== build the changed hello from source; both are now in the store, side by side"
H2=$(nix-build --no-out-link -A hello2 ./pkgs.nix 2>/dev/null); echo "$H2"; $H2/bin/hello
ls -d /nix/store/*-hello-2.* | grep -v '\.drv$' | grep -v -- '-doc$\|-man$\|-info$' | sort
echo "=== a profile: install hello, then cowsay; roll back"
P=$W/profile
nix-env -p $P -f ./pkgs.nix -iA hello 2>&1 | grep -v "^building\|^warning" || true
nix-env -p $P -f ./pkgs.nix -iA cowsay 2>&1 | grep -v "^building\|^warning" || true
nix-env -p $P --list-generations | sed 's/ *$//'
echo "bin: $(ls $P/bin | tr '\n' ' ')"
echo "profile -> $(readlink $P)"
nix-env -p $P --rollback 2>&1
nix-env -p $P --list-generations | sed 's/ *$//'
echo "bin: $(ls $P/bin | tr '\n' ' ')"
echo "profile -> $(readlink $P)"
echo "=== $(nix --version)"
