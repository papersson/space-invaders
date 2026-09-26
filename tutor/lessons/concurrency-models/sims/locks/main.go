// Shared memory with locks: each account has its own mutex. A transfer locks the
// account it takes from, then the account it pays into. Run a transfer A->B and a
// transfer B->A at the same moment, many times, and count the runs that get stuck.
// Then lock in a fixed order (lower account number first) and count again.
package main

import (
	"fmt"
	"sync"
	"time"
)

type account struct {
	id      int
	mu      sync.Mutex
	balance int
}

func transfer(from, to *account, amt int, ordered bool) {
	first, second := from, to
	if ordered && to.id < from.id {
		first, second = to, from
	}
	first.mu.Lock()
	time.Sleep(time.Microsecond) // some work while holding the first lock
	second.mu.Lock()
	from.balance -= amt
	to.balance += amt
	second.mu.Unlock()
	first.mu.Unlock()
}

func trial(ordered bool) bool {
	a, b := &account{id: 1, balance: 100}, &account{id: 2, balance: 100}
	var start sync.WaitGroup
	start.Add(1)
	done := make(chan bool, 2)
	go func() { start.Wait(); transfer(a, b, 30, ordered); done <- true }()
	go func() { start.Wait(); transfer(b, a, 20, ordered); done <- true }()
	start.Done()
	timeout := time.After(200 * time.Millisecond)
	for i := 0; i < 2; i++ {
		select {
		case <-done:
		case <-timeout:
			return true
		}
	}
	return false
}

func main() {
	const runs = 1000
	for _, ordered := range []bool{false, true} {
		stuck := 0
		for i := 0; i < runs; i++ {
			if trial(ordered) {
				stuck++
			}
		}
		label := "each transfer locks its own account first"
		if ordered {
			label = "every transfer locks the lower account number first"
		}
		fmt.Printf("%s: stuck in %d of %d runs\n", label, stuck, runs)
	}
}
