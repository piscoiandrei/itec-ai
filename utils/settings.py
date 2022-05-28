# generation settings
zone = 10
TRIANGLE = "triangle"
RECTANGLE = "rectangle"
ELLIPSE = "ellipse"
SEQ_SIZE = 100  # how many of each shape to generate in a process
NUM_PROCESSES = 30
SHAPES = [TRIANGLE, RECTANGLE, ELLIPSE]
COLORS = {
    "red": "#ff0000",
    "green": "#00ff00",
    "blue": "#0000ff"
}
SHAPE_CODES = {
    TRIANGLE: 0,
    ELLIPSE: 1,
    RECTANGLE: 2
}
COLOR_CODES = {
    "red": 0,
    "green": 1,
    "blue": 2
}
SIZE = 96
TOTAL_AREA = SIZE ** 2
