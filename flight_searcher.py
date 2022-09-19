from collections import deque, defaultdict
from input_parser import InputParser
from typing import Iterable, Dict, List
from fligh_dataclass import FlightData


class FlightSearcher:
    def __init__(self):
        self.flight_data = InputParser().process_user_input()
        self.input_dict = InputParser().user_input # TODO sort input flights
        self.paths = []

    def _filter_by_bag_counts(self) -> Iterable:
        """
        Keep the flights where the number of allowed bags meets the searched number of bags.
        :return: filtered flights generator
        """
        return (flight for flight in self.flight_data if int(flight.bags_allowed) >= self.input_dict['bags_count'])

    def _validate_if_contains_origin(self, data: Iterable) -> None:
        if not self.input_dict['origin'].upper() in (flight.origin for flight in data):
            raise AttributeError(f'Origin airport code {self.input_dict["origin"]} is not found')

    def _validate_if_contains_destination(self, data: Iterable) -> None:
        if not self.input_dict['destination'].upper() in (flight.destination for flight in data):
            raise AttributeError(f'Destination airport code {self.input_dict["destination"]} is not found')

    def _create_pairs(self, data: Iterable) -> Dict[str, List[FlightData]]: # TODO remove duplicated func
        """ Create helper index to be able to build a graph """
        indexed_flights = defaultdict(list)
        for flight in data:
            indexed_flights[flight.origin].append(flight)
        return indexed_flights

    def search_flights(self):
        """ pathfinding using breadth-first search algorithm"""
        origin = self.input_dict['origin']
        destination = self.input_dict['destination']

        filtered_flight_data = self._filter_by_bag_counts()
        self._validate_if_contains_origin(filtered_flight_data)
        self._validate_if_contains_destination(filtered_flight_data)
        graph = self._create_pairs(filtered_flight_data)
        q = deque()
        visited = []
        for flight in graph.get(origin):
            q.append(flight)

        while not not q:  # queue not empty
            node = q.popleft()
            if node.destination == destination:
                self.paths.append(node)
                continue
            possible_routes = graph.get(node.destination)
            for possible_node in possible_routes:
                if possible_node.destination == origin:
                    continue

                if bool(1 < (possible_node.departure - node.arrival).total_seconds() / 3600 < 6) is False:
                    continue

                possible_node.parent = node
                if possible_node not in visited:
                    visited.append(possible_node)
                    q.append(possible_node)
        print(self.paths)


if __name__ == "__main__":
    FlightSearcher().search_flights()
    # InputParser().process_user_input()
    pass
