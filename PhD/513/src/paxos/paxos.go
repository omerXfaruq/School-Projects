package paxos

// The application interface:
// px = paxos.Make(peers []string, me string)
// px.Start(seq int, v interface{}) -- start agreement on new instance
// px.Status(seq int) (Fate, v interface{}) -- get info about an instance
// px.Done(seq int) -- ok to forget all instances <= seq
// px.Max() int -- highest instance seq known, or -1
// px.Min() int -- instances before this seq have been forgotten

import (
	"log"
	"math/rand"
	"net"
	"net/rpc"
	"os"
	"strconv"
	"sync"
	"sync/atomic"
	"syscall"
	"time"
)

// px.Status() return values, indicating  whether an agreement has been decided,
// or Paxos has not yet reached agreement, or it was agreed but forgotten (i.e. < Min()).
type Fate int

const (
	Decided   Fate = iota + 1 // decided
	Pending                   // still not decided.
	Forgotten                 // previously decided but forgotten now.
)

// These are the variables given in the psuedocode.
type instance struct {
	n_p           string      // proposal number
	n_a           string      // accept number
	v_a           interface{} // accept value, interface
	instanceState Fate        // instance state
}

type Paxos struct {
	mu            sync.Mutex
	l             net.Listener
	dead          int32             // for testing
	unreliable    int32             // for testing
	rpcCount      int32             // for testing
	me            int               // index into peers[]
	peers         []string          // peers
	instances     map[int]*instance // mapped by sequence number, mapping to corresponding instances
	majorityCount int               // majority count among the paxos peers
	maxSeqNums    []int             // indexed by paxos peer id and keeps the sequence number
}

// call() sends an RPC to the rpcname handler on server srv with arguments args, waits for the reply,
// and leaves the reply in reply. the reply argument should be a pointer  to a reply structure.
// the return value is true if the server responded, and false if call() was not able to contact
// the server. in particular,  the replys contents are only valid if call() returned true.
// you should assume that call() will time out and return an error after a while if it does not
// get a reply from the server. please use call() to send all RPCs, in client.go and server.go.
// please do not change this function.
func call(srv string, name string, args interface{}, reply interface{}) bool {
	c, err := rpc.Dial("unix", srv)
	if err != nil {
		err1 := err.(*net.OpError)
		if err1.Err != syscall.ENOENT && err1.Err != syscall.ECONNREFUSED {
			// fmt.Printf("paxos Dial() failed: %v\n", err1)
		}
		return false
	}
	defer c.Close()

	err = c.Call(name, args, reply)
	if err == nil {
		return true
	}
	// fmt.Println(err)
	return false
}

type PrepSendArgs struct {
	SequenceNum int    // sequence number sent with preparation
	ProposalNum string // proposal number sent with preparation
}

type PrepResponseArgs struct {
	Response          string      // response which is either ACCEPT or REJECT
	AcceptProposalNum string      // proposal number for ACCEPT case
	AcceptValue       interface{} // accepted interface for value
}

// send prepare function in given pseudocode
func (px *Paxos) sendPrepare(sendPrep PrepSendArgs, value interface{}) (bool, interface{}) {
	var proposolNumber string = "" // proposal number to be proposed and accepted (maybe)
	var agreedPeerCount int = 0    // counter to count number of peers that will say ACCEPT

	// we need to send prepare(n) message to all servers including me (as stated in psuedocode)
	for i, peer := range px.peers {
		responsePrep := PrepResponseArgs{AcceptValue: "", AcceptProposalNum: "", Response: "REJECT"}

		// if this peer is me
		if i == px.me {
			px.ReceivePrepare(&sendPrep, &responsePrep)
		} else { // if this is one of the other peers
			call(peer, "Paxos.ReceivePrepare", &sendPrep, &responsePrep)
		}

		// if upcoming response is OK, we need to assign accepted value
		// v' = v_a with highest proposal number n_a as stated in the psuedocode
		if responsePrep.Response == "ACCEPT" {
			agreedPeerCount++
			if responsePrep.AcceptProposalNum > proposolNumber {
				value = responsePrep.AcceptValue
				proposolNumber = responsePrep.AcceptProposalNum
			}
		}
	}
	return agreedPeerCount >= px.majorityCount, value
}

// receive prepare function in given pseudocode
func (px *Paxos) ReceivePrepare(send *PrepSendArgs, response *PrepResponseArgs) error {
	px.mu.Lock()
	defer px.mu.Unlock()

	_, exist := px.instances[send.SequenceNum]
	if !exist {
		px.instances[send.SequenceNum] = &instance{n_a: "", n_p: "", v_a: nil, instanceState: Pending}
	}

	// If coming propopsal number is < proposal number of that peer
	if send.ProposalNum < px.instances[send.SequenceNum].n_p {
		response.Response = "REJECT"
		return nil
	} else { // If coming propopsal number is >= proposal number of that peer
		px.instances[send.SequenceNum].n_p = send.ProposalNum           // update proposal number
		response.AcceptProposalNum = px.instances[send.SequenceNum].n_a // update value number
		response.AcceptValue = px.instances[send.SequenceNum].v_a       // update value instance
		response.Response = "ACCEPT"                                    // reply with ACCEPT
		return nil
	}
}

type AcceptArgs struct {
	SequenceNum int         // sequnce number for accept case
	ProposalNum string      // proposal number for accept case
	Value       interface{} // value with interface for accept case
}

// send accept function in given pseudocode
func (px *Paxos) sendAccept(prepSend PrepSendArgs, value interface{}) bool {
	controlArgs := AcceptArgs{SequenceNum: prepSend.SequenceNum,
		ProposalNum: prepSend.ProposalNum, Value: value}
	var acceptPeerCount int = 0

	for i, peer := range px.peers {
		var response interface{} = "REJECT"
		if i == px.me {
			px.ReceiveAccept(&controlArgs, &response)
		} else {
			call(peer, "Paxos.ReceiveAccept", &controlArgs, &response)
		}
		if response == "ACCEPT" {
			acceptPeerCount++
		}
	}
	return acceptPeerCount >= px.majorityCount
}

// recieve accept function in given pseudocode
func (px *Paxos) ReceiveAccept(send *AcceptArgs, response *interface{}) error {
	px.mu.Lock()
	defer px.mu.Unlock()

	_, check := px.instances[send.SequenceNum]
	if !check {
		px.instances[send.SequenceNum] = &instance{n_a: "", n_p: "", v_a: nil, instanceState: Pending}
	}

	if send.ProposalNum < px.instances[send.SequenceNum].n_p {
		*response = "REJECT"
		return nil
	} else { //if proposal number >= minimum proposal num
		*response = "ACCEPT"
		px.instances[send.SequenceNum].n_p = send.ProposalNum // update proposal number
		px.instances[send.SequenceNum].n_a = send.ProposalNum // update accept number
		px.instances[send.SequenceNum].v_a = send.Value       // update accept number with value
		return nil
	}
}

type DecideArgs struct {
	SequenceNumber int         // decided sequence number
	ProposalNumber string      // decided proposal number
	Me             int         // peer id
	Done           int         // state verification for decision
	Value          interface{} // decided value interface
}

// send decide as given in pseudocode
func (px *Paxos) sendDecide(prepSend PrepSendArgs, value interface{}) {
	var decisionArgs DecideArgs = DecideArgs{SequenceNumber: prepSend.SequenceNum,
		ProposalNumber: prepSend.ProposalNum, Value: value, Me: px.me, Done: px.maxSeqNums[px.me]}

	for i, peer := range px.peers {
		// if i'th peer is me
		if i == px.me {
			px.ReceiveDecide(&decisionArgs, nil)
		} else { // if i'th peer is some other peer except me
			call(peer, "Paxos.ReceiveDecide", &decisionArgs, nil)
		}
	}
}

// receive decide for send decide function which is given in pseudocode
func (px *Paxos) ReceiveDecide(sendArgs *DecideArgs, a *int) error {
	px.mu.Lock()
	defer px.mu.Unlock()

	_, check := px.instances[sendArgs.SequenceNumber]
	if !check {
		px.instances[sendArgs.SequenceNumber] = &instance{n_a: "", n_p: "", v_a: nil, instanceState: Pending}
	}

	px.instances[sendArgs.SequenceNumber].n_p = sendArgs.ProposalNumber
	px.instances[sendArgs.SequenceNumber].n_a = sendArgs.ProposalNumber
	px.instances[sendArgs.SequenceNumber].v_a = sendArgs.Value
	px.instances[sendArgs.SequenceNumber].instanceState = Decided
	px.maxSeqNums[sendArgs.Me] = sendArgs.Done

	return nil
}

// the application wants paxos to start agreement on instance seq, with proposed value v. Start()
// returns right away; the application will call Status() to find out if/when agreement is reached.
func (px *Paxos) Start(seq int, v interface{}) {
	go func() {
		if seq < px.Min() {
			return
		}
		for {
			var proposalNum string = strconv.FormatInt(time.Now().UTC().Unix(), 10) + "#" + strconv.Itoa(px.me) // unique proposal number
			var prepSend PrepSendArgs = PrepSendArgs{SequenceNum: seq, ProposalNum: proposalNum}
			sendPrepCheck, value := px.sendPrepare(prepSend, v)
			if sendPrepCheck {
				sendAcceptCheck := px.sendAccept(prepSend, value)
				if sendAcceptCheck {
					px.sendDecide(prepSend, value)
					break
				}
			}
			instanceState, _ := px.Status(seq)
			if instanceState == Decided {
				break
			}
		}
	}()
}

// the application on this machine is done with all instances <= seq.
func (px *Paxos) Done(seq int) {
	px.mu.Lock()
	if px.maxSeqNums[px.me] <= seq {
		px.maxSeqNums[px.me] = seq
	}
	px.mu.Unlock()
}

// the application wants to know the highest instance sequence known to this peer.
func (px *Paxos) Max() int {
	px.mu.Lock()
	defer px.mu.Unlock()

	var temp int = -1
	for sequence := range px.instances {
		if temp <= sequence {
			temp = sequence
		}
	}
	return temp
}

// Min() should return one more than the minimum among z_i, where z_i is the highest number
// ever passed to Done() on peer i. A peers z_i is -1 if it has never called Done().
// Paxos is required to have forgotten all information about any instances it knows that are < Min().
// The point is to free up memory in long-running Paxos-based servers.
// Paxos peers need to exchange their highest Done() arguments in order to implement Min(). These
// exchanges can be piggybacked on ordinary Paxos agreement protocol messages, so it is OK if one
// peers Min does not reflect another Peers Done() until after the next instance is agreed to.
//
// The fact that Min() is defined as a minimum over *all* Paxos peers means that Min() cannot
// increase until all peers have been heard from. So if a peer is dead  or unreachable,
// other peers Min()s will not increase even if all reachable peers call Done. The reason for
// this is that when the unreachable peer comes back to  life, it will need to catch up on instances
// that it missed -- the other peers therefor cannot forget these instances.
func (px *Paxos) Min() int {
	px.mu.Lock()
	defer px.mu.Unlock()

	var temp int = px.maxSeqNums[px.me]
	for _, sequence := range px.maxSeqNums {
		if temp > sequence {
			temp = sequence
		}
	}
	for sequence, inst := range px.instances {
		if (inst.instanceState == Decided) && (temp > sequence) {
			delete(px.instances, sequence)
		}
	}
	return temp + 1
}

// the application wants to know whether this peer thinks an instance has been decided,
// and if so what the agreed value is. Status() should just inspect the local peer state;
// it should not contact other Paxos peers.
func (px *Paxos) Status(seq int) (Fate, interface{}) {
	var min int = px.Min()
	px.mu.Lock()
	defer px.mu.Unlock()

	if seq < min {
		return Forgotten, nil
	}

	instance, ok := px.instances[seq]
	if ok {
		return instance.instanceState, instance.v_a
	}
	return Pending, nil
}

func (px *Paxos) Kill() {
	atomic.StoreInt32(&px.dead, 1)
	if px.l != nil {
		px.l.Close()
	}
}

func (px *Paxos) isdead() bool {
	return atomic.LoadInt32(&px.dead) != 0
}

func (px *Paxos) setunreliable(what bool) {
	if what {
		atomic.StoreInt32(&px.unreliable, 1)
	} else {
		atomic.StoreInt32(&px.unreliable, 0)
	}
}

func (px *Paxos) isunreliable() bool {
	return atomic.LoadInt32(&px.unreliable) != 0
}

func Make(peers []string, me int, rpcs *rpc.Server) *Paxos {
	px := &Paxos{}
	px.peers = peers
	px.me = me

	px.instances = make(map[int]*instance)
	px.majorityCount = len(peers)/2 + 1
	px.maxSeqNums = make([]int, len(peers))
	for i := range px.peers {
		px.maxSeqNums[i] = -1
	}

	if rpcs != nil {
		// caller will create socket &c
		rpcs.Register(px)
	} else {
		rpcs = rpc.NewServer()
		rpcs.Register(px)

		// prepare to receive connections from clients.
		// change "unix" to "tcp" to use over a network.
		os.Remove(peers[me]) // only needed for "unix"
		l, e := net.Listen("unix", peers[me])
		if e != nil {
			log.Fatal("listen error: ", e)
		}
		px.l = l

		// please do not change any of the following code,
		// or do anything to subvert it.

		// create a thread to accept RPC connections
		go func() {
			for px.isdead() == false {
				conn, err := px.l.Accept()
				if err == nil && px.isdead() == false {
					if px.isunreliable() && (rand.Int63()%1000) < 100 {
						// discard the request.
						conn.Close()
					} else if px.isunreliable() && (rand.Int63()%1000) < 200 {
						// process the request but force discard of reply.
						c1 := conn.(*net.UnixConn)
						f, _ := c1.File()
						err := syscall.Shutdown(int(f.Fd()), syscall.SHUT_WR)
						if err != nil {
							// fmt.Printf("shutdown: %v\n", err)
						}
						atomic.AddInt32(&px.rpcCount, 1)
						go rpcs.ServeConn(conn)
					} else {
						atomic.AddInt32(&px.rpcCount, 1)
						go rpcs.ServeConn(conn)
					}
				} else if err == nil {
					conn.Close()
				}
				if err != nil && px.isdead() == false {
					// fmt.Printf("Paxos(%v) accept: %v\n", me, err.Error())
				}
			}
		}()
	}
	return px
}
