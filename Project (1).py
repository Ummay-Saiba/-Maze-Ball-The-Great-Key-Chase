import sys
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# catcher initial positions
catcher_pos_x, catcher_pos_y = 35, 456

# catcher size
catcher_rad = 7

# catcher movement speed
catcher_speed = 12 # max limit 10

# catcher points
score = 0

# Keeps track of the level
level = 1

# Difficulty state
difficulty_status = { 1 : 'Easy',
                      2 : 'Medium',
                      3 : 'Hard'}

# define obstackle---> initial posiyions
obst_one_pos =  (250, 250)
obst_two_pos =  (30, 40)
obst_three_pos =  (450, 450)

# Store Obstackle---> in a list
obstackle_lst = [obst_one_pos, obst_two_pos, obst_three_pos]

# initial game status---> False
game_play, game_over, is_game_pause = False, False, False

# allocate---> initial time frame
# initially entire time left
total_time, left_time = 60, 60 # in second's

def display_pixel(x, y, color):
    glPointSize(2.5)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glColor3f(color[0], color[1], color[2])
    glVertex2f(x, y)  # jekhane show korbe pixel
    glEnd()


# figures out the---> zone n
def find_actual_zone(x1, y1, x2, y2):

    # get the---> differences
    del_x,del_y = x2-x1, y2-y1


    # get the abs differences---> to get into the segment of four zone
    val_01 = abs(del_x)
    val_02 = abs(del_y)

    # check for---> zone 1, 2, 5, 6
    if (val_01 < val_02):
        if del_x >= 0 and del_y >= 0:
            zone = 1
        elif del_x <= 0 and del_y >= 0:
            zone = 2
        elif del_x <= 0 and del_y <= 0:
            zone = 5
        elif del_x >= 0 and del_y <= 0:
            zone = 6
    # get into---> zone 0, 3, 4, 7
    else:
        if del_x >= 0 and del_y >= 0:
            zone = 0
        elif del_x <= 0 and del_y >= 0:
            zone = 3
        elif del_x <= 0 and del_y <= 0:
            zone = 4
        elif del_x >= 0 and del_y <= 0:
            zone = 7

    # give us the belonged zone
    return zone

# convert zone n---> zone 0
# for calculation simplicity.
def convert_zone_zero(zone, x, y):
    # check for---> 1, 2, 5, 6
    if zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, x)

    # check for---> 0, 3, 4, 7
    elif zone == 0:
        return (x, y)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 7:
        return (x, -y)

# convert zone 0---> zone n
def convert_original_zone(zone, x, y):
    # check for---> 1, 2, 5, 6
    if zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)

    # check for---> 0, 3, 4, 7
    elif zone == 0:
        return (x, y)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 7:
        return (x, -y)

# uses---> mpl approach
def display_line(x1, y1, x2, y2, color):
    # get the---> actual zone
    zone = find_actual_zone(x1, y1, x2, y2)

    # get the---> zone zero co-ordinates
    x1_zero, y1_zero = convert_zone_zero(zone, x1, y1)
    x2_zero, y2_zero = convert_zone_zero(zone, x2, y2)

    # get the differences ---> zone zero
    dx_zero = x2_zero - x1_zero
    dy_zero = y2_zero - y1_zero

    # assign the---> descition parameters
    decision = 2*dy_zero-dx_zero
    inc_North_East = 2 * (dy_zero - dx_zero)
    inc_East = 2*dy_zero

    # assign the x co-ordinate range ---> start to end point
    start = x1_zero
    end = x2_zero

    #assign the y co-ordinate range ---> from start
    y = y1_zero

    for x in range(start, end):

        # get the converted---> co-ordinates
        co_ordinates = convert_original_zone(zone, x, y)
        x_conv, y_conv= co_ordinates[0], co_ordinates[1]

        # display each pixel
        display_pixel(x_conv, y_conv, color)

        # check and update---> north east
        if decision >= 0:
            y += 1
            decision += inc_North_East
        # check and update---> east
        else:
            decision += inc_East

# uses---> 8 way symmetry approach to draw the circle points
def display_circle_point(cen_x, cen_y, dis_x, dis_y, color):
    display_pixel(cen_x - dis_y, cen_y - dis_x, color)
    display_pixel(cen_x - dis_x, cen_y - dis_y, color)
    display_pixel(cen_x + dis_y, cen_y - dis_x, color)
    display_pixel(cen_x + dis_x, cen_y + dis_y, color)
    display_pixel(cen_x - dis_y, cen_y + dis_x, color)
    display_pixel(cen_x + dis_y, cen_y + dis_x, color)
    display_pixel(cen_x - dis_x, cen_y + dis_y, color)
    display_pixel(cen_x + dis_x, cen_y - dis_y, color)

def mpc(cen_x, cen_y, rad, color):
    # assign---> necessary parameters
    decision, x, y = 1-rad, 0, rad

    # display--->  the initial points
    display_circle_point(cen_x, cen_y, x, y, color)

    # unless reaches---> end point
    while x < y:
        if decision  >= 0:
            y -= 1
            decision += 2*x - 2*y + 5  # update---> decision

        else:
            decision  += 2 * x + 3  # update---> decision

        # update x---> disregaring cases
        x += 1

        # draw the point
        display_circle_point(cen_x, cen_y, x, y, color)


def iterate():
    glViewport(0, 0, 500, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def collide(x, y, del_x, del_y):
    # assign---> maze boundary's
    boundary = [ [11, 489, 491, 489],   [11, 9, 491, 9],      [11, 9, 11, 489],
             [491, 9, 491, 489],    [91, 489, 91, 419],   [296, 489, 296, 419],
             [421, 489, 421, 439],  [11, 349, 126, 349],  [126, 349, 126, 449],
             [251, 319, 251, 369],  [191, 319, 351, 319], [351, 219, 351, 319],
             [351, 269, 391, 269],  [391, 269, 391, 329], [191, 279, 191, 319],
             [71, 279, 191, 279],   [71, 279, 71, 309],   [71, 309, 151, 309],
             [151, 309, 151, 409],  [151, 409, 271, 409], [271, 369, 271, 409],
             [271, 369, 321, 369],  [321, 369, 321, 439], [361, 369, 491, 369],
             [361, 369, 361, 459],  [361, 459, 388, 459], [388, 399, 388, 459],
             [388, 399, 461, 399],  [461, 399, 461, 449], [61, 9, 61, 99],
             [61, 99, 151, 99],     [151, 99, 151, 199],  [151, 199, 281, 199],
             [281, 199, 281, 279],  [281, 279, 321, 279], [401, 99, 491, 99],
             [401, 99, 401, 199],   [401, 199, 441, 199], [441, 149, 441, 199],
             [201, 9, 201, 99],     [181, 99, 201, 99],   [181, 99, 181, 149],
             [181, 149, 351, 149],  [351, 179, 351, 149], [11, 149, 61, 149],
             [61, 149, 61, 234],    [61, 234, 221, 234],  [221, 234, 221, 279],
             [441, 249, 491, 249],  [301, 9, 301, 69],    [251, 109, 331, 109],
             [331, 59, 331, 109],   [331, 59, 441, 59]]

    # extract each wall
    for wall in boundary:

        # get the---> start and end co-ordinates of every wall that is in the boundary
        x1_start, y1_start, x2_end, y2_end = wall

        # distance calculation
        # circle position---> line
        distance = dis_cirPoint_line(x, y, x1_start, y1_start, x2_end, y2_end)
        # If the distance is less than or equal to the radius of the ball, there is a collision
        if catcher_rad >= distance:
            return True

    # after getting done with checking---> give false
    return False


def dis_cirPoint_line(px, py, x1, y1, x2, y2):

    # get diffrences ---> line co-ordinate
    del_x_line = x2-x1
    del_y_line = y2-y1

    # get diffrences---> circle point and first co-ordinate of line
    x_axis_diff = px - x1
    y_axis_diff = py - y1

    # check---> line is a point
    if (del_x_line == 0) and (del_y_line == 0): # will fall at the same position

        # apply---> euclidean formula
        distance = math.sqrt(x_axis_diff**2 +  y_axis_diff** 2)

        return distance

    #line is certainly not a point
    else:
       # apply---> projection concept
       numer = x_axis_diff*del_x_line + y_axis_diff*del_y_line
       denomi = del_x_line**2 + del_y_line**2
       projec =  numer / denomi

       # limiting ---> within 0 to 1 range
       if projec < 0: # less than zero
          projec = 0
       elif projec > 1: # more than 1
          projec = 1

    # define closest point---> on the segment
    closest_x = x1 + projec * del_x_line
    closest_y = y1 + projec * del_y_line

    # apply---> euclidean formula
    # distance---> circle point and the closest point of the segment
    distance = math.sqrt((px - closest_x)**2 + (py - closest_y)**2)
    return distance


def display_obstackle(x, y):
    # define---> obstackle color
    clr = (0, 1, 0.5)

    # display---> circle part
    mpc(x, y, 7, clr)

    #  display---> teeth
    display_line(x - 8, y + 14, x, y + 22, clr)
    display_line(x, y + 8, x, y + 22, clr)
    display_line(x + 8, y + 14, x, y + 22, clr)


def display_left_arrow():
    #glColor3f(0.0, 1.0, 1.0)

    # assign---> blue color
    clr = (0, 0, 1) # shade of blue

    # define---> all three bars
    display_line(13, 573, 38, 598, clr)
    display_line(13, 573, 63, 573, clr)
    display_line(38, 548, 13, 573, clr)


def display_right_cross():
    #glColor3f(1.0, 0.0, 0.0)

    # assign---> red color
    clr = (1, 0, 0) # shade of red

    # define---> all two diagonal bars
    display_line(452, 552, 492, 592, clr)
    display_line(492, 552, 452, 592, clr)


def display_pause_bar():
    #glColor3f(1.0, 1.0, 0.0)

    # assign---> yellow color
    clr = (1, 1, 0) # shade of yellow

    # define---> all two parallel bars
    display_line(247, 592, 247, 552, clr)
    display_line(257, 552, 257, 592, clr)


def display_triangle():
    #glColor3f(1.0, 1.0, 0.0)

    # assign---> yellow color
    clr = (1, 1, 0) # shade of yellow

    # define---> triangle bars
    display_line(237, 552, 237, 592, clr)
    display_line(237, 592, 277, 572, clr)
    display_line(237, 552, 277, 572, clr)


def showScreen():
    # necessary calls
    global score, is_game_pause, left_time, level
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0)


    # assign---> maze boundary
    boundary = [ [11, 489, 491, 489],   [11, 9, 491, 9],      [11, 9, 11, 489],
             [491, 9, 491, 489],    [91, 489, 91, 419],   [296, 489, 296, 419],
             [421, 489, 421, 439],  [11, 349, 126, 349],  [126, 349, 126, 449],
             [251, 319, 251, 369],  [191, 319, 351, 319], [351, 219, 351, 319],
             [351, 269, 391, 269],  [391, 269, 391, 329], [191, 279, 191, 319],
             [71, 279, 191, 279],   [71, 279, 71, 309],   [71, 309, 151, 309],
             [151, 309, 151, 409],  [151, 409, 271, 409], [271, 369, 271, 409],
             [271, 369, 321, 369],  [321, 369, 321, 439], [361, 369, 491, 369],
             [361, 369, 361, 459],  [361, 459, 388, 459], [388, 399, 388, 459],
             [388, 399, 461, 399],  [461, 399, 461, 449], [61, 9, 61, 99],
             [61, 99, 151, 99],     [151, 99, 151, 199],  [151, 199, 281, 199],
             [281, 199, 281, 279],  [281, 279, 321, 279], [401, 99, 491, 99],
             [401, 99, 401, 199],   [401, 199, 441, 199], [441, 149, 441, 199],
             [201, 9, 201, 99],     [181, 99, 201, 99],   [181, 99, 181, 149],
             [181, 149, 351, 149],  [351, 179, 351, 149], [11, 149, 61, 149],
             [61, 149, 61, 234],    [61, 234, 221, 234],  [221, 234, 221, 279],
             [441, 249, 491, 249],  [301, 9, 301, 69],    [251, 109, 331, 109],
             [331, 59, 331, 109],   [331, 59, 441, 59]]

    # maze formation
    for wall in boundary: # extract---> all the wall one by one
        # get the co-ordinates---> of each wall
        x1_wall, y1_wall, x2_wall, y2_wall = wall

        # assign---> color
        clr = [0.5, 0.5, 1] # maze color

        # build wall's
        display_line(x1_wall, y1_wall, x2_wall, y2_wall, clr)

    glColor3f(1.0, 0.0, 0.0)  # Red color for the ball
    mpc(catcher_pos_x, catcher_pos_y, catcher_rad, [1.0, 0.0, 0.0])
    display_left_arrow()
    display_right_cross()

    if is_game_pause:
        display_triangle()
    else:
        display_pause_bar()

    # Draw keys
    for key_pos in obstackle_lst:
        key_x, key_y = key_pos
        display_obstackle(key_x, key_y)

    # Check collision with the keys
    for key_pos in obstackle_lst:
        key_x, key_y = key_pos
        if abs(catcher_pos_x - key_x) <= catcher_speed and abs(catcher_pos_y - key_y) <= catcher_speed:
            score += 1
            print("Score:", score)
            obstackle_lst.remove(key_pos)  # Remove the key from the list when touched by the ball


    # construct---> score counter
    score_text = f"Score: {score}" # format
    glColor3f(0.5, 1, 0.9) # paste color
    glRasterPos2f(380, 500) # display poition
    # display one character at a time
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))

    # construct---> level counter
    level_text = f"Level: {level}" # format
    glColor3f(0.95, 0.95, 0.90) # pearl color
    glRasterPos2f(380, 520) # display poition
    # display one character at a time
    for char in level_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))

    # construct---> difficulty status
    dif_text = f"Difficulty: {difficulty_status[level]}" # select---> level wise
    glColor3f(0.95, 0.95, 0.90) # pearl color
    glRasterPos2f(8, 500) # display poition
    # display one character at a time
    for char in dif_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))

    # construct---> time counter
    time_left_text = f"Time left: {left_time} seconds" # format
    glColor3f(1, 0.4, 1) # purple color
    glRasterPos2f(8, 520) # display poition

    for char in time_left_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))

    # case---> game win
    if len(obstackle_lst) == 0: # it has to be zero
        game_win_text = "Game win, Hurray!"
        glColor3f(1.0, 1.0, 0.0)  # Yellow color for game win text
        glRasterPos2f(225, 520)  # Position to display game win text
        # display one character at a time
        for char in game_win_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))

        # will shift---> to next level
        level += 1 # inc by one
        shift_level()

        # Stop the timer
        #glutTimerFunc(0, timer, 0)

    # case---> game over
    elif left_time == 0:
        game_over_text = "Game over!"
        glColor3f(1.0, 0.0, 0.0)  # Red color for game over text
        glRasterPos2f(225, 520)  # Position to display game over text #yo
        # display one character at a time
        for char in game_over_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(char)))

        # Stop the timer
        #glutTimerFunc(0, timer, 0)

    glutSwapBuffers()


def keyboard_listner(key, x, y): #
    global catcher_pos_x, catcher_pos_y, is_game_pause

    if key == b'\x1b':  # Escape key (ASCII value for escape)
        sys.exit(0)

    # Move up
    if is_game_pause == False:
        if key == b'w':
            updated_y = catcher_pos_y+catcher_speed
            temp = collide(catcher_pos_x, updated_y, 0, catcher_speed)
            if temp == False : # doesn't colide
                catcher_pos_y = updated_y  # update

        # Move down
        elif key == b's':
            updated_y = catcher_pos_y - catcher_speed
            temp = collide(catcher_pos_x, updated_y, 0, -catcher_speed)
            if temp == False :# doesn't colide
                catcher_pos_y = updated_y  # update

        # Move left
        elif key == b'a':
            updated_x = catcher_pos_x - catcher_speed
            temp = collide(updated_x, catcher_pos_y, -catcher_speed, 0)
            if temp == False :# doesn't colide
                catcher_pos_x = updated_x  # update

        # Move right
        elif key == b'd':
            updated_x = catcher_pos_x + catcher_speed
            temp = collide(updated_x, catcher_pos_y, catcher_speed, 0)
            if temp == False :# doesn't colide
                catcher_pos_x = updated_x  # update

    glutPostRedisplay()


def restartGame():
    global catcher_rad, catcher_speed, catcher_pos_x, catcher_pos_y, score, obstackle_lst
    global total_time, left_time, game_play, is_game_pause, game_over

    # catcher initial positions
    catcher_pos_x, catcher_pos_y = 35, 456

    # catcher size
    catcher_rad = 8

    # catcher movement speed
    catcher_speed = 12 # max limit 10

    # catcher points
    score = 0

    # Keeps track of the level
    # level = 1

    # define obstackle---> initial posiyions
    obst_one_pos =  (250, 250)
    obst_two_pos =  (30, 40)
    obst_three_pos =  (450, 450)

    # Store Obstackle---> in a list
    obstackle_lst = [obst_one_pos, obst_two_pos, obst_three_pos]

    # initial game status---> False
    game_play, game_over, is_game_pause = False, False, False

    # allocate---> initial time frame
    # initially entire time left
    total_time, left_time = 60, 60 # in second's

    print("Let's start again!")
    glutPostRedisplay()


def shift_level():

    global catcher_rad, catcher_speed, catcher_pos_x, catcher_pos_y, score, obstackle_lst
    global total_time, left_time, game_play, is_game_pause, game_over

    # catcher initial positions
    catcher_pos_x, catcher_pos_y = 35, 456

    # catcher size
    catcher_rad = 8

    # level wise---> updates
    if level == 1:
        catcher_speed = 12

        # define obstackle---> initial posiyions
        obst_one_pos =  (250, 250)
        obst_two_pos =  (30, 40)
        obst_three_pos =  (450, 450)

        # Store Obstackle---> in a list
        obstackle_lst = [obst_one_pos, obst_two_pos, obst_three_pos]

    elif level == 2:
        catcher_speed = 8 # previously it was 12

        # define obstackle---> initial posiyions
        obst_one_pos =  (90, 250)
        obst_two_pos =  (420, 175)
        obst_three_pos =  (372, 435)

        # Store Obstackle---> in a list
        obstackle_lst = [obst_one_pos, obst_two_pos, obst_three_pos]

        total_time, left_time = 45, 45 # 15 sec reduction

    elif level == 3:
        catcher_speed = 4 # previously it was 8

        # define obstackle---> initial posiyions
        obst_one_pos =  (35, 456)
        obst_two_pos =  (30, 40)
        obst_three_pos =  (372, 435)

        # Store Obstackle---> in a list
        obstackle_lst = [obst_one_pos, obst_two_pos, obst_three_pos]

        catcher_pos_x, catcher_pos_y = 250, 270
        total_time, left_time = 30, 30 # 20 sec reduction

    # catcher points
    score = 0

    # initial game status---> False
    game_play, game_over, is_game_pause = False, False, False

    print("Let's start again!")
    glutPostRedisplay()

def mouse_listner(button, state, x, y): #
    global is_game_pause, game_over, printed, score, game_play

    # GLUT_DOWN---> pressed down the button


    # case---> restart game
    if (button == GLUT_LEFT_BUTTON) and (state == GLUT_DOWN):

        # cursor---> region check
        if (10 <= x <= 70) and (30 <= y <= 70):
            is_game_pause = False
            if game_over == False :
                print(f"Game Over! Score: {score}")
            restartGame()
            print("Starting Over!")

        # cursor---> region check
        if (420 <= x <= 490) and (20 <= y <= 80):
            printed = True
            print("Goodbye")
            print(f"Score: {score}")
            game_over = True
            glutLeaveMainLoop()

        # cursor---> region check
        if (245 <= x <= 255) and (25 <= y <= 65):
            # invert the status
            is_game_pause = not is_game_pause
            # pause
            if is_game_pause == True:
                game_play = False
                print("Game Paused")
            # play
            else:
                game_play = True
                print("Game Resumed")
            glutPostRedisplay()

        print(f"Mouse clicked at ({x}, {y})")
        # glutPostRedisplay()


def timer(value):
    global left_time, is_game_pause

    # debugg---> purpose
    print(f"Game paused:  {is_game_pause}")
    print(f"Timer:  {left_time}")

    # game is ----> active
    if is_game_pause == False:
        # call timer--->after 1 sec, for 1000 milisec times
        glutTimerFunc(1000, timer, 0)

        # debugg---> purpose
        print("Time remaining:", left_time)

        # decr---> left time by 1 sec
        if left_time > 0: # didn't reach the end yet
            left_time -= 1
        else: # reached the end
            print("Time's up!")
            glutLeaveMainLoop() # take an exit

        glutPostRedisplay()

    # game is ----> inactive
    else:
        glutTimerFunc(0, timer, 0)

#===================================="DRIVER_CODE"====================================
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 600)  # window size
glutInitWindowPosition(200, 200)
wind = glutCreateWindow(b"OpenGL Coding Practice")  # window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard_listner)
glutMouseFunc(mouse_listner)
glutTimerFunc(1000, timer, 0)
glutMainLoop()
