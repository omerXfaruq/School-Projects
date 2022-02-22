import simpy
import random
import numpy as np

#---------------------Constants-------------------- 
RANDOM_SEED = 978
random.seed(RANDOM_SEED)
INTERARRIVAL_RATE = 1/14.3
RENEGE_RATE=1/60.0
EXPERT_RATE=1/10.2
BREAK_RATE=1/60.0
#---------------------------------------------------

#-------------------Statistic and variable definitions------------
service_times = [] #Duration of the conversation between the customer and the front operator (Service time)
service_times2 = [] #Duration of the conversation between the customer and the expert operator (Service time)
queue2_waiting_times=[] # Waiting time of customers in the second queue (expert), used to calculate a statistic
total_waiting_time_to_total_system_time_ratios= [] # All customers' total waiting time to total system time ratios 
total_waiting_times = [] # Total waiting time is a customer's waiting time in 1st queue + waiting time in 2nd queue. 
break_decision = False # Becomes true when expert operator decides to take a break
customers_to_finish_to_break = [] # This is a list of customer numbers that are needed to be served 
#in order expert operator to be able take a break
# -------------------------------------------------------------------------

class Customer(object):
    
    def __init__(self, name, env, opr):
        self.env = env
        self.name = name
        self.arrival_t = self.env.now
        self.action = env.process(self.call())
    
    def call(self):
        print('%s initiated a call at %g' % (self.name, self.env.now))
        total_waiting_time = 0 # Total waiting time means waiting time in first queue + second queue
        total_system_time = 0 #Total time a customer spends in the system 
        with operator.request() as req:
            yield req
            print('%s is assigned to the front operator at %g' % (self.name, self.env.now))
            total_waiting_time += self.env.now - self.arrival_t
            yield self.env.process(self.ask_question()) # Wait to be served
            print('%s is done with the front operator at %g' % (self.name, self.env.now))
        expert_arrival = self.env.now
        with operator2.request() as req:
            renege_duration = random.expovariate(RENEGE_RATE) 
            results = yield req | env.timeout(renege_duration) # Wait to be served or running out of patience, which is first 
            global total_time            
            if req in results: # If served
                print('%s is assigned to the expert operator at %g' % (self.name, self.env.now))
                total_waiting_time += self.env.now - expert_arrival
                queue2_waiting_times.append(self.env.now - expert_arrival)
                yield self.env.process(self.ask_question2())
                print('%s is done with the expert operator at %g' % (self.name, self.env.now))
                total_system_time = self.env.now - self.arrival_t
                total_waiting_times.append(total_waiting_time)
                total_waiting_time_to_total_system_time_ratios.append(total_waiting_time/total_system_time)
                if self.name == "Cust " + str(CUSTOMER_NUMBER): # Last customer's departure is total time because of FCFS principle
                    total_time = self.env.now
            else: # If reneged
                print("---------------Customer "+str(self.name)+" reneged after "+ str(self.env.now - expert_arrival) + " of waiting.")
                total_system_time = self.env.now - self.arrival_t
                total_waiting_time += self.env.now - expert_arrival                
                total_waiting_time_to_total_system_time_ratios.append(total_waiting_time/total_system_time)
                total_waiting_times.append(total_waiting_time)                
                if self.name == "Cust " + str(CUSTOMER_NUMBER): 
                    total_time = self.env.now                
            
    def ask_question(self):
        m1=7.2                             
        v1=2.7 # Lognormal dist of service time 1, set up
        mu1=np.log((m1**2/((v1**2+m1**2)**0.5)))
        variance1=np.log((v1**2+m1**2)/m1**2)
        duration = random.lognormvariate(mu1,variance1**0.5)
        yield self.env.timeout(duration)
        service_times.append(duration)
        
    def ask_question2(self):
        duration = random.expovariate(EXPERT_RATE) 
        yield self.env.timeout(duration)
        service_times2.append(duration)
    
def customer_generator(env, operator):
    for i in range(CUSTOMER_NUMBER):
        duration = random.expovariate(INTERARRIVAL_RATE)
        yield env.timeout(duration)
        Customer('Cust %s' %(i+1), env, operator)  
    global last_came # This variable is used to stop operator 2 from taking breaks
    last_came = True  

def give_break():
    while(True):
        global break_decision
        if(break_decision and not any(check in customers_to_finish_to_break for check in operator2.queue)):
		# any(..) expression checks for any common elements in two lists and return true if there is.
		# Overall if = if decision is taken and all the customers that are there when the decision is taken are done
            with operator2.request() as req:
                yield req
                print("---------------Expert operator takes a break at " + str(env.now))
                yield env.timeout(3)
                print("---------------Expert operator comes again at " + str(env.now))
                break_decision = False  
        if (last_came and (len(operator.queue) + operator.count + len(operator2.queue) + operator2.count == 0)): 
		# If last customer came and no one in the queue and no one is being served by operator2 
            break
        duration = random.expovariate(1/60.0)
        yield env.timeout(duration)
        if not break_decision: # If decision is not taken already take it
            global customers_to_finish_to_break
            break_decision = True
            customers_to_finish_to_break = operator2.queue #When decision taken record people in the queue 

            
""" ------------------Simulation Running Area------------------  """
last_came = False
CUSTOMER_NUMBER = 1000  
env = simpy.Environment()
operator = simpy.Resource(env, capacity = 1) # front
operator2= simpy.Resource(env, capacity = 1) # expert 
env.process(customer_generator(env, operator)) 
break_process = env.process(give_break()) # Expert's taking break process

# ----------------Initilization of statistic counters--------------- 
busy_time_expert=0
busy_time_front=0
total_time=0
total_waiting_time=0
total_wait_in_queue2=0
#-------------------------------------------------------------------
#---------------------Run simulation and calculate statistics--------------
print("--------------- CUSTOMER NUMBER 1000 ------------------")
env.run()

for i in service_times:
    busy_time_front += i
for i in service_times2:
    busy_time_expert += i
for i in total_waiting_times:
    total_waiting_time += i 
for i in queue2_waiting_times:
    total_wait_in_queue2 += i

print("Utilization of operator 1 is:" + str(busy_time_front/total_time))
print("Utilization of operator 2 is:" + str(busy_time_expert/total_time))
print("Average total waiting time is:" + str(total_waiting_time/CUSTOMER_NUMBER))
print("Maximum total waiting time to total system time ratio " + str(max(total_waiting_time_to_total_system_time_ratios)))
print("Average number of people waiting to be served by the expert operator " + str(total_wait_in_queue2/total_time))        
#------------------------------------------------------------------------

#---------------------Prepare the environment to run the simulation again with 5000 customers ----------------
CUSTOMER_NUMBER=5000
last_came = False   
break_decision = False   
print("--------------- CUSTOMER NUMBER 5000 ------------------")
env = simpy.Environment()
operator = simpy.Resource(env, capacity = 1)
operator2= simpy.Resource(env, capacity = 1)
env.process(customer_generator(env, operator))
break_process = env.process(give_break())

#------------------Initialization of statistic counters------------------
busy_time_expert = 0
busy_time_front = 0
total_waiting_time = 0
total_waiting_times = []
total_wait_in_queue2 = 0
total_waiting_time_to_total_system_time_ratios = []
total_time = 0
service_times = []
service_times2 = []
#------------------------------------------------------------------------

#---------------Run and collect statistics ------------------------------

env.run()
for i in service_times:
    busy_time_front += i
for i in service_times2:
    busy_time_expert += i
for i in total_waiting_times:
    total_waiting_time += i 
for i in queue2_waiting_times:
    total_wait_in_queue2 += i

print("Utilization of operator 1 is:" + str(busy_time_front/total_time))
print("Utilization of operator 2 is:" + str(busy_time_expert/total_time))
print("Average total waiting time is:" + str(total_waiting_time/CUSTOMER_NUMBER))
print("Maximum total waiting time to total system time ratio " + str(max(total_waiting_time_to_total_system_time_ratios)))
print("Average number of people waiting to be served by the expert operator " + str(total_wait_in_queue2/total_time)) 


"""-----------------------End of simulation running area----------------------"""
