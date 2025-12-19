import math
import random

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement

# === Provided class Position
class Position(object):
    def __init__(self:Position, x:float, y:float) -> None:
        self.x = x
        self.y = y
        
    def get_x(self:Position) -> float:
        return self.x
    
    def get_y(self:Position) -> float:
        return self.y
    
    def get_new_position(self:Position, angle:float, speed:float) -> Position:
        old_x:float = self.get_x() 
        old_y:float = self.get_y()

        delta_y:float = speed * math.cos(math.radians(angle))
        delta_x:float = speed * math.sin(math.radians(angle))
    
        new_x:float = old_x + delta_x
        new_y:float = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self:Position) -> str:  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))

class RectangularRoom(object):
    def __init__(self:RectangularRoom, width:int, height:int, dirt_amount:int) -> None:
        self.width:int = width
        self.height:int = height
        self.dirt_amount:int = dirt_amount
        self.tiles:dict[tuple[int],int] = {}
        for i in range(width):
            for j in range(height):
                self.tiles[(i,j)] = dirt_amount
    
    def clean_tile_at_position(self:RectangularRoom, pos:Position, capacity:int) -> None:
        key = (int(pos.get_x()),int(pos.get_y()))
        self.tiles[key] -= capacity
        if self.tiles[key] < 0:
            self.tiles[key] = 0

    def is_tile_cleaned(self:RectangularRoom, m:int, n:int) -> bool:
        return self.tiles[(m,n)] == 0

    def get_num_cleaned_tiles(self:RectangularRoom) -> int:
        return sum([1 for x in self.tiles.values() if x == 0])
        
    def is_position_in_room(self:RectangularRoom, pos:Position) -> bool:
        return (math.floor(pos.get_x()),math.floor(pos.get_y())) in self.tiles
        
    def get_dirt_amount(self:RectangularRoom, m:int, n:int) -> int:
        return self.tiles[(m,n)]
        
    def get_num_tiles(self:RectangularRoom) -> int:
        # do not change -- implement in subclasses
        raise NotImplementedError   
        
    def is_position_valid(self:RectangularRoom, pos:Position) -> bool:
        # do not change -- implement in subclasses
        raise NotImplementedError   
    
    def get_random_position(self:RectangularRoom) -> Position:
        # do not change -- implement in subclasses
        raise NotImplementedError        

class Robot(object):
    def __init__(self:Robot, room:RectangularRoom, speed:float, capacity:int) -> None:
        self.room:RectangularRoom = room
        self.speed:float = speed
        self.capacity:int = capacity
        self.direction:float = random.random() * 360
        self.position:Position = self.room.get_random_position()

    def get_robot_position(self:Robot) -> Position:
        return self.position

    def get_robot_direction(self:Robot) -> float:
        return self.direction

    def set_robot_position(self:Robot, position:Position) -> None:
        self.position:Position = position

    def set_robot_direction(self:Robot, direction:float) -> None:
        self.direction:float = direction

    def update_position_and_clean(self:Robot) -> None:
        # do not change -- implement in subclasses
        raise NotImplementedError

class EmptyRoom(RectangularRoom):
    def get_num_tiles(self:EmptyRoom) -> int:
        return len(self.tiles)
        
    def is_position_valid(self:EmptyRoom, pos:Position) -> bool:
        return self.is_position_in_room(pos)
        
    def get_random_position(self:EmptyRoom) -> Position:
        return Position(random.random() * self.width, random.random() * self.height)

class FurnishedRoom(RectangularRoom):
    def __init__(self:FurnishedRoom, width:int, height:int, dirt_amount:int) -> None:
        RectangularRoom.__init__(self, width, height, dirt_amount)
        self.furniture_tiles:list[tuple[int]] = []
        
    def add_furniture_to_room(self:FurnishedRoom) -> None:
        furniture_width:int = random.randint(1, self.width - 1)
        furniture_height:int = random.randint(1, self.height - 1)
 
        f_bottom_left_x:int = random.randint(0, self.width - furniture_width)
        f_bottom_left_y:int = random.randint(0, self.height - furniture_height)

        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self:FurnishedRoom, m:int, n:int) -> bool:
        return (m,n) in self.furniture_tiles
        
    def is_position_furnished(self:FurnishedRoom, pos:Position) -> bool:
        return self.is_tile_furnished(int(pos.get_x()),int(pos.get_y()))
        
    def is_position_valid(self:FurnishedRoom, pos:Position) -> bool:
        return self.is_position_in_room(pos) and not self.is_position_furnished(pos)
        
    def get_num_tiles(self:FurnishedRoom) -> int:
        return len(self.tiles) - len(self.furniture_tiles)
        
    def get_random_position(self:FurnishedRoom) -> Position:
        position:Position = Position(random.random() * self.width, random.random() * self.height)
        while not self.is_position_valid(position):
            position = Position(random.random() * self.width, random.random() * self.height)
        return position

class StandardRobot(Robot):
    def update_position_and_clean(self:StandardRobot) -> None:
        self.room.clean_tile_at_position(self.get_robot_position(), self.capacity)
        position:Position = self.get_robot_position().get_new_position(self.get_robot_direction(), self.speed)
        if not self.room.is_position_valid(position):
            self.set_robot_direction(random.random() * 360)
        else:
            self.set_robot_position(position)

# test_robot_movement(StandardRobot, EmptyRoom)
# test_robot_movement(StandardRobot, FurnishedRoom)

class FaultyRobot(Robot):
    p:float = 0.15

    @staticmethod
    def set_faulty_probability(prob:float) -> None:
        FaultyRobot.p = prob
    
    def gets_faulty(self:FaultyRobot) -> bool:
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        if self.gets_faulty():
            self.set_robot_direction(random.random() * 360)
        else:
            self.room.clean_tile_at_position(self.get_robot_position(), self.capacity)
            position:Position = self.get_robot_position().get_new_position(self.get_robot_direction(), self.speed)
            if not self.room.is_position_valid(position):
                self.set_robot_direction(random.random() * 360)
            else:
                self.set_robot_position(position)    
    
# test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
def run_simulation(num_robots:int, speed:float, capacity:int, width:int, 
                   height:int, dirt_amount:int, min_coverage:float, 
                   num_trials:int,robot_type:type[Robot]) -> float:
    times:list[int] = []
    for i in range(num_trials):
        room:RectangularRoom = EmptyRoom(width, height, dirt_amount)
        robots:list[Robot] = [robot_type(room, speed, capacity) for _ in range(num_robots)]
        time_steps:int = 0
        while room.get_num_cleaned_tiles() / room.get_num_tiles() < min_coverage:
            for robot in robots:
                robot.update_position_and_clean()
            time_steps += 1
        times.append(time_steps)
    return sum(times) / len(times)

# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

def show_plot_compare_strategies(title, x_label, y_label):
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


# show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
# show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
