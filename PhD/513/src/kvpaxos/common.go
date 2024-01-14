package kvpaxos

const (
	OK       = "OK"
	ErrNoKey = "ErrNoKey"
)

type Err string

type PutAppendReply struct {
	Err Err
}

type GetArgs struct {
	Key         string // get function key used to map to value
	OperationId int64  // OperationId that we used for each operation
}

// Put or Append
type PutAppendArgs struct {
	Key         string // key
	Value       string // value
	Op          string // "Put" or "Append"
	OperationId int64  // OperationId that we used for each operation
}

type GetReply struct {
	Err   Err
	Value string
}
