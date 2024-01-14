package kvpaxos

import (
	"cse-513/src/paxos"
	"encoding/gob"
	"log"
	"math/rand"
	"net"
	"net/rpc"
	"os"
	"sync"
	"sync/atomic"
	"syscall"
)

const Debug = 0

type KVPaxos struct {
	mu                sync.Mutex
	l                 net.Listener
	me                int
	dead              int32             // for testing
	unreliable        int32             // for testing
	px                *paxos.Paxos      // paxos
	operation_history map[int64]bool    // history map to save the execution of an operation (mapped by operation ids).
	key_value         map[string]string // key-value pairs.
	log_threshold     int
}

type Op struct {
	OperationId int64  // operation id
	Key         string // key
	Value       string // value
	Type        string // operation type -> Get, Put, Append
}

func DPrintf(format string, a ...interface{}) (n int, err error) {
	if Debug > 0 {
		log.Printf(format, a...)
	}
	return
}

func (kv *KVPaxos) Get(args *GetArgs, reply *GetReply) error {
	kv.mu.Lock()

	// if operation is recorded history log
	if kv.operation_history[args.OperationId] {
		reply.Value = kv.key_value[args.Key] // Get found the value
		reply.Err = OK                       // Reply status is OK
		kv.mu.Unlock()
		return nil
	}

	// if operation is not recorded history log
	var getOperation Op = Op{OperationId: args.OperationId, Key: args.Key, Type: "Get"}
	var op Op
	// Compare args.operation id and current operation's operation id to find called operation by
	// incrementing log sequence iteratively and looking for operation.
	for {
		// first, check the status of peer's activity on paxos to see if it is decided or pending?
		status, valueInterface := kv.px.Status(kv.log_threshold)
		if status == paxos.Decided { // if consensus is reached, peer must save corresponding interface locally
			op = valueInterface.(Op)
		} else { // otherwise, start a prepare/accept request for this sequence
			// and wait till consensus is reached.
			kv.px.Start(kv.log_threshold, getOperation)
			for {
				status, valueInterface := kv.px.Status(kv.log_threshold)
				if status == paxos.Decided {
					op = valueInterface.(Op)
					break
				}
			}
		}

		// now we have interface and an operation connected to this interface.
		// before calling paxos done for that operation, we must store the key_value map and operational id.
		// if op is either put or append we must update value.
		// if op is get, we must just return with value in reply message.
		if op.Type == "Put" { // Put brings with new key both globally and locally
			kv.key_value[op.Key] = op.Value
		} else if op.Type == "Append" {
			value, exist := kv.key_value[op.Key]
			if exist { // if Append locally exists, update value.
				kv.key_value[op.Key] = value + op.Value
			} else { // otherwise
				kv.key_value[op.Key] = op.Value
			}
		}

		// store the operational id of the corresponding op.
		kv.operation_history[op.OperationId] = true
		kv.px.Done(kv.log_threshold) // done with this number.
		kv.log_threshold++           // assign new number.

		// if the found op is the operation which calls this function (args's operation id)
		if args.OperationId == op.OperationId {
			reply.Value = kv.key_value[args.Key]
			break
		}
		// otherwise try with new number.
	}
	kv.mu.Unlock()
	return nil
}
func (kv *KVPaxos) Completed(args *int64, reply *bool) error {
	// Marks Operation id as completed
	kv.mu.Lock()
	delete(kv.operation_history, *args)
	kv.mu.Unlock()
	*reply = true
	return nil
}

// Same approach as in Get server function
func (kv *KVPaxos) PutAppend(args *PutAppendArgs, reply *PutAppendReply) error {
	kv.mu.Lock()

	// if operation is recorded history log
	if kv.operation_history[args.OperationId] {
		reply.Err = OK
		// fmt.Printf("This operation is recorded")
		kv.mu.Unlock()
		return nil
	}

	var appendPutArgs Op = Op{OperationId: args.OperationId, Key: args.Key,
		Value: args.Value, Type: args.Op}
	var op Op
	for {
		status, valueInterface := kv.px.Status(kv.log_threshold)
		if status == paxos.Decided {
			op = valueInterface.(Op)
		} else {
			kv.px.Start(kv.log_threshold, appendPutArgs)
			for {
				status, valueInterface := kv.px.Status(kv.log_threshold)
				if status == paxos.Decided {
					op = valueInterface.(Op)
					break
				}
			}

		}
		if op.Type == "Put" {
			kv.key_value[op.Key] = op.Value
		} else if op.Type == "Append" {
			if curr, exist := kv.key_value[op.Key]; exist {
				kv.key_value[op.Key] = curr + op.Value
			} else {
				kv.key_value[op.Key] = op.Value
			}
		}
		kv.operation_history[op.OperationId] = true
		kv.px.Done(kv.log_threshold)
		kv.log_threshold++

		if appendPutArgs.OperationId == op.OperationId {
			reply.Err = OK
			break
		}
	}
	kv.mu.Unlock()
	return nil
}

// tell the server to shut itself down.
// please do not change these two functions.
func (kv *KVPaxos) kill() {
	DPrintf("Kill(%d): die\n", kv.me)
	atomic.StoreInt32(&kv.dead, 1)
	kv.l.Close()
	kv.px.Kill()
}

// call this to find out if the server is dead.
func (kv *KVPaxos) isdead() bool {
	return atomic.LoadInt32(&kv.dead) != 0
}

// please do not change these two functions.
func (kv *KVPaxos) setunreliable(what bool) {
	if what {
		atomic.StoreInt32(&kv.unreliable, 1)
	} else {
		atomic.StoreInt32(&kv.unreliable, 0)
	}
}

func (kv *KVPaxos) isunreliable() bool {
	return atomic.LoadInt32(&kv.unreliable) != 0
}

// servers[] contains the ports of the set of
// servers that will cooperate via Paxos to
// form the fault-tolerant key/value service.
// me is the index of the current server in servers[].
func StartServer(servers []string, me int) *KVPaxos {
	// call gob.Register on structures you want
	// Go's RPC library to marshall/unmarshall.
	gob.Register(Op{})

	kv := new(KVPaxos)
	kv.me = me

	kv.key_value = make(map[string]string)
	kv.operation_history = make(map[int64]bool)
	kv.log_threshold = 0

	rpcs := rpc.NewServer()
	rpcs.Register(kv)

	kv.px = paxos.Make(servers, me, rpcs)

	os.Remove(servers[me])
	l, e := net.Listen("unix", servers[me])
	if e != nil {
		log.Fatal("listen error: ", e)
	}
	kv.l = l

	// please do not change any of the following code,
	// or do anything to subvert it.

	go func() {
		for kv.isdead() == false {
			conn, err := kv.l.Accept()
			if err == nil && kv.isdead() == false {
				if kv.isunreliable() && (rand.Int63()%1000) < 100 {
					// discard the request.
					conn.Close()
				} else if kv.isunreliable() && (rand.Int63()%1000) < 200 {
					// process the request but force discard of reply.
					c1 := conn.(*net.UnixConn)
					f, _ := c1.File()
					err := syscall.Shutdown(int(f.Fd()), syscall.SHUT_WR)
					if err != nil {
						// fmt.Printf("shutdown: %v\n", err)
					}
					go rpcs.ServeConn(conn)
				} else {
					go rpcs.ServeConn(conn)
				}
			} else if err == nil {
				conn.Close()
			}
			if err != nil && kv.isdead() == false {
				// fmt.Printf("KVPaxos(%v) accept: %v\n", me, err.Error())
				kv.kill()
			}
		}
	}()

	return kv
}
