from typing import Generator, List, Tuple
from collections import defaultdict, deque
from input_parser import InputParser
from helpers import Stack


class Graph(object):
    """ Graph data structure, directed by default. """

    def __init__(self, connections, directed=True):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (origin-destination pairs) to graph """

        for origin, destination in connections:
            self.add(origin, destination)

    def add(self, origin, destination):
        """ Add connection between origin and destination """

        self._graph[origin].add(destination)
        if not self._directed:
            self._graph[destination].add(origin)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))


class FlightSearcher:
    def __init__(self):
        self.flight_data = InputParser().process_user_input()
        self.input_dict = InputParser().user_input
        self.paths = []

    def _filter_by_bag_counts(self) -> Generator:
        """
        Keep the flights where the number of allowed bags meets the searched number of bags.
        :return: filtered flights generator
        """
        return (flight for flight in self.flight_data if int(flight.bags_allowed) >= self.input_dict['bags_count'])

    def _contains_origin(self, data: Generator) -> bool:
        if self.input_dict['origin'].upper() in (flight.origin for flight in data):
            return True
        else:
            raise AttributeError(f'Origin airport code {self.input_dict["origin"]} is not found')

    def _contains_destination(self, data: Generator) -> bool:
        if self.input_dict['destination'].upper() in (flight.destination for flight in data):
            return True
        else:
            raise AttributeError(f'Destination airport code {self.input_dict["destination"]} is not found')

    def _create_pairs(self, data) -> List[Tuple]:
        """ Regroup flight information into tuples to be able to build a graph """
        return [(flight.origin, flight) for flight in data]

    def _build_graph(self, data) -> Graph:
        pairs = self._create_pairs(data)
        return Graph(pairs)

    def _save_path(self, origin, destination, parents):
        stack = Stack()
        first, last = destination, parents[destination]
        while last is not None:
            stack.push(first)
            first, last = last, parents[last]
        stack.push(first)
        stack.push(last)
        path = []
        while not stack.is_empty():
            node = stack.pop()
            path.append(node) if node is not None else path
        self.paths.append(path)

    def search_flights(self):
        """ pathfinding using breadth-first search algorithm"""
        origin = self.input_dict['origin']
        destination = self.input_dict['destination']

        filtered_flight_data = self._filter_by_bag_counts()
        self._contains_origin(filtered_flight_data)
        self._contains_destination(filtered_flight_data)
        graph = self._build_graph(filtered_flight_data)
        q = deque()
        parents = {}
        visited = []
        q.append(origin)
        parents[origin] = None

        while not not q:  # queue not empty
            node = q.popleft()
            if node == destination:
                self._save_path(origin, destination, parents)
                print(self.paths)
                return


if __name__ == "__main__":
    # FlightSearcher().search_flights()
    # InputParser().process_user_input()
    pass
