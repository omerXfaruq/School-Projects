package kvpaxos

import (
	"crypto/rand"
	"math/big"
	"net/rpc"
)

type Clerk struct {
	servers []string
	// clientId int64 // client ID for each client
}

func nrand() int64 {
	max := big.NewInt(int64(1) << 62)
	bigx, _ := rand.Int(rand.Reader, max)
	x := bigx.Int64()
	return x
}

func MakeClerk(servers []string) *Clerk {
	ck := new(Clerk)
	ck.servers = servers
	// ck.clientId = nrand() // assigned random client IDs
	return ck
}

// call() sends an RPC to the rpcname handler on server srv with arguments args, waits for the reply,
// and leaves the reply in reply. the reply argument should be a pointer to a reply structure.
// the return value is true if the server responded, and false if call() was not able to contact the server.
// in particular, the reply's contents are only valid if call() returned true.
// you should assume that call() will return an error after a while if the server is dead. don't provide your
// own time-out mechanism.
// please use call() to send all RPCs, in client.go and server.go.  please don't change this function.
func call(srv string, rpcname string, args interface{}, reply interface{}) bool {
	c, errx := rpc.Dial("unix", srv)
	if errx != nil {
		return false
	}
	defer c.Close()

	err := c.Call(rpcname, args, reply)
	if err == nil {
		return true
	}
	// fmt.Println(err)
	return false
}

// fetch the current value for a key. returns "" if the key does not exist.
// keeps trying forever in the face of all other errors. This function will get a value
// for a given key by a call, and we need some args to send which must include the key.
// call(srv string, rpcname string, args interface{}, reply interface{})
// srv string must be the peer id -> ck.servers[]
// rpcname string must be the function. -> KVPaxos.Get
// args -> getCallerArgs, reply -> getResponseArgs
func (ck *Clerk) Get(key string) string {

	var getArgs GetArgs = GetArgs{Key: key, OperationId: nrand()}
	var replyArgs GetReply
	var i int = 0
	// maybe we can implement some kind of a timer counter here instead of busy wait
	// but it is stated that we should not implement any timeout mechanism,
	// so, busy wait should be fine.
	for {
		if call(ck.servers[i%len(ck.servers)], "KVPaxos.Get", &getArgs, &replyArgs) {
			break
		}
		i++ // call each server (repeatedly to cover after server heals)
	}

	node := 0
	var bo bool
	// Clear key from operation_history
	for {
		for {
			if call(ck.servers[node%len(ck.servers)], "KVPaxos.Completed", &getArgs.OperationId, &bo) {
				break
			}
		}
		node++
		if node > i {
			break
		}
	}

	return replyArgs.Value
}

// shared by Put and Append.
// call(srv string, rpcname string, args interface{}, reply interface{})
// - srv string must be the peer id -> ck.servers[]
// - rpcname string must be the function. -> KVPaxos.PutAppend
// - args -> putCallerArgs, reply -> responseArgs
func (ck *Clerk) PutAppend(key string, value string, op string) {
	var putAppendArgs PutAppendArgs = PutAppendArgs{Key: key, Value: value, Op: op,
		OperationId: nrand()}
	var replyArgs GetReply
	var i int = 0
	for {
		if call(ck.servers[i%len(ck.servers)], "KVPaxos.PutAppend", &putAppendArgs, &replyArgs) {
			return // put will return after putting the value with argument.
		}
		i++ // call each server (repeatedly to cover after server heals)
	}
}

func (ck *Clerk) Put(key string, value string) {
	ck.PutAppend(key, value, "Put")
}
func (ck *Clerk) Append(key string, value string) {
	ck.PutAppend(key, value, "Append")
}
