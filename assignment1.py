'''Handles the evaluation of LC Values as input and generates a matrix of
    processes and events that match those values'''
import copy
import sys
import os
import itertools

class LogicValueAnalysis:
    '''Processes input file of logical clock values and generates events that correspond'''
    def __init__(self, file_name):
        self.processes = []             # Holds input data stored as list
        self.result = []                # Holds results
        self.send_receive_count = 0     # Holds the send-receive pair count
        self.max_clock_value = 0        # Holds the maximum Logical Clock Time Stamp value

        with open(file_name) as in_file:
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
            sys.stdout.write("\nValid input, processing...\n")
            self.generate_possibilities(self.result)     # Calls function to evaluate input
        else:
            sys.stdout.write("INCORRECT")

    def validate(self):
        '''Validates input by iterating through 'processes_at_time'
            and evaluating'''
        no_error = True

        for processes in enumerate(self.processes_at_time[:-1]):
            next_set = self.processes_at_time[processes[0]+1]
            diff = next_set.difference(processes[1])

            # Empty set => Missing step
            if processes[1] == set():
                sys.stdout.write("ERROR:".ljust(12)+"missing a clock step.")
                no_error = False

            # Number of receives in next clock step > number of possible matching senders
            elif len(diff) > len(processes[1]):
                sys.stdout.write("ERROR:".ljust(12)+"Not enough sends")
                no_error = False
        return no_error


    def generate_possibilities(self, working_result, s_flag=0, pos=0):
        '''Uses 'self.processes_at_time' to determine the events
            that occurred at each logical time'''
        processes_at_current_time = self.processes_at_time[pos]
        output = copy.deepcopy(working_result)  # Make a copy of working_result...
        all_receives = set()

        # If send flag is raised, we need to handle receives
        if s_flag == 1:
            possible_receives = processes_at_current_time - self.processes_at_time[pos-1]
            self.send_receive_count -= len(possible_receives)
            # Marking each as a receive
            for rcv_process in possible_receives:
                s_flag = 0
                self.send_receive_count += 1
                all_receives.add(rcv_process)
                output[rcv_process].append('r{}'.format(self.send_receive_count))

        # After any receives have been processed, process remaining info
        try:
            possible_receives = self.processes_at_time[pos+1] - processes_at_current_time
            possible_sends = \
                    processes_at_current_time.difference(possible_receives).difference(all_receives)
            # Generate possible combinations of send processes based on num of following receies
            #   and currently involved processes
            send_combinations = itertools.combinations(possible_sends, len(possible_receives))

            # For each combination of possible send events
            for combo in send_combinations:
                all_sends = set()
                # First set the send events for each process in the combo
                for s_process in enumerate(combo):
                    s_flag = 1
                    self.send_receive_count += 1
                    output[s_process[1]].append('s{}'.format(self.send_receive_count))
                    all_sends.add(s_process[1])
                # Make remaining processes internal events
                for remaining_process in \
                        processes_at_current_time.difference(all_sends).difference(all_receives):
                    output[remaining_process].append('i')
                self.generate_possibilities(output, s_flag, pos+1)

        # In the case of IndexError, we have hit the last clock time.
        #   Process remaining input then
        except IndexError:
            remaineders = processes_at_current_time - all_receives
            for remaining_process in remaineders:
                output[remaining_process].append('i')
            # Displaying output
            for process in output:
                for event in process:
                    sys.stdout.write(str(event).ljust(4))
                    # print(str(event).ljust(4), end="")
                sys.stdout.write("\n")
            self.result = output
            os._exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        lva = LogicValueAnalysis(sys.argv[1])