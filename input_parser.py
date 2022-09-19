import argparse
import os
import csv
from fligh_dataclass import FlightData
from typing import List


def parse_arguments() -> dict:
    """
    Parse all command line arguments and return an object with all read arguments.
    """
    parser = argparse.ArgumentParser("flight_search")
    parser.add_argument('flight_data_file', type=str, help='The path of flight data .csv file', nargs=1)
    parser.add_argument("origin", type=str, help='Origin airport code', nargs=1)
    parser.add_argument("destination", type=str, help='Destination airport code', nargs=1)
    parser.add_argument('--bags', dest="bags_count", default=0, type=int,
                        help='Number of requested bags. Optional (defaults to 0)'
                        )
    parser.add_argument('--return', dest="is_return", action='store_true',
                        help='Is it a return flight?. Optional (defaults to false)'
                        )
    # args = parser.parse_args()

    # result = {
    #     "flight_data_file": args.flight_data_file.pop(0),
    #     "origin": args.origin.pop(0),
    #     "destination": args.destination.pop(0),
    #     "bags_count": args.bags_count,
    #     "is_return": args.is_return
    # }
    result = {
        "flight_data_file": 'example/example0.csv',
        "origin": 'ECV',
        "destination": 'RFZ',
        "bags_count": 0,
        "is_return": False
    }
    return result


class InputParser:
    """
    The class validates user input arguments and parse .csv file. Flight data are stored as NamedTuple to be
    able to transform this structure into graph and apply further searching algorithms.
    """
    def __init__(self):
        self.user_input = parse_arguments()

    def _check_upload_path(self) -> None:
        """
        Check the given class if all necessary components are present.
        :return:
        :raises ValueError: In case that some components of a given path does not exist
        """

        if not os.path.exists(self.user_input['flight_data_file']):
            raise ValueError("The base path to flight data file does not exist")

    def _check_airport_codes(self) -> None:
        """
        Check if airport code contains three letters.
        :return: raises ValueError if format of airport codes is not correct
        """
        airport_codes = {'origin': self.user_input['origin'], 'destination': self.user_input['destination']}
        for key, value in airport_codes.items():
            if not value.isalpha() or len(value) != 3:
                raise ValueError(f"The {key} airport code should contain three letters")

    def _store_flight_data(self) -> List[FlightData]:
        """
        Read .csv file containing flights data and store each flight from the table in dataclasses as
        for better readability.
        """
        with open(self.user_input['flight_data_file'], 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            flights = []
            for row in reader:
                flight = FlightData(*row)
                flights.append(flight)
            return flights

    def process_user_input(self) -> List[FlightData]:
        """Main function executing the above defined steps
        :return: named tuples for flight data packed in generator object
        """
        self._check_upload_path()
        self._check_airport_codes()
        flights = self._store_flight_data()
        return flights
