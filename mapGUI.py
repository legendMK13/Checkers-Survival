import tkinter as tk

#GUI Map Definition - Enlarged Map and Mini-Map

#The Mini-Map will be displayed at bottom-left of UI during normal gameplay
#Enlarged Map displayed upon user input

#note that mini-map has not yet been implemented

#Key Variables and Rules Used to Display Enlarged Map (only):
#   each room takes maximum of 80x80 including paths in all directions
#
#   the 'pivot' is the room most likely to be at center of the map
#       it is first obtained to ensure building the map is efficient,
#       and that the map appear at the center of the window
#
#   'location' is the room the player is located in. In both maps it will be
#       highlighted when printed
#
#   coordinates eg canvas.create_line(x, y, x, y) are:
#       X-start, Y-start, X-end, Y-end where X is x distance from top-right
#       corner of window, and Y is y distance (increases downwards) from
#       top-right corner
#
#             ****************Most Important Below****************
#   those coordinates point to the position in the window the CENTER of a
#       room will be printed.


def locate_pivot(level):
    #Pivot is the room which is most likely to be at center of the map
    #
    #Makes it quicker to display map, and allows map to be at center of window
    #   if the pivot is printed at very center of window.
    
    #Concept to find pivot:
    #   Get the rooms with most connections to other rooms eg all 4 paths
    #      connect to another room. Keep these in 'prospects[]'
    #   Of those in prospects[], select the one with most connections 'pts'
    #       to other rooms in prospects[] (rooms with most connections)
    #   The one with the highest pts is the pivot
    
    prospects = [] #rooms most likely  to be the ideal pivot.
    flag = False
    i = 0
    while flag == False:
        flag = False
        for room in level:
            if len(room.get_empty_paths()) == i:
                prospects.append(room)
                flag = True
        if flag == False: #keep adding i so if all rooms dont have 4 connects
                            #then check for those that have 3
            i+=1
        if i == 5: #just 1 room in the level
            return room
    pivot = prospects[0]
    highest_pts = 0
    for room in prospects:
        pts = 0
        paths = room.get_existing_paths()
        for path in paths:
            if room.get_adjacent_room(path) in prospects:
                pts+=1
        if pts > highest_pts:
            highest_pts = pts
            pivot = room
    return pivot

def nxt_room_position(direction, x, y):
    #Given each room occupies a certain amount of space, this gives the
    #   position where the CENTER of the next room should be printed.
    if direction == 'N':
        return [x, y-60] #Up
    elif direction == 'S':
        return [x, y+60] #Down
    elif direction == 'E':
        return [x+60, y] #Right
    elif direction == 'W':
        return [x-60, y] #Left

def display_path(canvas, direction, x, y):
    #Direction is the direction of the line representing a path
    if direction == 'N':
        canvas.create_line(x, y-21, x, y-39) #Up
    elif direction == 'S':
        canvas.create_line(x, y+21, x, y+39) #Down
    elif direction == 'E':
        canvas.create_line(x+21, y, x+39, y) #Right
    elif direction == 'W':
        canvas.create_line(x-21, y, x-39, y) #Left

def display_room(canvas, x, y, flag=False):
    #Prints a room onto window. Takes its center and prints it according to
    #   standard boundaries

    #Flag is True if player is in that room.    
    #Remember x and y are mark the center of the room shape
    if flag == False:
        canvas.create_rectangle(x-20, y-20, x+20, y+20, outline="#fb0",
                                fill="#000")
    else:
        canvas.create_rectangle(x-20, y-20, x+20, y+20, outline="#fb0",
                                fill="#fb0")

def display_level(canvas, room, location, x, y, prev_dir=None):
    #room is the current room being examined to be printed
    #x and y are mark the center of the room shape
    if room == location:
        display_room(canvas, x, y, True)
    else:
        display_room(canvas, x, y, False)
    paths = room.get_existing_paths()
    if prev_dir != None:
        opposite_dir = {
            'N': 'S',
            'S': 'N',
            'E': 'W',
            'W': 'E'
        }
        paths.remove(opposite_dir[prev_dir])
    for path in paths:
        display_path(canvas, path, x, y)
        next_position = nxt_room_position(path, x, y)
        display_level(canvas, room.get_adjacent_room(path), location, 
                      next_position[0], next_position[1], path)
    print('HERE')
    return

def start_small_map_IO(location):
    #location is the player's current location (room)
    return

def start_large_map_IO(level, location):
    #Defines the Enlarged Map Window and Creates the Canvas to generate map
    root = tk.Tk(className=" Map")
    root.geometry("1080x680")
    canvas = tk.Canvas(root, width=1040, height=610)
    
    vert_scroll = tk.Scrollbar(root, orient='vertical')
    vert_scroll.pack(side='right', fill='y')
    hori_scroll = tk.Scrollbar(root, orient='horizontal')
    hori_scroll.pack(side='bottom', fill='x')
    
    #Print pivot first at CENTER of window, then display the rest
    pivot = locate_pivot(level)
    x = 525 #center of the screen on x-axis
    y = 305 #center of the screen on y-axis
    display_level(canvas, pivot, location, x, y)
    canvas.pack()
    
    returnButton = tk.Button(root, text="OK", padx=50, command=root.destroy)
    returnButton.pack(side='bottom')
    root.mainloop()