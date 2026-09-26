// Two account processes that share nothing and talk only over unbuffered channels.
// To transfer, an account sends "credit this amount" to the other account and waits
// until the other account has taken it. Start a transfer A->B and a transfer B->A at
// the same moment, and count the runs in which both accounts end up waiting on each other.
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

func (a *account) run(other *account, done chan bool) {
	for {
		select {
		case amt := <-a.credits:
			a.balance += amt
		case amt := <-a.transfer:
			a.balance -= amt
			other.credits <- amt // waits until the other account takes it
			done <- true
		}
	}
}

func trial() bool {
	a := &account{make(chan int), make(chan int, 1), 100}
	b := &account{make(chan int), make(chan int, 1), 100}
	a.transfer <- 30 // both transfers are waiting before either account starts
	b.transfer <- 20
	done := make(chan bool, 2)
	go a.run(b, done)
	go b.run(a, done)
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
	stuck := 0
	for i := 0; i < runs; i++ {
		if trial() {
			stuck++
		}
	}
	fmt.Printf("transfers A->B and B->A at once: both accounts stuck waiting in %d of %d runs\n", stuck, runs)
}
