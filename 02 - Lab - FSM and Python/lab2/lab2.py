# Three state machine example ... bad code included.

# variables
stamina = 0
adrenaline = 0
frustration = 0

states = ['waiting','running','hitting','celebrating']
current_state = 'waiting'

alive = True
running = True
max_limit = 100
game_time = 0

while running and alive:
    game_time += 1

    # waiting: increases stamina
    if current_state is 'waiting':
        # Do things for this state
        print("...")
        stamina += 1
        # Check for change state
        if stamina > 10:
            current_state = 'running'

    # running: reduces stamina, increases adrenaline, increases frustration
    elif current_state is 'running':
        # Do things for this state
        print("clomp")
        stamina -= 1
        adrenaline += 1
        frustration += 1
        # Check for change state
        if stamina < 6:
            current_state = 'hitting'
            
    # hitting: reduces stamina, increases adrenaline, increases/decreases frustration level depending on whether the ball goes in or out
    elif current_state is 'hitting':
        # Do things for this state
        print("smack")
        stamina -= 1
        adrenaline += 1
        frustration -= 1
        # Check for change state
        if frustration < 4:
            current_state = 'celebrating'
               
    # celebrating: reduces frustration level
    elif current_state is 'celebrating':
        # Do things for this state
        print("hooray!")
        frustration -= 1
        # Check for change state
        if frustration < 0:
            current_state = 'waiting' 
            
    # check for broken ... :(
    else:
        print("AH! BROKEN .... how did you get here?")
        die() # not a real function - just breaks things! :)

    if stamina == 0:
        alive = False
        
    # Check for end of game time
    if game_time > max_limit:
        running = False

print('-- The End --')


    
