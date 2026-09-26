# Declarative infrastructure and reconciliation loops: the canonical treatment

In this document, "canonical" means the following sources. For Kubernetes: the official docs and design docs, the Borg/Omega/Kubernetes paper (Burns et al., *ACM Queue* 2016), *Kubernetes: Up & Running* (KUAR) and *Programming Kubernetes*, and the Kubebuilder and controller-runtime docs. For infrastructure as code: the Terraform docs, *Terraform: Up & Running* (TUR), Kief Morris's *Infrastructure as Code* and Fowler's bliki. For the history: the CFEngine and LISA papers by Burgess and by Traugott & Brown. For GitOps: OpenGitOps. For formal work: the OSDI papers Sieve (2022) and Anvil (2024). I checked every quotation below against the primary text unless it is marked **[uncertain]**.

---

## 1. The canonical worked example

**The dominant example is keeping N identical replicas running (a replica count).** Nearly every canonical source uses it:

- **Kubernetes docs**, [Objects in Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/). A Deployment's `spec` asks for three replicas. "If any of those instances should fail (a status change), the Kubernetes system responds to the difference between spec and status by making a correction--in this case, starting a replacement instance."
- **KUAR** (Burns, Beda, Hightower; Ch. 1 in every edition). It contrasts the imperative "run A, run B, run C" with the declarative "replicas equals three". On self-healing: "If you manually create a fourth replica Kubernetes will destroy one to bring the number back to three. If you manually destroy a replica, Kubernetes will create one" ([excerpt notes](https://garba.org/references/hightower2017/hightower2017.html)). The "ReplicaSets" chapter (Ch. 9 in the 3rd ed., 2022) has a section titled "Reconciliation Loops".
- **Burns, Grant, Oppenheimer, Brewer, Wilkes, "Borg, Omega, and Kubernetes", *ACM Queue* 14(1), 2016** ([PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/pdf/44843.pdf)). A reconciliation loop "compares a desired state (e.g., how many pods should match a label-selector query) against the observed state (the number of such pods that it can find), and takes actions to converge the observed and desired states."
- **controller-runtime** `Reconciler` godoc ([source](https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/reconcile/reconcile.go)). "Observe that the object spec specifies 5 replicas but actual cluster contains only 1 Pod replica. Create 4 Pods."
- **CoreOS, "Introducing Operators"** (B. Philips, 3 Nov 2016). "A single pod is running, and the user updates the desired Pod count to 3." The etcd Operator example is the same idea: "a user can simply increase the etcd cluster size field by 1."
- **In infrastructure as code the same example appears as "10 servers → 15 servers"** (Brikman, [Gruntwork blog 2016](https://www.gruntwork.io/blog/why-we-use-terraform-and-not-chef-puppet-ansible-saltstack-or-cloudformation); TUR Ch. 1 "Why Terraform"). With a procedural Ansible `count: 10`, "if you just updated the number of servers to 15 and reran that code, it would deploy 15 new servers, giving you 25 total!" With Terraform you change `count` from 10 to 15 and it creates only five.

**Why this example is standard:**

- The state is one scalar that is easy to observe: you just count pods.
- All three possible actions appear: create, delete and do nothing.
- Perturbing it takes a single command (`kubectl delete pod`).
- It makes the difference between an **absolute target** (15) and a **delta instruction** (+5) obvious.
- It shows idempotence: re-applying does nothing.
- It shows level-triggering: the Kubernetes API conventions use "2 → 5 → 3", and Bowes's article uses "1 → 5 → 2".
- It needs no domain knowledge.

**The competing standard example is the thermostat.** The Kubernetes [Controllers](https://kubernetes.io/docs/concepts/architecture/controller/) page opens with it: "When you set the temperature, that's telling the thermostat about your *desired state*. The actual room temperature is the *current state*. The thermostat acts to bring the current state closer to the desired state, by turning equipment on or off." It is also the textbook entry point to feedback control: Åström & Murray, *Feedback Systems* (Princeton, 2008), Ch. 1 (Fig. 1.4a, the Honeywell T87; "on-off control", eq. 1.1).

**Which is more common:** the thermostat usually introduces the idea of a loop, and the replica count is the example that gets worked through. The replica count is much more common in Kubernetes and infrastructure-as-code material. The Kubernetes docs use both, with the thermostat first.

**The Terraform-specific worked example** is a single `aws_instance`: TUR Ch. 2 uses `aws_instance "example"` and HashiCorp's tutorial uses `aws_instance.app_server`. The tutorial then changes an attribute so the plan shows `-/+ destroy and then create replacement`, and in the ["Manage resource drift"](https://developer.hashicorp.com/terraform/tutorials/state/resource-drift) tutorial something is changed out-of-band.

---

## 2. The standard progression

This is the order the ideas usually come in across sources:

1. **The problem.** Manual or imperative changes produce *snowflake servers* ("good for a ski resort, bad for a data center", [Fowler 2012](https://martinfowler.com/bliki/SnowflakeServer.html)) and *configuration drift*. See Morris, *Infrastructure as Code* 2nd ed. (2020), Ch. 2 "Principles of Cloud Age Infrastructure", and Traugott & Brown's "divergence" (LISA 2002).
2. **Declarative vs. imperative.** Say *what* you want, not *how* to get it. The Kubernetes [Object Management](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/) page steps from imperative commands, to imperative object configuration, to declarative object configuration (`kubectl apply`). Morris 2nd ed. Ch. 4 covers "Declarative Versus Imperative Languages for Infrastructure" (chapter placement per the published table of contents). Brikman's 10 → 15 example belongs here too.
3. **Idempotence and convergence.** Running the configuration again is safe (Burgess 1998; the Ansible glossary). Terraform prints "No changes. Your infrastructure matches the configuration."
4. **One-shot diff and apply.** Terraform's "Write → Plan → Apply" ([intro](https://developer.hashicorp.com/terraform/intro)).
5. **The control loop.** First the thermostat, then observe → diff → act → repeat. The simplest version in code comes from the Kubernetes ["Writing Controllers"](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-api-machinery/controllers.md) guide:
   ```go
   for {
     desired := getDesiredState()
     current := getCurrentState()
     makeChanges(desired, current)
   }
   ```
   The guide follows it with "Watches, etc, are all merely optimizations of this logic."
6. **Level-triggered vs. edge-triggered logic**, which explains why the loop compares states rather than replaying events. Sources: the API conventions' 2 → 5 → 3 example; Tim Hockin, ["Edge vs. Level triggered logic"](https://speakerdeck.com/thockin/edge-vs-level-triggered-logic) (slides, 2017, built on a hardware-interrupt analogy); J. Bowes, ["Level Triggering and Reconciliation in Kubernetes"](https://hackernoon.com/level-triggering-and-reconciliation-in-kubernetes-1f17fe30333d) (2018).
7. **Continuous vs. on-demand reconciliation, and drift correction.** Kubernetes, Crossplane and GitOps reconcile continuously; Terraform reconciles only when run.
8. **Composition.** Many small controllers coordinate through the API server, which is choreography rather than orchestration: Deployment → ReplicaSet → Pods → scheduler → kubelet. Sources: Beda, ["Core Kubernetes: Jazz Improv over Orchestration"](https://blog.heptio.com/core-kubernetes-jazz-improv-over-orchestration-a7903ea92ca) (Heptio, 30 May 2017); Lukša, *Kubernetes in Action* (2018), §11.2 "How controllers cooperate" / §11.2.2 "The chain of events"; Burns et al. 2016.
9. **Extension.** A custom resource plus a controller is an Operator: CoreOS 2016; the [Kubebuilder book](https://book.kubebuilder.io/cronjob-tutorial/cronjob-tutorial) CronJob tutorial; the [Operator SDK](https://sdk.operatorframework.io/docs/building-operators/golang/tutorial/) Memcached tutorial with `spec.size`. GitOps follows ([OpenGitOps](https://github.com/open-gitops/documents/blob/main/PRINCIPLES.md)).
10. **Production realities.** Status, conditions and `observedGeneration`; informers, workqueues and rate-limited requeue; optimistic concurrency; owner references and finalizers; multiple writers (Server-Side Apply).

**Where a simpler version is shown before the full one:**

| Simple version first | Full version later | Source |
|---|---|---|
| The infinite `for {}` polling loop | Shared informers + workqueue + rate-limited requeue + resync | Writing Controllers guide; client-go `sample-controller`; *Programming Kubernetes* (Hausenblas & Schimanski, 2019) Ch. 1 "Controllers and Operators", then Ch. 3 on client-go |
| Pod | ReplicaSet → Deployment | KUAR 3rd ed. Ch. 5 → 9 → 10; Kubernetes Basics tutorial ("Scale", "Update") |
| `terraform apply` | `plan` + saved plans + remote state + locking | HashiCorp "Get Started" tutorials (Build → Change → Destroy → … → remote state); TUR Ch. 2 (single server → web server → cluster → load balancer) → Ch. 3 (state) |
| Client-side `kubectl apply` 3-way merge using the `last-applied-configuration` annotation | Server-Side Apply with field managers | [kubectl declarative config](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/); [SSA](https://kubernetes.io/docs/reference/using-api/server-side-apply/) |
| Idempotence | Convergence → congruence / immutable servers | Burgess; Traugott & Brown 2002; Fowler/Morris bliki |
| Thermostat on-off control | Hysteresis / stabilization (the HPA) | Åström & Murray Ch. 1; [HPA docs](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/) |

The subsection order in *Programming Kubernetes* Ch. 1 ("The Control Loop" → "Events" → "Edge- Versus Level-Driven Triggers" → "Changing Cluster Objects or the External World" → "Optimistic Concurrency" → "Operators") is partly from memory. The two headings "Edge- Versus Level-Driven Triggers" and "Optimistic Concurrency" are confirmed. **[uncertain: exact order and names of the others]**.

*Kubernetes Patterns* 2nd ed. (Ibryam & Huß, 2023) places Ch. 3 "Declarative Deployment" early and leaves Ch. 27 "Controller" and Ch. 28 "Operator" for the advanced part.

---

## 3. Models and terminology

**The four models**

| Model | Definition | What it guarantees |
|---|---|---|
| **Imperative / procedural** (scripts, Chef/Ansible used procedurally) | A sequence of actions | Only that the actions ran. The end state depends on the starting state and on history: "Procedural code does not fully capture the state of the infrastructure" (Brikman). |
| **Declarative, one-shot reconciliation** (Terraform, Pulumi, CloudFormation; `kubectl apply` as a client action) | The engine diffs desired against (refreshed) current state and executes create/read/update/delete (CRUD) in dependency order | After a *successful* run, the managed resources match the configuration. Nothing is guaranteed between runs, and nothing about resources the tool does not manage. |
| **Declarative, continuous closed-loop reconciliation** (Kubernetes controllers, Crossplane, Argo CD/Flux, and CFEngine/Puppet/DSC agents on a timer) | Observe → compare → act, repeated forever | *Eventual* convergence under assumptions (§4). Drift is **corrected**, not just detected. |
| **Congruent / immutable** | Never mutate in place. Rebuild from a complete description. | Traugott & Brown's "congruence": "maintaining production hosts in complete compliance with a fully descriptive baseline." See also Fowler's PhoenixServer and Morris's ImmutableServer. |

**Standard definitions**

- **Spec / status.** Kubernetes [API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md): "The specification is a complete description of the desired state…" and "fields in `status` should be the most recent observations of actual state." An object is a "record of intent" ([docs](https://kubernetes.io/docs/concepts/overview/working-with-objects/)).
- **Controller.** "Control loops that watch the state of your cluster, then make or request changes where needed" ([docs](https://kubernetes.io/docs/concepts/architecture/controller/)).
- **Reconciliation.** "The process of ensuring the actual state of a system matches its desired state" ([OpenGitOps glossary](https://github.com/open-gitops/documents/blob/main/GLOSSARY.md)). Kubebuilder: "We call this process *reconciling*."
- **Level-based.** "The system must operate correctly given the desired state and the current/observed state, regardless of how many intermediate state updates may have been missed. Edge-triggered behavior must be just an optimization." ([Kubernetes design principles](https://github.com/kubernetes/design-proposals-archive/blob/main/architecture/principles.md))
- **Idempotent vs. convergent** (Burgess, ["A tiny overview of cfengine: convergent maintenance agent"](http://markburgess.org/papers/tiny_intro.pdf), c. 2005 **[year uncertain]**). Idempotence only requires Ô² = Ô. Convergence is relative to a policy state q₀: Ô q = q₀ and Ô q₀ = q₀. In Burgess's words: "no matter how many times cfengine is run, its state will only get closer to the ideal configuration. This is a stronger condition than idempotence". He introduced convergence in "Computer Immunology" (LISA 1998).
- **Operator.** "An application-specific controller that extends the Kubernetes API to create, configure, and manage instances of complex stateful applications" (CoreOS 2016).
- **Drift.** "When a system's actual state has moved or is in the process of moving away from the desired state" (OpenGitOps). Terraform's wording is "Objects have changed outside of Terraform".

**Terminology across fields**

| Concept | Control theory (Åström & Murray) | Autonomic computing | Kubernetes | Terraform | Configuration management | GitOps |
|---|---|---|---|---|---|---|
| Target | reference / setpoint *r* | policy / goal | `spec`, desired state, "record of intent" | configuration (`.tf`) | policy / promise (CFEngine), catalog (Puppet), `state: present` (Ansible) | desired state in the "state store" (Git) |
| Actual | output / process variable *y* | monitored state | `status`, observed / current / actual / live state | "remote objects" / real infrastructure. The *state file* is a recorded mapping plus cache, not the world. | host state | live / actual state |
| Difference | error *e = r − y* | analysis | diff; `observedGeneration` ≠ `generation`; conditions | the plan / diff; "drift" | non-compliance ("sick" vs. "healthy" in Burgess) | drift, `OutOfSync` (Argo CD) |
| Act | actuator / control input *u* | execute | reconcile / sync / "make it so" (Apply) | `apply` through provider CRUD | converge / repair / enforce | sync / reconcile |
| Loop | continuous or sampled | monitor-analyze-plan-execute over shared knowledge (MAPE-K; Kephart & Chess, *IEEE Computer* 2003; IBM blueprint) **[MAPE-K naming attribution uncertain]** | watch-triggered + requeue + periodic resync | runs only when a human or CI invokes it | agent run interval | poll interval |

**Terminology that conflicts between sources**

- **"State."** In Terraform, "state" is Terraform's *record* of what it manages ([state purpose](https://developer.hashicorp.com/terraform/language/state/purpose)). It is neither the desired state nor, strictly, the actual state. In Kubernetes, "state" covers both spec and status.
- **"Source of truth"** means four different things:
  - HashiCorp says the state file "acts as a source of truth for your environment" ([intro](https://developer.hashicorp.com/terraform/intro)).
  - GitOps treats Git as the source of truth.
  - Crossplane calls `forProvider` the "source of truth" for external resources.
  - Kubernetes's resource-model doc says "The reported observed state is truth" ([KRM doc](https://github.com/kubernetes/design-proposals-archive/blob/main/architecture/resource-management.md)).
- **"Reconciliation"** in React means a one-shot diff of the virtual DOM ([React legacy docs](https://legacy.reactjs.org/docs/reconciliation.html)), not a continuous loop.
- **"Orchestration."** Kubernetes says it "eliminates the need for orchestration… first do A, then B, then C" ([Overview](https://kubernetes.io/docs/concepts/overview/)). Burns et al. contrast "choreography" with "centralized orchestration", and Beda calls Kubernetes "jazz improv". Yet Kubernetes is universally marketed as a "container orchestrator", and Ansible uses "orchestration" approvingly.
- **"Declarative."** In Kubernetes it means spec fields are nouns, not verbs: they "represent the desired state, not actions intended to yield the desired state" (API conventions). Pulumi is a "desired state model" written in imperative languages ([docs](https://www.pulumi.com/docs/iac/concepts/how-pulumi-works/)). So "declarative" describes the *interface to the engine*, not the syntax of the language.
- **"Level/edge triggered"** comes from hardware interrupts (Hockin) and `epoll`. In Kubernetes it describes the *logic*, not the notification transport: controllers are woken by watch events but decide from the whole current state.
- **"Self-healing"** in Kubernetes corresponds to Burgess's "computer immunology" (1998) and IBM's "autonomic computing". The Google SRE Book, Ch. 7, ends its hierarchy of automation at "autonomous systems".

---

## 4. Key results and guarantees: assumptions and where they stop holding

1. **Level-based correctness.** The system acts correctly from (desired, observed) alone, however many intermediate updates it missed (Kubernetes principles; controller-runtime: "action isn't driven off changes in individual Events, but instead is driven by actual cluster state").
   - *Assumption:* the relevant state is observable. "Object status must be 100% reconstructable by observation. Any history kept must be just an optimization" (principles).
   - *Breaks* when state is not observable. CloudFormation cannot drift-check properties "that the service… doesn't return", such as passwords ([AWS](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)). External resources without stable IDs leak, which is why finalizers and Crossplane's `external-name` annotation exist.
   - *Also breaks* when intent is really a one-off action. The standard workaround is to encode the verb as a change to desired state: `kubectl rollout restart` just stamps a `kubectl.kubernetes.io/restartedAt` annotation on the pod template.
   - Sieve found real "unobserved-state" bugs in exactly this area (below).

2. **Eventual convergence: Eventually Stable Reconciliation (ESR).** Sun et al., "Anvil: Verifying Liveness of Cluster Management Controllers", OSDI 2024, Best Paper ([paper](https://www.usenix.org/system/files/osdi24-sun-xudong.pdf)). "If at some point the desired state stops changing, then the cluster will eventually reach a state that matches it, and stay that way forever." In temporal logic: ∀d. □(□desire(d) → ◇□match(d)).
   - *Assumptions:* the desired state eventually stops changing; faults "can happen an arbitrary number of times but eventually stop happening"; scheduling is weakly fair; and conflicting controllers eventually stop interfering.
   - *Breaks* with a moving target, since "the controller will keep chasing a moving target forever". It also breaks with **controllers that fight each other**: Anvil notes the StatefulSet controller "can compete with the target controller forever". In everyday use, the HPA and `kubectl apply` fight over `replicas` ([HPA docs](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/): "thrashing or flapping").
   - *Also breaks* when the desired state is infeasible (Pods stay Pending) and when controllers have bugs.
   - The Kubernetes docs say it plainly: "potentially, your cluster never reaches a stable state."

3. **No transactions, no ordering, asynchronous actuation** ([KRM doc](https://github.com/kubernetes/design-proposals-archive/blob/main/architecture/resource-management.md)). "Desired state is updated immediately but actuated asynchronously and eventually. Kubernetes does not support atomic transactions across multiple resources… The Kubernetes API also does not provide strong ordering or consistency across multiple resources, and does not enforce referential integrity." Concurrent writers are handled with optimistic concurrency on `resourceVersion`: one write wins and the other gets a conflict and retries (API conventions; Omega, Schwarzkopf et al., EuroSys 2013).

4. **Idempotence.** Re-applying an unchanged configuration is a no-op (Terraform: "No changes. Your infrastructure matches the configuration."; the [Ansible glossary](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html)).
   - *Assumption:* every resource implementation checks before acting.
   - *Breaks* for Ansible `command`/`shell`, and for Chef `execute` without guards, which Chef documents as not idempotent by nature. It also breaks for Terraform provisioners, and for providers that normalize values and so show a diff on every plan (common practitioner knowledge; **[not a formally documented guarantee]**).

5. **Convergence of orthogonal operations** (Burgess). Many convergent operations that do not overlap reach the correct configuration "no matter which part of the configuration is incorrect, or in what order things occur."
   - *Assumptions:* the operations commute, and everything is under the tool's control.
   - *Breaks* with operations that overlap. Traugott & Brown ([LISA 2002](http://www.infrastructures.org/papers/turing/turing.html)): "there will always be unmanaged files on each host. Whether current differences between unmanaged files will have an impact on future changes is undecidable." That argument motivated congruence and immutable infrastructure.

6. **Terraform plan/apply.** A plan (1) reads the current state of existing remote objects, (2) compares the configuration to that prior state, and (3) proposes actions ([plan docs](https://developer.hashicorp.com/terraform/cli/commands/plan)). Apply runs in dependency order and in parallel where it can.
   - *Not guaranteed:*
     - Atomicity: "Terraform does not automatically roll back a partially-completed apply" ([apply docs](https://developer.hashicorp.com/terraform/cli/commands/apply)).
     - Any continuous enforcement. HCP Terraform drift detection only *reports* drift ([health assessments](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/health)).
     - Awareness of unmanaged resources.
   - A saved plan is refused if the *state* changed since it was made ("Saved plan is stale"). Changes to the *real world* after planning are not caught that way **[my reading of the source; uncertain]**.
   - State locking prevents concurrent applies, on backends that support it.

7. **Periodic resync is not a correctness mechanism for missed events.** controller-runtime's `SyncPeriod` defaults to 10 hours. Its docs say that to guard "against missed watch events" or "poll services that cannot be watched" you should return `RequeueAfter` instead ([cache.go](https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/cache/cache.go)).

8. **Empirical limits.** Sieve (Sun et al., OSDI 2022, [paper](https://www.usenix.org/conference/osdi22/presentation/sun)) found "46 serious safety and liveness bugs… in ten popular controllers". They fell into three classes: **intermediate states** (a crash in the middle of a reconcile), **stale states** (the cache "time travels" to an older view) and **unobserved states** (the controller missed an event).

---

## 5. Standard concrete examples as they appear in the sources

**Kubernetes Deployment** (the official [nginx-deployment.yaml](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)). The docs then run `kubectl set image … nginx=nginx:1.16.1` to show a rolling update.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: nginx-deployment, labels: {app: nginx}}
spec:
  replicas: 3
  selector: {matchLabels: {app: nginx}}
  template:
    metadata: {labels: {app: nginx}}
    spec:
      containers:
      - {name: nginx, image: nginx:1.14.2, ports: [{containerPort: 80}]}
```

**Demos in the KUAR style:**

- Delete a pod and a replacement appears.
- Scale the Deployment.
- **Quarantine** a pod by relabeling it. The ReplicaSet no longer selects it, so it creates a new pod while the old one stays around for debugging (KUAR, ReplicaSets chapter).

**Level vs. edge.** From the API conventions: "if a value is changed from 2 to 5 in one PUT and then back down to 3 in another PUT the system is not required to 'touch base' at 5". Bowes gives the counter-example: with 1 → 5 → 2 applied as deltas (+4, then −3) while only 3 pods had started, an edge-triggered system kills 3 and ends at 0 instead of 2. The Writing Controllers guide adds: "If an API object appears with a marker value of `true`, you can't count on having seen it turn from `false` to `true`."

**controller-runtime reconciler shape** (Kubebuilder; controller-runtime godoc). The request carries only a namespace and name, never the event itself.

```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // read object + owned objects, compare spec vs observed, create/delete, update status
    return ctrl.Result{}, nil   // or {RequeueAfter: t}; returning an error => backoff requeue
}
```

**Terraform, Brikman style** (the Gruntwork blog; TUR Ch. 1–2):

```hcl
resource "aws_instance" "example" {
  count         = 10          # change to 15 -> plan: 5 to add
  ami           = "ami-0fb653ca2d3203ac1"
  instance_type = "t2.micro"
}
```

The procedural Ansible equivalent is `- ec2: count: 10 …`. Rerunning it with `count: 15` creates 15 more instances.

**Terraform drift** ([tutorial](https://developer.hashicorp.com/terraform/tutorials/state/resource-drift)):

1. Change a security group out-of-band with the AWS CLI.
2. Run `terraform plan -refresh-only`, which prints "Objects have changed outside of Terraform".
3. Run `apply -refresh-only`, `import` the new security group, then `apply`.

Plan symbols: `+` create, `-` destroy, `~` update in place, `-/+` replace. The default replacement order is destroy-then-create unless `create_before_destroy` is set.

**Operators:** Operator SDK's Memcached (`spec.size` → Deployment replicas; "Ensure that the Deployment size is the same as specified by the Memcached CR spec"), and Kubebuilder's CronJob.

**The HPA as a "real" feedback controller:** `desiredReplicas = ceil(currentReplicas × currentMetric / desiredMetric)`. It runs every 15 s by default, uses a 10% tolerance and a 300 s scale-down stabilization window. The docs note flapping is "similar to the concept of hysteresis in cybernetics".

**SRE Book, Ch. 7** ("The Evolution of Automation at Google", Beyer et al. 2016): Prodtest paired with **idempotent fixes** that run on a schedule, which is a reconciler written as test-then-repair.

---

## 6. Misconceptions practitioners bring, and the canonical corrections

| Misconception | Canonical correction |
|---|---|
| "`kubectl apply` succeeded, so my app is running." | Apply only records intent: "Desired state is updated immediately but actuated asynchronously and eventually" (KRM). Check `status`, conditions and `observedGeneration` against `generation`, or run `kubectl rollout status`. Brian Grant's [design doc](https://github.com/kubernetes/design-proposals-archive/blob/main/architecture/declarative-application-management.md) calls this a known usability cost. |
| "Terraform keeps my infrastructure in the declared state." | Only when it runs. Between runs, drift persists, and HCP drift detection only reports it. Continuous enforcement means Crossplane, a Kubernetes controller, or a GitOps agent: "Crossplane overrides any changes made to an external resource outside of Crossplane" ([docs](https://docs.crossplane.io/latest/managed-resources/managed-resources/)). |
| "Controllers react to events." | Events are only wake-up hints. The logic is level-based, and the reconcile request carries just the name. "Level driven, not edge driven… your controller may be off for an indeterminate amount of time" (Writing Controllers). |
| "Declarative means no imperative code and no ordering." | Controllers *are* imperative code. Terraform walks a dependency graph and has `depends_on`. Kubernetes has no cross-resource ordering and relies on retries plus status reporting (KRM). |
| "Delete it from the manifest and it disappears." | Terraform plans a destroy. `kubectl apply` does not: prune is alpha, and the docs recommend `kubectl delete -f` ([docs](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/)). Argo CD auto-sync "will not delete resources" by default ([docs](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)). Flux needs `prune: true`. |
| "Kubernetes rolls back bad deployments automatically." | "Kubernetes takes no action on a stalled Deployment other than to report a status condition with `reason: ProgressDeadlineExceeded`" ([Deployment docs](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)). |
| "My YAML file / Git is the only writer." | Objects have multiple writers: the HPA, defaulting, admission webhooks, `kubectl scale`. "A Kubernetes object should be managed using only one technique. Mixing… results in undefined behavior" (Object Management). With an HPA, "don't set `.spec.replicas`". SSA field ownership formalizes this, and Terraform's `ignore_changes` is the analogue. |
| "The Terraform state file is the real infrastructure." | It is a mapping plus a cache. Refresh reads the world. With misconfigured credentials Terraform "may be misled into thinking that all of the managed objects have been deleted" ([refresh docs](https://developer.hashicorp.com/terraform/cli/commands/refresh)). |
| "Controllers are stateless." | Correctness must not *depend* on history, but real controllers cache. The ReplicaSet controller keeps "expectations" so a stale informer cache does not make it create pods twice: "A ReplicaSet is temporarily suspended after creating/deleting these many replicas. It resumes normal action after observing the watch events for them" ([source](https://github.com/kubernetes/kubernetes/blob/master/pkg/controller/replicaset/replica_set.go)). |
| "Idempotent, declarative and convergent are the same thing." | They are distinct: see Burgess's Ô² = Ô vs. Ô q = q₀, and the non-idempotent escape hatches in declarative tools (§4.4). |
| "Self-healing fixes everything." | It only fixes what some controller observes and owns. It cannot fix a crash-looping image or an infeasible spec. |

The canonical way to *correct* these misconceptions is by demonstration. Kill a pod and watch it return. Walk the 2 → 5 → 3 timeline. Put spec and status side by side. Change something out-of-band and run `terraform plan`. Read the KRM list of what Kubernetes does *not* guarantee.

---

## 7. For a short lesson: essential, common extras, leave out

**Essential:**

- Desired vs. actual state.
- Declarative vs. imperative, taught through the replica count or 10 → 15.
- The observe → diff → act loop: thermostat, then the four-line `for {}`.
- Level-triggered vs. edge-triggered, taught through the missed-event example.
- **One-shot (Terraform) vs. continuous (Kubernetes) reconciliation**, and what each means for drift.
- Idempotence.
- Eventual consistency: apply is not the same as done; watch `status`.

**Common extras:**

- The controller chain (Deployment → ReplicaSet → Pod → scheduler → kubelet) and choreography vs. orchestration.
- Operators and CRDs.
- GitOps's four principles.
- Terraform state, refresh and locking.
- Conflicting writers (HPA vs. apply; Server-Side Apply).
- The ESR statement in plain English.
- The CFEngine → Puppet → Terraform → Kubernetes lineage.
- The mapping to control-theory vocabulary.

**Leave out:**

- Informer, workqueue and DeltaFIFO internals.
- `resourceVersion` mechanics.
- Strategic-merge and 3-way-merge internals.
- The details of Terraform's graph walk.
- TLA+ notation and proof strategy.
- PID tuning and stability analysis.
- Promise Theory.
- Authoring CRDs and webhooks.
- Templating debates (Helm/Kustomize/HCL vs. general-purpose languages).
- Tool-by-tool feature comparisons.

---

## 8. Systems canonically cited for each model, with their mechanisms

| System | Model | Specific mechanism |
|---|---|---|
| **Kubernetes** | Continuous, level-based | Objects with `spec`/`status` in the API server (etcd behind it). Controllers in kube-controller-manager use list+watch informers, a workqueue and `Reconcile`. Optimistic concurrency on `resourceVersion`. `ownerReferences` with garbage collection, and finalizers. The scheduler is itself a controller that binds Pods. The kubelet is a node-level reconciler. SSA tracks field ownership. |
| **Borg / Omega** | Precursors | Reconciliation loops shared across Borg, Omega and Kubernetes (Burns et al. 2016). Omega used shared state with optimistic concurrency (Schwarzkopf et al., EuroSys 2013). |
| **Terraform** | One-shot | HCL configuration; state file (mapping, metadata, cache); refresh → diff → plan; apply walks a resource graph in parallel through provider CRUD; state locking; no rollback. Invoked by a human or CI. HCP drift detection only reports. |
| **Pulumi** | One-shot | A general-purpose-language program registers desired resources. The engine diffs against the last deployed state through providers. |
| **AWS CloudFormation** | One-shot | Templates, stacks, change sets. Stack updates *do* roll back on failure, unlike Terraform. Drift detection is detect-only and covers only "property values that are explicitly set". |
| **CFEngine** (Burgess 1993–) | Continuous, convergent | Convergent promises. `cf-execd` runs `cf-agent` every 5 minutes by default ([docs](https://docs.cfengine.com/docs/master/reference/components/cf-execd/)). |
| **Puppet** | Continuous | Declarative manifests compile to a catalog. The agent pulls and applies it every 30 minutes by default (`runinterval`). Providers check and then fix. `noop` mode is available. |
| **Chef** | Continuous (periodic runs) | Resources with "test and repair" (`converge_if_changed`, `not_if`/`only_if` guards). |
| **Ansible** | Mostly one-shot | Idempotent modules (`state: present`). "Push mode is the default"; `ansible-pull` is optional. Check mode. |
| **PowerShell DSC** | Continuous | Resources implement Get/Test/Set. The Local Configuration Manager's `ConfigurationMode`: `ApplyOnly`, `ApplyAndMonitor` (the default, which *reports* drift) and `ApplyAndAutoCorrect` (which re-applies), every 15 minutes ([docs](https://learn.microsoft.com/en-us/powershell/dsc/managing-nodes/metaconfig?view=dsc-1.1)). It neatly shows the detect-vs-correct distinction. |
| **Docker Swarm** | Continuous | "The swarm manager node constantly monitors the cluster state and reconciles any differences between the actual state and your expressed desired state" ([docs](https://docs.docker.com/engine/swarm/)). |
| **Argo CD / Flux** (GitOps) | Continuous, pull-based | They pull from Git, diff against the live cluster and sync. Argo CD polls about every 3 minutes (`timeout.reconciliation`); self-heal and prune are opt-in. Flux reconciles every `.spec.interval`, uses a "server-side apply dry-run to detect and correct drift", and prune is opt-in. OpenGitOps principles: Declarative, Versioned and Immutable, Pulled Automatically, Continuously Reconciled ("continues to happen, not that it must be instantaneous"). |
| **Crossplane** (also ACK, Config Connector) | Continuous, for cloud resources | Kubernetes controllers for external APIs. They revert console changes, use an `external-name` annotation for identity, a `poll-interval`, and support `Observe`-only management policies. |
| **HPA** | Continuous, closest to classical feedback | Proportional formula, tolerance, stabilization window (hysteresis). |

---

## 9. Claims that are commonly overstated or subtly wrong

1. **"Kubernetes guarantees your desired state."** It guarantees only best-effort, *eventual* convergence under ESR-style assumptions, and the cluster may never be stable (Kubernetes docs; Anvil).
2. **"Declarative configuration eliminates drift."** Only continuous reconciliation *corrects* drift, and only for fields and resources that are managed. Unmanaged state stays a blind spot: Traugott & Brown's undecidability argument; Morris's ["ConfigurationSynchronization"](https://martinfowler.com/bliki/ConfigurationSynchronization.html) (2013): "when some part of the system not managed by automation tools does cause an issue, the effects are unexpected"; CloudFormation checks explicit properties only.
3. **"Level-triggered means polling / no events."** Kubernetes prefers watches ("Watch is preferred over polling", principles). Level-based is a property of the decision logic. The principles doc even posits a "CAP-like theorem" for polling vs. events: performance, reliability and simplicity, "pick any 2".
4. **"Resync protects against missed events."** controller-runtime says no, and recommends `RequeueAfter` (§4.7).
5. **"Kubernetes does automated rollbacks."** The Overview page's "automated rollouts and rollbacks" is often read that way. In fact the Deployment controller only reports `ProgressDeadlineExceeded`, and rollback (`kubectl rollout undo`) is a separate action.
6. **"Kubernetes eliminates orchestration."** It moves orchestration inside controllers: the Deployment controller *does* sequence a rolling update. The KRM doc: "Imperative operations and flowchart-like workflow orchestration can be built on top of its declarative model."
7. **"Terraform is declarative, so order doesn't matter."** It builds a dependency graph, has `depends_on`, replaces resources destroy-first by default, and provisioners are imperative.
8. **"Idempotent" used to mean "convergent"**, and "declarative tools are idempotent by construction". Both are wrong (§4.4, §4.5). Wikipedia's article on Mark Burgess even notes that his term convergence "is now often inaccurately just called idempotence" (a secondary source).
9. **"Single source of truth."** The phrase is overloaded (§3). Objects are co-owned by several writers.
10. **"Kubernetes controllers are control loops in the control-theory sense."** Most are set-point matchers with no model of the system's dynamics, closer to on-off control than PID. Åström & Murray note that on-off control "typically results in a system where the controlled variables oscillate". The HPA, with its hysteresis, is the closest to textbook feedback control. This characterization is my synthesis; **no single canonical source states it**.
11. **"GitOps = YAML in Git."** OpenGitOps also requires *pull* and *continuous reconciliation*, so push-based CI running `kubectl apply` does not satisfy principles 3 and 4.
12. **"Terraform plan shows exactly what apply will do."** The world can change between plan and apply, values can be "known after apply", and a failed apply leaves partial changes.

---

## 10. Which parts to animate, which to have learners do, which to leave for reading

The mapping is my recommendation. It rests on multimedia-learning research: Mayer, *Multimedia Learning* (3rd ed. 2020); Mayer & Moreno, "Nine ways to reduce cognitive load…", *Educational Psychologist* 2003; Tversky, Morrison & Bétrancourt, "Animation: can it facilitate?", *IJHCS* 2002, which finds animation helps mainly when it depicts change over time and is paced or segmented; Höffler & Leutner's 2007 meta-analysis. It also draws on predict-observe-explain teaching.

**Best as narrated animation** (processes that unfold over time and cause each other, which static diagrams show poorly):

- The observe → diff → act cycle: the thermostat morphing into the replica controller.
- Self-healing: a pod dies, status diverges from spec, and a replacement appears.
- The **2 → 5 → 3 / 1 → 5 → 2 timeline** with a dropped event, run by an edge-triggered and a level-triggered controller side by side.
- The **cascade through the API server**: Deployment → ReplicaSet → Pods → scheduler binds → kubelet runs → status flows back.
- A Terraform plan as a three-way picture (config, state, real world) with drift appearing between runs.

Keep each segment short and signaled, and pause at each step of the loop.

**Best by doing** (these misconceptions are corrected by prediction and then observation):

- In `kind`/`minikube`:
  - delete a pod, scale, and relabel a pod to quarantine it;
  - run `kubectl apply` and then read `status` and `rollout status`, to see that apply is not the same as done;
  - make the HPA and `apply` fight over `replicas`.
- With Terraform: change a resource in the console, then run `plan` / `-refresh-only`; delete a block and see a destroy planned; compare with `kubectl apply` without prune.
- **Write a 20-line reconciler** (for example for files in a directory). Inject dropped events and restarts, and watch the edge-triggered version fail while the level-triggered version recovers.
- An interactive simulation of two controllers fighting, or of an infeasible desired state that never converges.

**Best by reading** (precise, reference-like, and meant for re-reading):

- Exact guarantees and their assumptions: ESR and fairness; the KRM list of what Kubernetes does *not* provide; Terraform's no-rollback and stale-plan rules.
- The terminology crosswalk (§3).
- Tool-by-tool mechanisms (§8).
- The history: CFEngine convergence → Traugott's congruence → IaC → Kubernetes → GitOps.
- API conventions: spec/status, conditions, `observedGeneration`.

---

### Key primary sources (quick list)

- Kubernetes docs: [Controllers](https://kubernetes.io/docs/concepts/architecture/controller/), [Objects](https://kubernetes.io/docs/concepts/overview/working-with-objects/), [Object Management](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/), [Overview](https://kubernetes.io/docs/concepts/overview/)
- Kubernetes design docs: [Design Principles](https://github.com/kubernetes/design-proposals-archive/blob/main/architecture/principles.md), [API Conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md), [Resource Model](https://github.com/kubernetes/design-proposals-archive/blob/main/architecture/resource-management.md), [Writing Controllers](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-api-machinery/controllers.md)
- Burns, Grant, Oppenheimer, Brewer, Wilkes, "Borg, Omega, and Kubernetes", *ACM Queue* 14(1), 2016
- Burns, Beda, Hightower (+ Evenson), *Kubernetes: Up & Running*, 3rd ed. 2022: Ch. 1, Ch. 9 ReplicaSets, Ch. 10 Deployments
- Hausenblas & Schimanski, *Programming Kubernetes*, 2019, Ch. 1 · Ibryam & Huß, *Kubernetes Patterns* 2nd ed. 2023, Ch. 3/27/28 · Lukša, *Kubernetes in Action*, 2018, §11.2
- Brikman, *Terraform: Up & Running* 3rd ed. 2022, Ch. 1–3 · [Terraform docs](https://developer.hashicorp.com/terraform/intro) · Morris, *Infrastructure as Code* 2nd ed. 2020, Ch. 2, 4
- Burgess, "Computer Immunology", LISA 1998 · Traugott & Brown, "Why Order Matters", LISA 2002 · Fowler, SnowflakeServer (2012) · Morris, ConfigurationSynchronization (2013)
- [OpenGitOps Principles v1](https://github.com/open-gitops/documents/blob/main/PRINCIPLES.md) · Richardson, "GitOps – Operations by Pull Request", Weaveworks, 2017
- Sun et al., Sieve, OSDI 2022 · Sun et al., Anvil, OSDI 2024 (Best Paper)
- Åström & Murray, *Feedback Systems*, 2008, Ch. 1 · Beyer et al., *Site Reliability Engineering*, 2016, Ch. 7
- Hockin, "Edge vs. Level triggered logic" (2017) · Bowes, "Level Triggering and Reconciliation in Kubernetes" (2018) · Beda, "Core Kubernetes: Jazz Improv over Orchestration" (2017) · Philips, "Introducing Operators" (CoreOS, 2016)
