import _operator
import  copy

    
class myGen:
    process_positions = []      # Holds processes involved with each Logical Clock Time Stamp
    processes = []              # Holds input data stored as list
    result = []                 # Holds results
    num_processes = 0           # Holds number of processes
    max = 0                     # Holds the maximum Logical Clock Time Stamp value
    send_receive_count = 0
    
    def __init__(self):
        with open("input.txt") as in_file:
            for line in in_file:
                self.processes.append([int(i) for i in line.strip().split(' ')])    # Load each row in the file into 'processes'
                self.num_processes += 1
                self.result.append([])  # Setting up result to have as many rows as processes
            
            for i, process in zip(range(self.num_processes), self.processes):       # Goes through 'process'...
                self.process_positions.append(0)    # Appending zeros to pad
                
                for j in range(len(process)):
                    if process[j] > self.max:       # Finding 'max' logical clock value
                        self.max = process[j]
            
            self.event_times = [set() for i in range(self.max)]     # Initializing 'event_times' size based off 'max' logical clock value
            for process in range(self.num_processes):               # Populating with data from 'processes'
                for event in self.processes[process]:
                    if event == 0:
                        continue
                    self.event_times[event - 1].add(process)
                    
        for event in self.event_times:
            print(event)
        
        self.generatePossibilities(self.result)     # Calls function to evaluate input
                    
    def generatePossibilities(self, result, flag = 0, pos = 0):
        event = self.event_times[pos]   # Getting current list of processes involved with events at current logical clock time value
        output = copy.deepcopy(result)  # Making a copy of output ... (Copies made so we don't affect original if we want to recursively find all possible solutions)
        
        print("\nIteration: {}".format(pos+1))
        if flag == 0 and pos < len(self.event_times) -1:    # If Send flag is not set and this isn't the last item
                                                            # This indicates that this wont be a receive
            print("{Next} - {Current}= ", self.event_times[pos+1] - event)
            if self.event_times[pos+1] - event != set():    # If set difference Next-Current != Empty Set: Then there is a send event
                print("Set at least one send, set others internal")
                self.send_receive_count += 1
                for item_i in event:                        # Go through all processes involved in current event
                    print("Making '{}' as send...".format(item_i))
                    output[item_i].append('s{}'.format(self.send_receive_count))  # Pick one as send
                    for item_j in event:                    # Make the others internal
                        if item_i != item_j:
                            print("Make '{}' internal...".format(item_j))
                            output[item_j].append('i')
                    # print(output)
                    self.generatePossibilities(output, flag+1, pos+1)   # Make next recursive call
                # flag += 1
                
            else:   # if the set difference Next-Current == Empty: Then there isn't a send event and all are internal
                print("No send event this time")
                print("Make all choices internal then?")
                for item in event:                          # Setting all to internal
                    print("Make '{}' internal...".format(item))
                    output[item].append('i')
                # print(output)
                self.generatePossibilities(output, flag, pos+1)
                
        else:   # Else flag is raised   TODO Handle when we have receive AND send at same time
            possible_receives = event - self.event_times[pos-1]
            if possible_receives:                           # If set difference Current-next: then we have a receive
                print("Set a receive event, others internal?")       # TODO: what if more than one send was made?
                for item_i in possible_receives:
                    print("Make '{}' receive...".format(item_i))
                    output[item_i].append('r{}'.format(self.send_receive_count))  # Set one to a receive
                    
                    # Now we have to check if any of the remainders are send events
                    
                    if self.event_times[pos+1] - event != set():
                        print("We also have a send event!")
                        print("{Next} - {Current}= ", self.event_times[pos+1] - event)
                        
                        self.send_receive_count += 1
                        for item_j in event:
                            if item_j != item_i:
                                output[item_j].append('s{}'.format(self.send_receive_count))  # Pick one as send
                                for item_k in event:                    # Make the others internal
                                    if item_j != item_k:
                                        print("Make '{}' internal...".format(item_k))
                                        output[item_k].append('i')
                        self.generatePossibilities(output, flag, pos+1)
                    
                    else:
                        for item_j in event - possible_receives:
                            print("Make '{}' internal...".format(item_j))
                            output[item_j].append('i')  # Set the rest to internal
                        self.generatePossibilities(output, flag-1, pos+1)
                
                # print(output)
                # flag -= 1
            else:
                print("Last element? No receives left? Must be internal")
                for item in event:  # Catches the case where this is the last element?
                    output[item].append('i')
                for row in output:
                    for process in row:
                        print(process, end='\t')
                    print('')
                    
                # This is a cheatsy way to end for the time being because I didn't implement recursion fully (yet?)
                exit()
    # print(i, event)
    
        
asdf = myGen()
