from collections import defaultdict
from typing import Dict
from fligh_dataclass import FlightData


class Stack:
    """A container with a last-in-first-out (LIFO) queuing policy."""
    def __init__(self):
        self.list = []

    def push(self, item):
        """Push 'item' onto the stack"""
        self.list.append(item)

    def pop(self):
        """Pop the most recently pushed item from the stack"""
        return self.list.pop()

    def is_empty(self):
        """Returns true if the stack is empty"""
        return len(self.list) == 0


class Graph(object):
    """ Graph data structure, directed by default. """

    def __init__(self, connections: Dict[str, FlightData], directed: bool = True):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections: Dict[str, FlightData]) -> None:
        """ Add connections (origin-destination pairs) to graph """

        for origin, destination in connections.items():
            self.add(origin, destination)

    def add(self, origin: str, destination: FlightData) -> None:
        """ Add connection between origin and destination """

        self._graph[origin].add(destination.destination)
        if not self._directed:
            self._graph[destination.destination].add(origin)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))