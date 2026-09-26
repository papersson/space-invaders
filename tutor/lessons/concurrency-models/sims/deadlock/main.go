// Two account processes that share nothing and talk only over unbuffered channels.
// To transfer, an account sends "credit this amount" to the other account and waits
// until the other account has taken it. Start a transfer A->B and a transfer B->A at
// the same moment, and count the runs in which both accounts end up waiting on each other.
// Then break the cycle: the account hands the send to a new goroutine and keeps listening.
package main

import (
	"fmt"
	"time"
)

type account struct {
	credits  chan int
	transfer chan int
	balance  int
}

func (a *account) run(other *account, done chan bool, handOff bool) {
	for {
		select {
		case amt := <-a.credits:
			a.balance += amt
		case amt := <-a.transfer:
			a.balance -= amt
			if handOff {
				go func() { other.credits <- amt; done <- true }() // keep listening meanwhile
			} else {
				other.credits <- amt // waits until the other account takes it
				done <- true
			}
		}
	}
}

func trial(handOff bool) bool {
	a := &account{make(chan int), make(chan int, 1), 100}
	b := &account{make(chan int), make(chan int, 1), 100}
	a.transfer <- 30 // both transfers are waiting before either account starts
	b.transfer <- 20
	done := make(chan bool, 2)
	go a.run(b, done, handOff)
	go b.run(a, done, handOff)
	timeout := time.After(200 * time.Millisecond)
	for i := 0; i < 2; i++ {
		select {
		case <-done:
		case <-timeout:
			return true // stuck: each account is waiting for the other
		}
	}
	return false
}

func main() {
	const runs = 1000
	for _, handOff := range []bool{false, true} {
		stuck := 0
		for i := 0; i < runs; i++ {
			if trial(handOff) {
				stuck++
			}
		}
		label := "each account waits in its own send"
		if handOff {
			label = "each account hands the send off and keeps listening"
		}
		fmt.Printf("transfers A->B and B->A at once, %s: stuck in %d of %d runs\n", label, stuck, runs)
	}
}
