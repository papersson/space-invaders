#!/bin/sh
# Terraform against local files standing in for servers (hashicorp/local provider), to show:
# a declared count, idempotent re-apply, 3 -> 5 as an absolute target, drift that nothing
# notices until the next plan, and an imperative script that repeats its work when re-run.
set -e
TF=${TF:-terraform}
D=$(mktemp -d); cd "$D"
cat > main.tf <<'TF'
variable "servers" { default = 3 }
resource "local_file" "server" {
  count    = var.servers
  filename = "${path.module}/servers/web-${count.index}"
  content  = "running\n"
}
TF
$TF init -input=false -no-color >/dev/null
echo "=== apply with servers = 3"
$TF apply -auto-approve -input=false -no-color | grep -E "Plan:|Apply complete|No changes"
echo "servers on disk: $(ls servers | tr '\n' ' ')"
echo "=== apply again, nothing changed"
$TF apply -auto-approve -input=false -no-color | grep -E "Plan:|Apply complete|No changes"
echo "=== change to servers = 5 and apply"
$TF apply -auto-approve -input=false -no-color -var servers=5 | grep -E "Plan:|Apply complete|No changes"
echo "servers on disk: $(ls servers | tr '\n' ' ')"
echo "=== someone deletes web-1 by hand; Terraform is not running, so nothing happens"
rm servers/web-1
echo "servers on disk: $(ls servers | tr '\n' ' ')"
echo "=== next terraform plan"
$TF plan -input=false -no-color -var servers=5 | grep -E "will be created|Plan:|No changes" | sed 's/^ *//'
$TF apply -auto-approve -input=false -no-color -var servers=5 | grep -E "Plan:|Apply complete"
echo "servers on disk: $(ls servers | tr '\n' ' ')"
echo "=== an imperative script: 'start 2 more servers', run twice"
mkdir -p imperative; for run in 1 2; do for i in 1 2; do n=$(ls imperative | wc -l); touch imperative/web-$n; done; echo "after run $run: $(ls imperative | wc -l) servers"; done
echo "=== $($TF version | head -1)"
