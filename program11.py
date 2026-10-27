import turtle

def draw_koch_segment(t, length, depth):
    """
    Recursively draws a single line segment of a Koch snowflake using directional movements.
    
    Args:
        t (turtle.Turtle): The turtle pen instance.
        length (float): The length of the current fractal segment.
        depth (int): The recursion depth for the fractal.
    """
    # Base case: draw a straight line when depth reaches 0
    if depth == 0:
        t.forward(length)
    else:
        # Recursive case: divide the segment into 3 parts and create the peak
        length /= 3.0
        draw_koch_segment(t, length, depth - 1)
        t.left(60)
        draw_koch_segment(t, length, depth - 1)
        t.right(120)
        draw_koch_segment(t, length, depth - 1)
        t.left(60)
        draw_koch_segment(t, length, depth - 1)

def draw_koch_snowflake(t, length, depth):
    """
    Draws a complete Koch snowflake fractal by rendering three connecting segments.
    
    Args:
        t (turtle.Turtle): The turtle pen instance.
        length (float): The total length of one side of the snowflake.
        depth (int): The recursion depth for the fractal.
    """
    for _ in range(3):
        draw_koch_segment(t, length, depth)
        t.right(120)

def main():
    """
    Main execution function that configures the screen parameters, dynamic RGB 
    background fills, and custom drawing pens to render the geometric pattern.
    """
    # Configure user-defined screen parameters
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    screen.title("Interactive Turtle Pattern Generator and Fractal Renderer")
    
    # Configure dynamic RGB background fills using 255 color mode
    turtle.colormode(255)
    screen.bgcolor(20, 30, 60)  # Dark navy blue background
    
    # Configure the custom drawing pen
    pen = turtle.Turtle()
    pen.speed(0)                # Set to maximum speed for fast rendering
    pen.color(0, 255, 200)      # Bright cyan pen color using RGB
    pen.pensize(2)              # Set stroke thickness
    
    # Apply directional movements to center the starting point of the fractal
    pen.penup()
    pen.goto(-150, 100)
    pen.pendown()
    
    # Render the recursive fractal pattern (Koch snowflake)
    draw_koch_snowflake(pen, length=300, depth=3)
    
    # Hide the turtle cursor and wait for user to close the window
    pen.hideturtle()
    screen.mainloop()

if __name__ == "__main__":
    main()