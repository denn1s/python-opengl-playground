# import the pygame module, so you can use it
import pygame

# define a main function

# initialize the pygame module
pygame.init()

# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((800, 600))



# define a variable to control the main loop
running = True    
# main loop
while running:
    # event handling, gets all event from the event queue
    x = 100
    y = 100
    screen.set_at((x, y), (255, 255, 255))

    pygame.display.flip()

    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False
     
