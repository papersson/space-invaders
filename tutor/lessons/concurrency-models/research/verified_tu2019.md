# Checked against the primary source: Tu, Liu, Song & Zhang, ASPLOS 2019

"Understanding Real-World Concurrency Bugs in Go", ASPLOS 2019 (songlh.github.io/paper/go-study.pdf), read in this session.

- Six applications: Docker, Kubernetes, etcd, CockroachDB, gRPC, BoltDB. 171 concurrency bugs: 85 blocking, 86 non-blocking; 105 caused by wrong shared memory protection, 66 by wrong message passing.
- Blocking bugs (Table 6): shared memory 28 Mutex + 5 RWMutex + 3 Wait = 36; message passing 29 Chan + 16 Chan w/ + 4 Lib = 49. Text: "around 42% blocking bugs caused by errors in protecting shared memory, and 58% are caused by errors in message passing."
- Observation 3: "Contrary to the common belief that message passing is less error-prone, more blocking bugs in our studied Go applications are caused by wrong message passing than by wrong shared memory protection."
- Non-blocking bugs (Table 9): shared memory 46 traditional + 11 anonymous function + 6 waitgroup + 6 lib = 69; message passing 16 chan + 1 lib = 17.
