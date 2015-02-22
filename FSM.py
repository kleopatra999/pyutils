#!/usr/bin/python
from collections import deque
import sys, time, select

""" A simple Finite state machine class.

The initial state is always 'INIT'. When events are delivered, the 
state changes, and corresponding functions get invoked.
See __main__ code below for an example.
"""

# fsm.enqueue_event('BEGIN')

class FSM:
    def __init__(self, fsm):
        self.events = deque()
        self.state = 'INIT'
        self.fsm = fsm

    def enqueue_event(self, event):
        #print "Enqueueing: " + event
        self.events.append(event)

    def have_events(self):
        return (len(self.events) > 0)

    def deliver_event(self, event):
        str = self.state + '-' + event
        if not str in self.fsm:
            raise RuntimeError("Don't know how to handle event {0} while in state {1}".format(event, self.state))
        (nextstate, action) = self.fsm[str]
        # print "Current state: {0}, event: {1}, next state: {2}".format(self.state, event, nextstate)
        self.state = nextstate;
        if action:
            ret = action()
            if ret:
                if ret == 'END':
                    return False
                else:
                    self.enqueue_event(ret)
                    return True

    def get_next_event(self):
        if len(self.events) == 0:
            raise RuntimeError("Event queue is empty!")
        return self.events.popleft()

    def run(self):
        running = True
        while running:
            event = self.get_next_event()
            running = self.deliver_event(event)

if __name__ == "__main__":
# Extremely simple alien-invaders like game.
# Start out running.

# State change handlers. A handler is invoked in response to an event.
    def run():
        print "Now running."
        # Get hit
        print "I'm hit!"
        return 'HIT'

    def degrade():
        print "Dropping to degrade."
        # Get hit while in a degraded mode
        #return 'HIT'
        print "Made it!"
        return 'GOAL'

    def finish():
        print "Hasta La Vista Baby!"
        # Finish game
        return 'END'

    def complete():
        print "You won!"
        # Finish game
        return 'END'

    # Define the state change table.
    state_table = {}
    state_table['INIT-BEGIN'] = ['RUNNING', run]
    state_table['RUNNING-HIT'] = ['DEGRADED', degrade]
    state_table['DEGRADED-HIT'] = ['DEAD', finish]
    state_table['RUNNING-GOAL'] = ['WON', complete]
    state_table['DEGRADED-GOAL'] = ['WON', complete]
    fsm = FSM(state_table)
    fsm.enqueue_event('BEGIN')
    # Start the game
    fsm.run()
