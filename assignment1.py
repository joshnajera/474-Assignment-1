'''Handles the evaluation of LC Values as input and generates a matrix of
    processes and events that match those values'''
import  copy
import itertools

class MyGen:
    '''Processes input file of logical clock values and generates events that correspond'''
    def __init__(self):
        self.processes = []             # Holds input data stored as list
        self.result = []                # Holds results
        self.send_receive_count = 0     # Holds the send-receive pair count
        self.max_clock_value = 0        # Holds the maximum Logical Clock Time Stamp value

        with open("input.txt") as in_file:
           # Read input, populate 'processes', get the process count, size 'result' accordingly
            for line in in_file:
                self.processes.append([int(i) for i in line.strip().split(' ')])
                self.result.append([])

            # Calculate 'max_clock_value'
            for process in self.processes:
                self.max_clock_value = max(max(iter(process)), self.max_clock_value)

            # Initializing 'processes_at_time' size based off 'max_clock_value'
            self.processes_at_time = [set() for i in range(self.max_clock_value)]

            # Populate 'processes_at_time' with data from 'processes'
            for process in enumerate(self.processes):
                for event in set(process[1]).difference({0}):
                    self.processes_at_time[event - 1].add(process[0])

        # for event in self.processes_at_time:
        #     print(event)
        if self.validate():
            print("\nInput valid, processing...")
            self.generate_possibilities(self.result)     # Calls function to evaluate input

    def validate(self):
        '''Validates input by iterating through 'processes_at_time'
            and evaluating'''
        no_error = True

        for processes in enumerate(self.processes_at_time[:-1]):
            next_set = self.processes_at_time[processes[0]+1]
            diff = next_set.difference(processes[1])

            # Empty set => Missing step
            if processes[1] == set():
                print("ERROR:".ljust(12)+"missing a clock step.")
                no_error = False

            # Number of receives in next clock step > number of possible matching senders
            elif len(diff) > len(processes[1]):
                print("ERROR:".ljust(12)+"Not enough sends")
                no_error = False

            # Valid step
            else:
                print("Step {}:".format(processes[0] + 1).ljust(12)+"Valid")
        print("Step {}:".format(len(self.processes_at_time)).ljust(12)+"Last item, Valid by default")
        return no_error


    def generate_possibilities(self, working_result, s_flag=0, pos=0):
        '''Uses 'self.processes_at_time' to determine the events
            that occurred at each logical time'''
        processes_at_current_time = self.processes_at_time[pos]
        output = copy.deepcopy(working_result)  # Make a copy of working_result...

        # If Send s_flag is NOT set and this isn't the last item
        if s_flag == 0 and pos < len(self.processes_at_time):
            # If set difference Next-Current != Empty Set: Then there is a send event

            ##### TESTING - START ####  TODO: Handle multiple send/receive events
            possible_receives = self.processes_at_time[pos+1] - processes_at_current_time
            possible_sends = processes_at_current_time - possible_receives
            # Generate possible combinations of send processes based on num of following receies
            #   and currently involved processes
            send_combinations = itertools.combinations(possible_sends, len(possible_receives))

            # For each combination
            for combo in send_combinations:
                all_sends = set()
                # First set the send events for each process in the combo
                for s_process in enumerate(combo):
                    s_flag = 1
                    self.send_receive_count += 1
                    output[s_process[1]].append('s{}'.format(self.send_receive_count))
                    all_sends.add(s_process[1])
                # Make remaining processes internal events
                for remaining_process in processes_at_current_time.difference(all_sends):
                    output[remaining_process].append('i')
                self.generate_possibilities(output, s_flag, pos+1)
            ##### TESTING - END  ####

            ##### Legacy    ####
            # if self.processes_at_time[pos+1] - processes_at_current_time != set():
            #     self.send_receive_count += 1

            #     for process in processes_at_current_time:
            #         # Pick one as send
            #         output[process].append('s{}'.format(self.send_receive_count))
            #         # Make the others internal
            #         for remaining_process in processes_at_current_time - {process}:
            #             output[remaining_process].append('i')

            #         # Make next recursive call
            #         self.generate_possibilities(output, s_flag+1, pos+1)
            # else:
            #     # Set all to internal
            #     for process in processes_at_current_time:
            #         output[process].append('i')
            #     self.generate_possibilities(output, s_flag, pos+1)

        # Else receive event
        else:
            ##### TESTING - START ####  TODO: Handle multiple send/receive events

            possible_receives = processes_at_current_time - self.processes_at_time[pos-1]
            self.send_receive_count -= len(possible_receives)
            all_receives = set()
            for rcv_process in possible_receives:
                s_flag = 0
                self.send_receive_count += 1
                all_receives.add(rcv_process)
                output[rcv_process].append('r{}'.format(self.send_receive_count))

            possible_receives = self.processes_at_time[pos+1] - processes_at_current_time
            possible_sends = processes_at_current_time.difference(possible_receives).difference(all_receives)
            # Generate possible combinations of send processes based on num of following receies
            #   and currently involved processes
            send_combinations = itertools.combinations(possible_sends, len(possible_receives))

            # For each combination
            for combo in send_combinations:
                all_sends = set()
                # First set the send events for each process in the combo
                for s_process in enumerate(combo):
                    s_flag += 1
                    self.send_receive_count += 1
                    output[s_process[1]].append('s{}'.format(self.send_receive_count))
                    all_sends.add(s_process[1])
                # Make remaining processes internal events
                for remaining_process in processes_at_current_time.difference(all_sends).difference(all_receives):
                    output[remaining_process].append('i')
                self.generate_possibilities(output, s_flag, pos+1)
            ##### TESTING - END   ####

            # Evaluate which current processes might be a receive event
            # possible_receives = processes_at_current_time - self.processes_at_time[pos-1]
            # if possible_receives:
            #     for receive_process in possible_receives:
            #         # Set one to a receive
            #         output[receive_process].append('r{}'.format(self.send_receive_count))

            #         # Now we have to check if any of the remaining are send events
            #         if self.processes_at_time[pos+1] - processes_at_current_time != set():
            #             self.send_receive_count += 1

            #             # Pick one as send
            #             for s_process in processes_at_current_time - {receive_process}:
            #                 output[s_process].append('s{}'.format(self.send_receive_count))

            #                 # Make the others internal
            #                 for internal_process in processes_at_current_time \
            #                 - {receive_process, s_process}:
            #                     output[internal_process].append('i')
            #             self.generate_possibilities(output, s_flag, pos+1)

            #         # No send events, make rest internal
            #         else:
            #             for internal_process in processes_at_current_time - possible_receives:
            #                 output[internal_process].append('i')
            #             self.generate_possibilities(output, s_flag-1, pos+1)

            # Catches the case where this is the last element?
            # else:
            #     for process in processes_at_current_time:
            #         output[process].append('i')

            #     # Print results
            #     for row in output:
            #         for process in row:
            #             print(process, end='\t')
            #         print('')

            #     # This is a cheatsy way to end because I didn't implement recursion fully (yet?)
            exit()

ASDF = MyGen()
