import turtle
import math

def draw_koch_edge(t, length, depth):
    if depth == 0:
        t.forward(length)
        return

    segment = length / 3

    # Drawing first segment
    draw_koch_edge(t, segment, depth - 1)

    # Turn inward (right 60°) to create indentation
    t.right(60)
    draw_koch_edge(t, segment, depth - 1)

    # Turn left 120° to complete the indentation triangle
    t.left(120)
    draw_koch_edge(t, segment, depth - 1)

    # Turn right 60° to realign
    t.right(60)
    draw_koch_edge(t, segment, depth - 1)

def draw_polygon(t, sides, length, depth):
    angle = 360 / sides
    for _ in range(sides):
        draw_koch_edge(t, length, depth)
        t.right(angle)

def main():
    # Getting user's input
    while True:
        try:
            sides = int(input("Enter the number of sides of the polygon (>=3): "))
            if sides < 3:
                print("Number of sides must be at least 3.")
                continue
            length = float(input("Enter the length of each side (positive number): "))
            if length <= 0:
                print("Length must be positive.")
                continue
            depth = int(input("Enter the recursion depth (>=0): "))
            if depth < 0:
                print("Depth must be zero or positive.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter numeric values.")

    # Settingup turtle
    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()

    # Position turtle to start drawing centered
    # Calculating radius of circumcircle to center the polygon
    radius = length / (2 * math.sin(math.pi / sides))
    t.penup()
    t.goto(-radius, radius / 2)
    t.pendown()

    # Drawing the Koch anti-snowflake polygon
    draw_polygon(t, sides, length, depth)

    screen.mainloop()

if __name__ == "__main__":
    main()

