import random
from math import sin, cos, pi, log
from tkinter import *

# Canvas dimensions
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11  # Scaling factor for heart shape
HEART_COLOR = "#e77c8e"  

def center_Window(root, width, height):
    # Centers window on screen.
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height)/ 2)
    root.geometry(size)

def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    #Defines parametric function for heart shape
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2*t) - 2 * cos(3*t) - cos(4*t))
    x *= shrink_ratio
    y *= shrink_ratio
    x += CANVAS_CENTER_X  
    y += CANVAS_CENTER_Y
    return int(x), int(y)

def scatter_inside(x, y, beta=0.15):
    #Creates scattered effect inside
    ratio_x = -beta * log(random.random()) 
    ratio_y = -beta * log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def shrink(x, y, ratio):
    #Shrinks heart shape with force-based effect
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def curve(p):
    #Smooth pulsating effect for the heart animation
    return 2 * (2 * sin(4 * p)) / (2 * pi)

class Heart:
    #class representing heart shape with animation effects
    def __init__(self, generate_frame=20):
        self._points = set() 
        self._edge_diffusion_points = set()  
        self._center_diffusion_points = set()  
        self.all_points = {}  
        self.build(2000)  
        self.random_halo = 1000  
        self.generate_frame = generate_frame  
        for frame in range(generate_frame):
            self.calc(frame)  

    def build(self, number):
        #Builds heart shape with diffusion effects
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y)) 

        # Create scattered points around edges
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))

        # Create scattered points inside the heart
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        #Calculates new positions for animation effects
        force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        #Precomputes positions for each animation frame.
        ratio = 10 * curve(generate_frame / 10 * pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))
        all_points = []

        # Generate glowing effect (halo) around heart
        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=11.6)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        # Add main heart points with animation effect
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        # Add scattered edge points
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        # Add scattered center points
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points  # Store points for this frame

    def render(self, render_canvas, render_frame):
        #Draws heart on canvas for given frame
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)

def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    #Recursive function to update animation
    render_canvas.delete('all')  
    render_heart.render(render_canvas, render_frame) 
    main.after(160, draw, main, render_canvas, render_heart, render_frame + 1)  
    
if __name__ == '__main__':
    # Initialize Tkinter window
    root = Tk()
    root.title = ("LOVE")
    center_Window(root, CANVAS_WIDTH, CANVAS_HEIGHT)  # Center window on screen

    # Create canvas for drawing
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()

    # Create heart object and start animation
    heart = Heart()
    draw(root, canvas, heart)

    # Display message
    Label(root, text="Happy Valentine's Day!\nLOVE YOU", bg="black", fg="#e77c8e", font="Helvetica 15 bold").place(
        relx=.5, rely=.5, anchor=CENTER
    )

    root.mainloop()  # Run Tkinter event loop
