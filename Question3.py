import turtle

# Recommended ranges to avoid very slow or broken drawings
RECOMMENDED_SIDES = (3, 12)
RECOMMENDED_LENGTH = (50, 500)
RECOMMENDED_DEPTH = (0, 6)

def draw_koch_edge(t, length, depth):
    """Draw one edge of the Koch pattern recursively."""
    if depth == 0:
        t.forward(length)
        return
    
    segment = length / 3
    draw_koch_edge(t, segment, depth - 1)
    t.right(60)
    draw_koch_edge(t, segment, depth - 1)
    t.left(120)
    draw_koch_edge(t, segment, depth - 1)
    t.right(60)
    draw_koch_edge(t, segment, depth - 1)

def draw_polygon(t, sides, length, depth):
    """Draw the starting polygon and apply the Koch pattern to each side."""
    angle = 360 / sides
    for _ in range(sides):
        draw_koch_edge(t, length, depth)
        t.right(angle)

def get_input(prompt, cast_func, name, safe_range, min_allowed):
    """
    Get user input with basic validation.
    If the value is outside the recommended range, warn once
    and allow the user to re-enter. If still outside, proceed anyway.
    """
    while True:
        try:
            value = cast_func(input(prompt))
            if value < min_allowed:
                print(f"{name} must be at least {min_allowed}. Try again.")
                continue

            low, high = safe_range
            if value < low or value > high:
                print(f"Warning: {name} = {value} is outside the recommended range "
                      f"({low}–{high}).")
                retry = cast_func(input(f"Re-enter {name}: "))
                if retry < min_allowed:
                    print(f"{name} must be at least {min_allowed}. Using {value} 😊")
                    return value
                if retry < low or retry > high:
                    print(f"Proceeding with {retry} 😊")
                return retry
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    # Collect parameters from the user
    sides = get_input("Enter the number of sides of the polygon (>=3): ",
                      int, "Number of sides", RECOMMENDED_SIDES, 3)
    length = get_input("Enter the length of each side (positive number): ",
                       float, "Side length", RECOMMENDED_LENGTH, 1)
    depth = get_input("Enter the recursion depth (>=0): ",
                      int, "Recursion depth", RECOMMENDED_DEPTH, 0)

    # Set up turtle screen
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.tracer(0)  # Disable animation for faster drawing

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()

    # Move to a better starting position
    t.penup()
    t.goto(-length / 2, -length / 2)
    t.pendown()

    # Draw the polygon with fractal edges
    draw_polygon(t, sides, length, depth)

    screen.update()
    turtle.done()

if __name__ == "__main__":
    main()
