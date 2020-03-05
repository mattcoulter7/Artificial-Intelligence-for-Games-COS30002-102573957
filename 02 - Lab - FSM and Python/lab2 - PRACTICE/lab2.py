# Three state machine example ... bad code included.

# variables
remaining_time = 30
battery_life = 1000

states = ['red','amber','green']
current_state = 'red'

alive = True
running = True
max_limit = 100
game_time = 0

while running and alive:
    game_time += 1
    remaining_time -= 0.001
    # Sleeping: reduced tired, hunger still increases
    if current_state is 'red':
        # Do things for this state
        print("Don't Move!")
        # updates
        if remaining_time == 0:
            current_state = "green"
            remaining_time = 50

    # Awake: does nothing interesting. gets hunugry. gets tired
    elif current_state is 'amber':
        print("SLOW DOWN!")
        if remaining_time == 0:
            current_state = "red"
            remaining_time = 30
            
    # Eating: reduces hunger, still gets tired
    elif current_state is 'green':
        print("GO... GO... GOOOOOOOO!!")
        if remaining_time == 0:
            current_state = "amber"
            remaining_time = 3

    # if battery_life == 100:
    #    print("URGENT: Battery is running low")

    # if battery_life <= 0:
    #    alive = False
        
    # Check for end of game time
    if game_time > max_limit:
        running = False

print('GOODBYE')


    

