from input_parser import InputParser


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class FlightSearcher:
    def __init__(self):
        self.flight_data = InputParser().process_user_input()
        self.input_dict = InputParser().user_input

    def _filter_by_bag_counts(self):
        """
        Keep the flights where the number of allowed bags meets the searched number of bags.
        :return: filtered flights generator
        """
        return (flight for flight in self.flight_data if int(flight.bags_allowed) >= self.input_dict['bags_count'])


if __name__ == "__main__":
    FlightSearcher()
