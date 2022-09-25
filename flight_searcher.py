from collections import deque, defaultdict
from input_parser import InputParser
from typing import Iterable, Dict, List
from fligh_dataclass import FlightData


class FlightSearcher:
    def __init__(self):
        self.flight_data: List[FlightData] = InputParser().process_user_input() # TODO sort input flights
        self.user_input: dict = InputParser().user_input
        self.found_paths: List[FlightData] = []
        self.tmp_output = deque()

    def _filter_by_bag_counts(self) -> Iterable:
        """
        Keep the flights where the number of allowed bags meets the searched number of bags.
        :return: filtered flights generator
        """
        return (flight for flight in self.flight_data if int(flight.bags_allowed) >= self.user_input['bags_count'])

    def _validate_if_contains_origin(self, data: Iterable) -> None:
        if not self.user_input['origin'].upper() in (flight.origin for flight in data):
            raise AttributeError(f'Origin airport code {self.user_input["origin"]} is not found')

    def _validate_if_contains_destination(self, data: Iterable) -> None:
        if not self.user_input['destination'].upper() in (flight.destination for flight in data):
            raise AttributeError(f'Destination airport code {self.user_input["destination"]} is not found')

    def _create_pairs(self, data: Iterable) -> Dict[str, List[FlightData]]:  # TODO remove duplicated func
        """ Create helper index to be able to build a graph """
        indexed_flights = defaultdict(list)
        for flight in data:
            indexed_flights[flight.origin].append(flight)
        return indexed_flights

    def _extract_routes(self, path: FlightData):
        """recursive function to build full route for each flight"""
        if not path.parent:
            self.tmp_output.appendleft(path)
            return
        else:
            self.tmp_output.appendleft(path)
            path = path.parent
            self._extract_routes(path)

    def _build_output(self):
        """function for building the output json"""
        result = []
        for path in self.found_paths:
            self._extract_routes(path)
            result.append({'flights': self.tmp_output.copy()})
            self.tmp_output.clear()
        return result

    def search_flights(self):
        """ pathfinding using breadth-first search algorithm"""
        origin = self.user_input['origin']
        destination = self.user_input['destination']

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
                self.found_paths.append(node)
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
        routes_output = self._build_output()
        print(self.found_paths)


if __name__ == "__main__":
    FlightSearcher().search_flights()
    pass
