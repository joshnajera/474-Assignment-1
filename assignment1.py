import  copy
import _operator


class MyGen:
    '''Processes input file of logical clock values and generates events that correspond'''
    def __init__(self):
        self.process_positions = []      # Holds processes involved with each Logical Time
        self.processes = []              # Holds input data stored as list
        self.result = []                 # Holds results
        self.num_processes = 0           # Holds number of processes
        self.send_receive_count = 0
        self.max_clock_value = 0         # Holds the maximum Logical Clock Time Stamp value

        with open("input.txt") as in_file:

           # Read input, populate 'processes', get the process count, size 'result' accordingly
            for line in in_file:
                self.processes.append([int(i) for i in line.strip().split(' ')])
                self.num_processes += 1
                self.result.append([])
                self.process_positions.append(0)    # Appending zeros to pad

            for process in self.processes:       # Goes through 'process'...
                self.max_clock_value = max(max(iter(process)), self.max_clock_value)

            # Initializing 'event_times' size based off 'max_clock_value' logical clock value
            self.event_times = [set() for i in range(self.max_clock_value)]

            # Populate 'event_times' with data from 'processes'
            for process in enumerate(self.processes):
                for event in process[1]:
                    if event != 0:
                        self.event_times[event - 1].add(process[0])

        # for event in self.event_times:
        #     print(event)

        self.generate_possibilities(self.result)     # Calls function to evaluate input


    def generate_possibilities(self, working_result, s_flag=0, pos=0):
        '''Uses 'self.event_times' to determine the events that occurred at each logical time'''
        event = self.event_times[pos]   # Getting current list of processes
        output = copy.deepcopy(working_result)  # Making a copy of working_result...

        # print("\nIteration: {}".format(pos+1))
        # If Send s_flag is not set and this isn't the last item
        if s_flag == 0 and pos < len(self.event_times) -1:    

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
                    self.generate_possibilities(output, s_flag+1, pos+1)   # Make next recursive call
                # s_flag += 1
                
            else:   # if the set difference Next-Current == Empty: Then there isn't a send event and all are internal
                print("No send event this time")
                print("Make all choices internal then?")
                for item in event:                          # Setting all to internal
                    print("Make '{}' internal...".format(item))
                    output[item].append('i')
                # print(output)
                self.generate_possibilities(output, s_flag, pos+1)
                
        else:   # Else s_flag is raised   TODO Handle when we have receive AND send at same time
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
                        self.generate_possibilities(output, s_flag, pos+1)
                    
                    else:
                        for item_j in event - possible_receives:
                            print("Make '{}' internal...".format(item_j))
                            output[item_j].append('i')  # Set the rest to internal
                        self.generate_possibilities(output, s_flag-1, pos+1)
                
                # print(output)
                # s_flag -= 1
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
    
        
asdf = MyGen()
