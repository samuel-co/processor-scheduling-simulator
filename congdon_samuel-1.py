''' Samuel Congdon
    CSCI460 OS - Assignment 1
    2 October 2017

    example execution: python3 congdon_samuel-1.py
    output file: congdon_samuel-1.output

    This python module simulates testing a multi-core non-preemptive process scheduler. The cores are created
    in class Processor. Each Processor instance tracks the amount of time it requires to complete its jobs. The
    main function initializes testing. Tests are run on both the Circular and Custom Procedures using the same
    randomly generated job sets. The overall turnaround time is recorded for each test and used to display overall
    statistics for the tests. Additionally, a provided job set is run using both procedures, reporting the overall
    turnaround time using each procedure. These statistics are output to congdon_samuel-1.output.

    The custom_test() is a job allocation procedure which assigns the next job to the processor with the current
    lowest completion_time. This mirrors what would happen if each job was assigned to the next available processor,
    still based on the order of the job arrival (the first job to arrive is always assigned next). This allows for
    a more efficient allocation of jobs, and as a result a processor isn't left idling whilst another processor has
    a queue of jobs waiting to begin processing.  This procedure beats the CIRCULAR procedure using the provided
    job set, and will always have a overall turnaround time less than or equal to that of the CIRCULAR procedure on
    randomly generated job sets.
'''

import random
import sys
from statistics import mean, stdev

class Processor:
    '''Creates individual processors representing cores, each processor tracks its overall job time. '''

    def __init__(self):
        self.completion_time = 0

    def add_job(self, job_time):
        ''' Adds a jobs time to the completion_time. 1 is added to represent load time for the job. '''
        self.completion_time += job_time + 1

    def check_waiting(self, current_time):
        ''' Determines if a processor is waiting for a job, if so the processors completion_time is updated. '''
        if current_time > self.completion_time:
            self.completion_time = current_time


def create_random_jobs(number_of_jobs):
    ''' Creates and returns  a dictionary of jobs. Key is job number, value is a tuple containing the arrival time
        and processing time. Arrival time is every ms starting at 0, processing time is random from 1 to 500. '''
    jobs = {}
    for i in range(number_of_jobs):
        jobs.update({i+1:(i, random.randint(1, 500))})
    return jobs

def create_set_jobs():
    ''' Returns a dictionary containing the supplied job set. Key is job number, value is a tuple containing the
        arrival time and processing time.'''
    return {1:(4,9), 2:(15,2), 3:(18,16), 4:(20,3), 5:(26,29), 6:(29,198), 7:(35,7), 8:(45,170), 9:(57,180),
            10:(83,178), 11:(88,73), 12:(95,8)}

def create_processors(number_of_processors):
    ''' Creates and returns a list of new processors. '''
    processors = []
    for i in range(number_of_processors):
        processors.append(Processor())
    return processors

def overall_turnaround(processors):
    ''' Determines and returns the largest time a processor in the list of supplied processors has
        to completion, representing the overall turnaround time. '''
    overall_turnaround_time = 0
    for processor in processors:
        if processor.completion_time > overall_turnaround_time:
            overall_turnaround_time = processor.completion_time

    return overall_turnaround_time

def circular_test(jobs, processors):
    ''' Allocates jobs to processors in a round-robin fashion. j tracks the last processor to be given a job. '''
    j = -1

    for job in jobs:
        current_time = jobs[job][0]
        for processor in processors:
            processor.check_waiting(current_time)
        processors[(j+1)%len(processors)].add_job(jobs[job][1])
        j += 1

    return overall_turnaround(processors) - jobs[1][0]  # subtracts the first job's arrival time from the completion time

def custom_test(jobs, processors):
    ''' Allocates jobs to processors based on which processor has the lowest current completion_time,
        simulating the allocation of jobs onto the first processor to complete its current task. '''
    for job in jobs:
        current_time = jobs[job][0]
        lowest_time = processors[0]
        for processor in processors:
            processor.check_waiting(current_time)
            if processor.completion_time < lowest_time.completion_time: lowest_time = processor
        lowest_time.add_job(jobs[job][1])

    return overall_turnaround(processors) - jobs[1][0]  # subtracts the first job's arrival time from the completion time

def main():
    ''' Runs the tests for various processor procedures. User should change number_of_tests, number_of_jobs, and std_no
        to alter test parameters. number_of_processors is determined by std_no, as required in the assignment. '''
    number_of_tests = 100
    number_of_jobs = 1000
    std_no = 2822
    number_of_processors = std_no % 3 + 2  # comes out as 4
    min = [sys.maxsize, sys.maxsize]
    max = [0, 0]
    circle_avg = []
    custom_avg = []

    for i in range(number_of_tests):
        # creates a list of jobs that both circular_test and custom_test will use for this test
        jobs = create_random_jobs(number_of_jobs)

        # a new list of processors is created for each test algorithm
        current_test = circular_test(jobs, create_processors(number_of_processors))
        if min[0] > current_test: min[0] = current_test
        if max[0] < current_test: max[0] = current_test
        circle_avg.append(current_test)

        current_test = custom_test(jobs, create_processors(number_of_processors))
        if min[1] > current_test: min[1] = current_test
        if max[1] < current_test: max[1] = current_test
        custom_avg.append(current_test)

    # Tests the algorithms on the provided set of jobs
    circle_set_test = circular_test(create_set_jobs(), create_processors(number_of_processors))
    custom_set_test = custom_test(create_set_jobs(), create_processors(number_of_processors))

    # outputs various statistics to congdon_samuel-1.output file
    fout = open("congdon_samuel-1.output", 'w')
    fout.write("Running {} tests of {} jobs using {} processors resulted in the following statistics.\n\n"
               "CIRCULAR PROCEDURE:\nMinimum: {} ms\nMaximum: {} ms\nAverage: {:0.2f} ms\nStandard Deviation: {:0.2f}\n"
               "Provided set overall turnaround time: {} ms\n\nCUSTOM PROCEDURE:\nMinimum: {} ms\nMaximum: {} ms\nAverage: {:0.2f} "
               "ms\nStandard Deviation: {:0.2f}\nProvided set overall turnaround time: {} ms\n\n"
               "".format(number_of_tests, number_of_jobs, number_of_processors, min[0], max[0], mean(circle_avg),
                         stdev(circle_avg), circle_set_test, min[1], max[1], mean(custom_avg), stdev(custom_avg), custom_set_test))
    fout.close()

if __name__ == "__main__":
    main()