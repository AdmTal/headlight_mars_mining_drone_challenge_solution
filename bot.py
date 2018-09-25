import os
import math

from cms_api import CmsApi
from traveling_salesman_solver import basic_tsp_solution
from image import GridImageMaker

GRID_MAX_X = int(os.environ['GRID_MAX_X'])
GRID_MAX_Y = int(os.environ['GRID_MAX_Y'])

SCAN_DISTANCE_X = int(os.environ['SCAN_DISTANCE_X'])
SCAN_DISTANCE_Y = int(os.environ['SCAN_DISTANCE_Y'])

MAX_CLAIMS = int(os.environ['MAX_CLAIMS'])

SHOW_IMAGE = bool(int(os.environ['SHOW_IMAGE']))

APPLY_TRAVELING_SALESMAN_SOLUTION = True


class BotImageMaker:
    """Helper class to visualize the PATH that the BOT will take"""

    def __init__(self, scan_locations):
        image_maker = GridImageMaker(GRID_MAX_X, GRID_MAX_Y)

        # Print Optimal Scan Locations
        scan_delta = math.floor(SCAN_DISTANCE_X / 2)
        for x, y in scan_locations:
            image_maker.fill_square(x, y)
            image_maker.outline_area(
                x - scan_delta,
                y - scan_delta,
                x + scan_delta + 1,
                y + scan_delta + 1
            )

        # Print Path between scanning locations
        num_locations = len(scan_locations)
        edges = []
        for i in range(0, num_locations - 1):
            edges.append([scan_locations[i], scan_locations[i + 1]])

        edges.append([scan_locations[0], scan_locations[-1]])

        for a, b in edges:
            image_maker.draw_path(a[0], a[1], b[0], b[1])

        image_maker.show_image()


class Bot:
    """A bot for mining Prometheum"""

    @staticmethod
    def log(message, indent_level=0):
        print(('\t' * indent_level) + message)

    def __init__(self, callsign):
        """Constructor for Bot"""

        # Register with the CMS
        self.log('Bot is coming online with callsign = {callsign}'.format(callsign=callsign))
        self.cms_api = CmsApi(callsign)
        registration_response = self.cms_api.register()

        # Handle registration Error
        if registration_response['Error']:
            raise Exception('Could not register with the CMS : {message}'.format(
                message=registration_response['ErrorMsg']
            ))

        # Save Starting Location
        self.location_x = registration_response['Status']['Location']['X']
        self.location_y = registration_response['Status']['Location']['Y']
        self.log('Starting location is ({x}, {y})'.format(x=self.location_x, y=self.location_y))

        # Calculate the optimal scanning locations
        self.scan_locations = self.calculate_optimal_scan_locations()

        if APPLY_TRAVELING_SALESMAN_SOLUTION:
            self.log('Solving Traveling Salesman...')
            self.scan_locations = basic_tsp_solution(self.scan_locations)

        if SHOW_IMAGE:
            BotImageMaker(self.scan_locations)

        # Find the closest point on the path to the starting point
        self.next_scan_location_index = \
            self.find_nearest_scan_location(self.location_x, self.location_y, self.scan_locations)

        # Decrement index - will be incremented at the top of the Main Loop
        self.next_scan_location_index -= 1

        # Start the Bot's main routine
        self.main()

    @staticmethod
    def calculate_optimal_scan_locations():
        """Given the grid size and scan distance - calculate the optimal scan locations"""

        # Calculate Min + Max bounds - to avoid scanning too close to the Grid's edges
        min_x = math.floor(SCAN_DISTANCE_X / 2)
        max_x = GRID_MAX_X - min_x
        min_y = math.floor(SCAN_DISTANCE_Y / 2)
        max_y = GRID_MAX_Y - min_y

        # Find the optimal X and Y coordinates that allow for scans with minimal overla
        x_coords = range(min_x, max_x, SCAN_DISTANCE_X)
        y_coords = range(min_y, max_y, SCAN_DISTANCE_Y)

        # Produce final list of coords as all parings of optimal X and Y coords
        scan_locations = []
        for x_coord in x_coords:
            for y_coord in y_coords:
                scan_locations.append([x_coord, y_coord])

        return [i for i in scan_locations]

    @staticmethod
    def distance_between_points(x1, y1, x2, y2):
        """Return the distance between two points"""
        return abs(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

    def find_nearest_scan_location(self, x, y, scan_locations):
        """For the given X, Y coordinate, returns the index of the closest scan location"""
        min_distince_found = float('inf')
        nearest_location_index = 0

        for index, scan_location in enumerate(scan_locations):
            loc_x, loc_y = scan_location
            distance = self.distance_between_points(x, y, loc_x, loc_y)
            if distance < min_distince_found:
                min_distince_found = distance
                nearest_location_index = index

        return nearest_location_index

    def move_to_coord(self, dest_x, dest_y):
        """Moves the bot from it's current location to the destination X, Y coords"""
        while self.location_x != dest_x and self.location_y != dest_y:
            x_delta = 0
            y_delta = 0

            if dest_x > self.location_x:
                x_delta = 1
            elif dest_x < self.location_x:
                x_delta = -1

            if dest_y > self.location_y:
                y_delta = 1
            elif dest_y < self.location_y:
                y_delta = -1

            move_response = self.cms_api.move(self.location_x + x_delta, self.location_y + y_delta)

            if move_response['Error']:
                # If there is an error moving - return and hope to try again later
                # I have not hit this error state yet
                return

            self.location_x = move_response['Status']['Location']['X']
            self.location_y = move_response['Status']['Location']['Y']

    def main(self):

        # Start Main Loop
        while True:

            # Find and move to next optimal scanning location
            self.next_scan_location_index += 1
            if self.next_scan_location_index >= len(self.scan_locations):
                self.next_scan_location_index = 0
            next_scanning_location = self.scan_locations[self.next_scan_location_index]
            self.log('Moving to {location}'.format(location=next_scanning_location))
            self.move_to_coord(*next_scanning_location)

            # Scan the current location for Nodes
            scan_response = self.cms_api.scan()

            # Report the current score
            score = scan_response['Status']['Score']
            self.log('Score is currently {score}'.format(score=score))

            # Check if any nodes can be mined, mine the most valuable first
            nodes_of_value = [node for node in scan_response['Nodes'] if not node['Claimed'] and node['Value']]

            if not nodes_of_value:
                self.log('\tNo Nodes found - moving to next optimal scan location')
                continue

            self.log('{x} nodes found - suitable for mining'.format(x=len(nodes_of_value)), 1)
            remaining_nodes = sorted(nodes_of_value, key=lambda x: x['Value'], reverse=True)

            claimed_nodes = []

            # Loop to Claim or Mine nodes
            while remaining_nodes or claimed_nodes:

                # Attempt to claim up to MAX_NODES before mining
                if remaining_nodes and len(claimed_nodes) < MAX_CLAIMS:
                    # Claim this node
                    node = remaining_nodes.pop(0)
                    node_id = node['Id']
                    claim_response = self.cms_api.claim(node_id)

                    if claim_response['Error']:
                        # Skip this Node if Claim fails
                        continue

                    self.log('CLAIMED {node_id} with value {value}'.format(value=node['Value'], node_id=node_id), 2)

                    claimed_nodes.append(node)

                    # Return to top of loop to Claim more or Mine
                    continue

                # Attempt to Mine a node to completion
                node = claimed_nodes.pop(0)
                node_id = node['Id']

                # Attempt to Mine this Node while it still has Value left
                value_extracted = 0
                while node['Value']:
                    self.log('Mining 1 Value from Node {node_id}...'.format(node_id=node_id), 3)
                    mine_response = self.cms_api.mine(node_id)
                    node['Value'] -= 1
                    value_extracted += 1

                    if mine_response['Error']:
                        # If Mining fails for any reason - Stop and move to the next node
                        break

                self.log('MINED {value} Value from Node {node_id}'.format(value=value_extracted, node_id=node_id), 2)

                # When mining is done - release the node
                release_response = self.cms_api.release(node_id)

                if release_response['Error']:
                    raise Exception('Error - can not release a Node - call for backup')

                self.log('RELEASE Node {node_id}'.format(node_id=node_id), 2)


my_bot = Bot('AdamTal')
