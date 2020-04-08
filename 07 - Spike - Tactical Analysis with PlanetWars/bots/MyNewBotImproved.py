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

                # Always send from the planet with the highest value that is closest to the centre
                src = min(haveShips, default=gameinfo.my_planets.values(), key=lambda p: gameinfo.planets[1].distance_to(p)/p.num_ships)

                # Generates a new list containing any ships that our src would be table to cpature considering distance and groth rate
                lessShips = filter(lambda x: int(x.num_ships+x.distance_to(src)*x.growth_rate) < int(src.num_ships), gameinfo.not_my_planets.values())
                
                # Chooses destination based off of the highest value that represents the ratio between distance and value is calculated
                dest = max(lessShips, default=gameinfo.not_my_planets.values(), key=lambda p: p.num_ships/p.distance_to(src))

                # launch new fleet if there's enough ships
                # Sends fleet size calculated by distance away and growth rate to ensure it captures with just enough ships
                if src.num_ships > 10 and dest is not None:
                    gameinfo.planet_order(src, dest, int(dest.num_ships+(dest.distance_to(src) + 1)*dest.growth_rate))

                # print("Planet %s attacked Planet %s from a distance of %s with %s ships" % (src.id,dest.id,round(src.distance_to(dest)),round(src.num_ships*0.75)))

