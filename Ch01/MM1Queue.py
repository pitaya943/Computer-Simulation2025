# -*- coding: utf-8 -*-
"""
Original file is located at
    https://colab.research.google.com/drive/1TJSIg6rO3sxixibdShQ1D2Zwyt_2Sk6k

Github for Computer Simulation's DEMO is located at
    https://github.com/pitaya943/Computer-Simulation2025/tree/main
"""

from google.colab import drive
import os
drive.mount('/content/drive')
path = "/content/drive/My Drive/Colab Notebooks/Computer Simulation"
print(os.listdir(path))

import sys
import math
import random
from datetime import datetime
from zoneinfo import ZoneInfo

class MM1Queue:
    def __init__(self, mean_interarrival, mean_service, num_delays_required, outfile):
        self.mean_interarrival = mean_interarrival
        self.mean_service = mean_service
        self.num_delays_required = num_delays_required
        self.outfile = outfile

        self.sim_time = 0.0
        self.num_custs_delayed = 0
        self.num_in_q = 0
        self.server_status = 0  # 0 = IDLE, 1 = BUSY
        self.q_limit = 100
        self.num_events = 2

        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.total_of_delays = 0.0
        self.time_last_event = 0.0

        self.time_arrival = [0.0] * (self.q_limit + 1)
        self.time_next_event = [0.0, 0.0, 1.0e+30]

    def expon(self, mean):
        return -mean * math.log(random.random())

    def initialize(self):
        self.sim_time = 0.0
        self.server_status = 0
        self.num_in_q = 0
        self.num_custs_delayed = 0
        self.total_of_delays = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.time_last_event = 0.0

        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)
        self.time_next_event[2] = 1.0e+30

    def timing(self):
        min_time_next_event = min(self.time_next_event[1:self.num_events + 1])
        self.next_event_type = self.time_next_event.index(min_time_next_event)

        if self.next_event_type == 0:
            print(f'\nEvent list EMPTY at time {self.sim_time}', file=self.outfile)
            sys.exit(1)

        self.sim_time = min_time_next_event

    def arrive(self):
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)

        if self.server_status == 1:
            self.num_in_q += 1
            if self.num_in_q > self.q_limit:

                print('\nOverflow of the array time_arrival at', file=self.outfile)
                print(f'time {self.sim_time}', file=self.outfile)
                sys.exit(2)

            self.time_arrival[self.num_in_q] = self.sim_time
        else:
            delay = 0.0
            self.total_of_delays += delay
            self.num_custs_delayed += 1
            self.server_status = 1
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)

    def depart(self):
        if self.num_in_q == 0:
            self.server_status = 0
            self.time_next_event[2] = 1.0e+30
        else:
            self.num_in_q -= 1
            delay = self.sim_time - self.time_arrival[1]
            self.total_of_delays += delay
            self.num_custs_delayed += 1
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)
            for i in range(1, self.num_in_q + 1):
                self.time_arrival[i] = self.time_arrival[i + 1]
                self.time_arrival[i + 1] = 0.0
            if self.num_in_q == 0:
                self.time_arrival[1] = 0.0

    def update_time_avg_stats(self):
        time_since_last_event = self.sim_time - self.time_last_event
        self.time_last_event = self.sim_time
        self.area_num_in_q += self.num_in_q * time_since_last_event
        self.area_server_status += self.server_status * time_since_last_event

    def report(self):

        print('\n\n------------------------------------------', file=self.outfile)
        print(f'Average delay in queue {(self.total_of_delays / self.num_custs_delayed):11.3f} minutes', file=self.outfile)
        print(f'Average number in queue {(self.area_num_in_q / self.sim_time):10.3f}', file=self.outfile)
        print(f'Server utilization {(self.area_server_status / self.sim_time):15.3f}', file=self.outfile)
        print(f'Time simulation ended {self.sim_time:12.3f} minutes', file=self.outfile)
        print('------------------------------------------\n', file=self.outfile)

    def run_simulation(self):
        self.initialize()

        print(f'Initialization time: {self.sim_time}', file=self.outfile)
        print(f'Server status: {self.server_status}', file=self.outfile)
        print(f'Number in queue: {self.num_in_q}', file=self.outfile)
        print(f'Times of arrival: {self.time_arrival[1:]}', file=self.outfile)
        print(f'Time of last event: {self.time_last_event}', file=self.outfile)
        print(f'Clock: {self.time_last_event}', file=self.outfile)
        print(f'Event list: {self.time_next_event[1:]}', file=self.outfile)
        print(f'Number delayed: {self.num_custs_delayed}', file=self.outfile)
        print(f'Total delay: {self.total_of_delays}', file=self.outfile)
        print(f'Area under Q(t): {self.area_num_in_q}', file=self.outfile)
        print(f'Area under B(t): {self.area_server_status}\n', file=self.outfile)

        while self.num_custs_delayed < self.num_delays_required:
            self.timing()
            self.update_time_avg_stats()
            if self.next_event_type == 1:
                self.arrive()

                print(f'Arrival time: {self.sim_time}', file=self.outfile)
                print(f'Server status: {self.server_status}', file=self.outfile)
                print(f'Number in queue: {self.num_in_q}', file=self.outfile)
                print(f'Times of arrival: {self.time_arrival[1:]}', file=self.outfile)
                print(f'Time of last event: {self.time_last_event}', file=self.outfile)
                print(f'Clock: {self.time_last_event}', file=self.outfile)
                print(f'Event list: {self.time_next_event[1:]}', file=self.outfile)
                print(f'Number delayed: {self.num_custs_delayed}', file=self.outfile)
                print(f'Total delay: {self.total_of_delays}', file=self.outfile)
                print(f'Area under Q(t): {self.area_num_in_q}', file=self.outfile)
                print(f'Area under B(t): {self.area_server_status}\n', file=self.outfile)

            elif self.next_event_type == 2:
                self.depart()

                print(f'Departure time: {self.sim_time}', file=self.outfile)
                print(f'Server status: {self.server_status}', file=self.outfile)
                print(f'Number in queue: {self.num_in_q}', file=self.outfile)
                print(f'Times of arrival: {self.time_arrival[1:]}', file=self.outfile)
                print(f'Time of last event: {self.time_last_event}', file=self.outfile)
                print(f'Clock: {self.time_last_event}', file=self.outfile)
                print(f'Event list: {self.time_next_event[1:]}', file=self.outfile)
                print(f'Number delayed: {self.num_custs_delayed}', file=self.outfile)
                print(f'Total delay: {self.total_of_delays}', file=self.outfile)
                print(f'Area under Q(t): {self.area_num_in_q}', file=self.outfile)
                print(f'Area under B(t): {self.area_server_status}\n', file=self.outfile)

            else:
                print('next_event_type ERROR!', file=self.outfile)
        self.report()

def main():
    in_path = '/content/drive/My Drive/Colab Notebooks/Computer Simulation/mm1.in'
    out_path = '/content/drive/My Drive/Colab Notebooks/Computer Simulation/mm1.out'

    with open(in_path, 'r') as infile, open(out_path, 'w') as outfile:
        line = infile.readline().strip()
        mean_interarrival, mean_service, num_delays_required = map(float, line.split())
        num_delays_required = int(num_delays_required)

        utc_time = datetime.now(ZoneInfo('UTC'))
        start_time = utc_time.astimezone(ZoneInfo('Asia/Taipei')).strftime('%m-%d-%Y %H:%M:%S')
        outfile.write(f'Start at {start_time}\n\n')

        outfile.write('------------------------------------------\n')
        outfile.write('// Single-Server Queueing System //\n')
        outfile.write(f'Mean interarrival time{mean_interarrival:11.3f} minutes\n')
        outfile.write(f'Mean service time{mean_service:16.3f} minutes\n')
        outfile.write(f'Number of customers{num_delays_required:14d}\n')
        outfile.write('------------------------------------------\n\n')

        mm1_queue = MM1Queue(mean_interarrival, mean_service, num_delays_required, outfile)
        mm1_queue.run_simulation()

        utc_time = datetime.now(ZoneInfo('UTC'))
        finished_time = utc_time.astimezone(ZoneInfo('Asia/Taipei')).strftime('%m-%d-%Y %H:%M:%S')
        outfile.write(f'Finished at {finished_time}')

main()