// The same request handler in Go: fetchUser takes 1.0 s, fetchOrders fails after 0.1 s.
// Written with bare goroutines and channels, and with errgroup plus a context.
// Each version serves 1000 requests at once; we count goroutines left over.
package main

import (
	"context"
	"errors"
	"fmt"
	"runtime"
	"sync"
	"time"

	"golang.org/x/sync/errgroup"
)

func fetchUser(ctx context.Context) (string, error) {
	select {
	case <-time.After(1000 * time.Millisecond):
		return "ada", nil
	case <-ctx.Done():
		return "", ctx.Err()
	}
}

func fetchOrders(ctx context.Context) ([]string, error) {
	select {
	case <-time.After(100 * time.Millisecond):
		return nil, errors.New("orders service down")
	case <-ctx.Done():
		return nil, ctx.Err()
	}
}

// bare goroutines: return on the first error; the other goroutine is left behind,
// and blocks forever on its send because nobody receives.
func handlerBare() error {
	users, errs := make(chan string), make(chan error)
	go func() { u, _ := fetchUser(context.Background()); users <- u }()
	go func() { _, err := fetchOrders(context.Background()); errs <- err }()
	select {
	case <-users:
		return <-errs
	case err := <-errs:
		return err
	}
}

// errgroup: the first error cancels ctx; Wait returns after every goroutine has returned.
func handlerGroup() error {
	g, ctx := errgroup.WithContext(context.Background())
	g.Go(func() error { _, err := fetchUser(ctx); return err })
	g.Go(func() error { _, err := fetchOrders(ctx); return err })
	return g.Wait()
}

func serve(name string, h func() error) {
	base := runtime.NumGoroutine()
	start := time.Now()
	var wg sync.WaitGroup
	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func() { defer wg.Done(); _ = h() }()
	}
	wg.Wait()
	took := time.Since(start)
	now := runtime.NumGoroutine() - base
	time.Sleep(1200 * time.Millisecond)
	later := runtime.NumGoroutine() - base
	fmt.Printf("%s: all 1000 handlers returned after %.2fs; goroutines left over: %d; 1.2 s later: %d\n",
		name, took.Seconds(), now, later)
}

func main() {
	serve("bare goroutines", handlerBare)
	serve("errgroup + context", handlerGroup)
	fmt.Println(runtime.Version())
}
