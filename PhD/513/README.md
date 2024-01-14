## Collaborators 

1. Burak Topcu

2. Omer Faruk Ozdemir

## Project Overview
In this assignment, you'll implement a fault-tolerant key-value store on 
top of Paxos. You need to fill in the necessary parts in `src/kvpaxos/client.go`, 
`src/kvpaxos/server.go`, and `src/kvpaxos/common.go`. Similarly, the 
communication between servers and clients is based on rpc, which is also 
provided in the template (`call()`).

The key-value store includes three kinds of operations: Put, Get, and Append.
Append performs the same as Put when the key is not in the store.
Otherwise, it appends new value to the existing value. For example,

1. Put('k', 'a')  // so put here replaces an entry with a specific key 
2. Append('k', 'bc')   // while append adds a new item which is not existing
3. Get(k) -> 'abc'

Clients send Put(), Append(), and Get() RPCs to kvpaxos servers. A client can
send an RPC to any of the kvpaxos servers, and should retry by sending to a
different server if there's a failure. Each kvpaxos server contains a replica of
the key/value database; handlers for client Get() and Put()/Append() RPCs; and a
Paxos peer. Paxos takes the form of a library that is included in each kvpaxos
server. A kvpaxos server talks to its local Paxos peer (**via method calls**).
All kvpaxos replicas should stay identical; the only exception is that some
replicas may lag others if they are not reachable. If a replica isn't reachable
for a while, but then starts being reachable, it should eventually catch up (
learn about operations that it missed).

## Test
To test your codes, try `go test -v` under the kvpaxos folder. You may see some 
error messages during the test, but as long as it shows "Passed" in the end 
of the test case, it passes the test case.

## Hints
Here's a plan for reference:

1. Fill in the Op struct in server.go with the "value" information that kvpaxos
   will use Paxos to agree on, for each client request. Op field names must
   start with capital letters. You should use Op structs as the agreed-on values
   -- for example, you should pass Op structs to Paxos Start(). Go's RPC can
   marshall/unmarshall Op structs; the call to gob.Register() in StartServer()
   teaches it how.
2. Implement the PutAppend() handler in server.go. It should enter a Put or
   Append Op in the Paxos log (i.e., use Paxos to allocate a Paxos instance,
   whose value includes the key and value (so that other kvpaxoses know about
   the Put() or Append())). An Append Paxos log entry should contain the
   Append's arguments, but not the resulting value, since the result might be
   large.
3. Implement a Get() handler. It should enter a Get Op in the Paxos log, and
   then "interpret" the the log before that point to make sure its key/value
   database reflects all recent Put()s.
4. Add code to cope with duplicate client requests, including situations where
   the client sends a request to one kvpaxos replica, times out waiting for a
   reply, and re-sends the request to a different replica. The client request
   should execute just once. Please make sure that your scheme for duplicate
   detection frees server memory quickly, for example by having the client tell
   the servers which RPCs it has heard a reply for. It's OK to piggyback this
   information on the next client request.

Hint: your server should try to assign the next available Paxos instance (
sequence number) to each incoming client RPC. However, some other kvpaxos
replica may also be trying to use that instance for a different client's
operation. So the kvpaxos server has to be prepared to try different instances.

Hint: your kvpaxos servers should not directly communicate; they should only
interact with each other through the Paxos log.

Hint: as in Lab 2, you will need to uniquely identify client operations to
ensure that they execute just once. Also as in Lab 2, you can assume that each
clerk has only one outstanding Put, Get, or Append.

Hint: a kvpaxos server should not complete a Get() RPC if it is not part of a
majority (so that it does not serve stale data). This means that each Get() (as
well as each Put() and Append()) must involve Paxos agreement.

Hint: don't forget to call the Paxos Done() method when a kvpaxos has processed
an instance and will no longer need it or any previous instance.

Hint: your code will need to wait for Paxos instances to complete agreement. The
only way to do this is to periodically call Status(), sleeping between calls.
How long to sleep? A good plan is to check quickly at first, and then more
slowly:
```
to := 10 * time.Millisecond
for {
status, _ := kv.px.Status(seq)
if status == paxos.Decided{
...
return
}
time.Sleep(to)
if to < 10 * time.Second {
to *= 2
}
}
```
Hint: if one of your kvpaxos servers falls behind (i.e. did not participate in
the agreement for some instance), it will later need to find out what (if
anything) was agree to. A reasonable way to to this is to call Start(), which
will either discover the previously agreed-to value, or cause agreement to
happen. Think about what value would be reasonable to pass to Start() in this
situation.

Hint: When the test fails, check for gob error (e.g. "rpc: writing response:
gob: type not registered for interface ...") in the log because go doesn't
consider the error fatal, although it is fatal for the lab.

