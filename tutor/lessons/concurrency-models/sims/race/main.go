// One goroutine owns the balance; cash machines talk to it only through a channel.
// Each machine asks for the balance, and withdraws $100 if the balance was at least $100.
// Count how often both machines withdraw from a $100 balance, over many runs.
// Then the same with one message, "withdraw if sufficient funds".
package main

import (
	"fmt"
	"sync"
)

type req struct {
	kind   string // "balance", "withdraw", "withdraw-if-sufficient"
	amount int
	reply  chan int
}

func account(balance int, reqs chan req) {
	for r := range reqs {
		switch r.kind {
		case "balance":
			r.reply <- balance
		case "withdraw":
			balance -= r.amount
			r.reply <- balance
		case "withdraw-if-sufficient":
			if balance >= r.amount {
				balance -= r.amount
				r.reply <- 1
			} else {
				r.reply <- 0
			}
		case "final":
			r.reply <- balance
		}
	}
}

func ask(reqs chan req, kind string, amount int) int {
	reply := make(chan int)
	reqs <- req{kind, amount, reply}
	return <-reply
}

func trial(oneMessage bool) int {
	reqs := make(chan req)
	go account(100, reqs)
	var wg sync.WaitGroup
	for m := 0; m < 2; m++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if oneMessage {
				ask(reqs, "withdraw-if-sufficient", 100)
			} else if ask(reqs, "balance", 0) >= 100 {
				ask(reqs, "withdraw", 100)
			}
		}()
	}
	wg.Wait()
	final := ask(reqs, "final", 0)
	close(reqs)
	return final
}

func main() {
	const runs = 100000
	for _, one := range []bool{false, true} {
		overdrawn := 0
		for i := 0; i < runs; i++ {
			if trial(one) < 0 {
				overdrawn++
			}
		}
		label := "check, then withdraw (two messages)"
		if one {
			label = "withdraw if sufficient (one message)"
		}
		fmt.Printf("%s: overdrawn to -$100 in %d of %d runs\n", label, overdrawn, runs)
	}
}
