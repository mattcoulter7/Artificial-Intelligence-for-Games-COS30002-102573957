from random import choice
from collections import Counter

class MyNewBotImproved(object):
        def update(self,gameinfo):
            # only send one fleet at a time
            if gameinfo.my_fleets:
                return
            # check if we should attack
            if gameinfo.my_planets and gameinfo.not_my_planets:
                # select strategic target and destination

                # List of AI's planets that have ships to avoid divide by 0
                haveShips = filter(lambda x: int(x.num_ships) > 0, gameinfo.my_planets.values())

                # Enemy planet with least amount of ships
                leastships = min(gameinfo.not_my_planets.values(),key = lambda p: p.num_ships)

                # Always send from the planet with the highest value that is closest to the centre
                src = min(haveShips, key=lambda p: leastships.distance_to(p)/p.num_ships)

                # Generates a new list containing any ships that our src would be table to cpature considering distance and groth rate
                lessShips = filter(lambda x: int(x.num_ships+x.distance_to(src)*x.growth_rate) < int(src.num_ships), gameinfo.not_my_planets.values())
                
                # Calculates a default destination that is used for when less ships is null
                defaultdest = max(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships/p.distance_to(src))

                # Chooses destination based off of the highest value that represents the ratio between distance and value is calculated
                dest = max(lessShips, key=lambda p: p.num_ships/p.distance_to(src),default=defaultdest)

                # launch new fleet if there's enough ships
                # Sends fleet size calculated by distance away and growth rate to ensure it captures with just enough ships
                if src.num_ships > 10 and dest is not None:
                    gameinfo.planet_order(src, dest, int(dest.num_ships+(dest.distance_to(src) + 1)*dest.growth_rate))

