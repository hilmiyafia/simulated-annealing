import numpy
import cv2

def Generate(width, height, count):
    cities = []
    for i in range(count):
        position_x = numpy.random.randint(width)
        position_y = numpy.random.randint(height)
        cities.append((position_x, position_y))
    return cities

def Initialize(count):
    solution = numpy.arange(count)
    numpy.random.shuffle(solution)
    return solution

def Evaluate(cities, solution):
    distance = 0
    for i in range(len(cities)):
        index_a = solution[i]
        index_b = solution[i - 1]
        delta_x = cities[index_a][0] - cities[index_b][0]
        delta_y = cities[index_a][1] - cities[index_b][1]
        distance += (delta_x ** 2 + delta_y ** 2) ** 0.5
    return distance

def Modify(current):
    new = current.copy()
    index_a = numpy.random.randint(len(current))
    index_b = numpy.random.randint(len(current))
    while index_b == index_a:
        index_b = numpy.random.randint(len(current))
    new[index_a], new[index_b] = new[index_b], new[index_a]
    return new

def Draw(width, height, cities, solution, infos):
    frame = numpy.zeros((height, width, 3))
    for i in range(len(cities)):
        index_a = solution[i]
        index_b = solution[i - 1]
        point_a = (cities[index_a][0], cities[index_a][1])
        point_b = (cities[index_b][0], cities[index_b][1])
        cv2.line(frame, point_a, point_b, GREEN, 2)
    for city in cities:
        cv2.circle(frame, (city[0], city[1]), 5, RED, -1)
    cv2.putText(frame, f"Temperature", (25, 50), FONT, SIZE, WHITE)
    cv2.putText(frame, f"Score", (25, 75), FONT, SIZE, WHITE)
    cv2.putText(frame, f"Best Score", (25, 100), FONT, SIZE, WHITE)
    cv2.putText(frame, f"Worst Score", (25, 125), FONT, SIZE, WHITE)
    cv2.putText(frame, f": {infos[0]:.2f}", (175, 50), FONT, SIZE, WHITE)
    cv2.putText(frame, f": {infos[1]:.2f}", (175, 75), FONT, SIZE, WHITE)
    cv2.putText(frame, f": {infos[2]:.2f}", (175, 100), FONT, SIZE, WHITE)
    cv2.putText(frame, f": {infos[3]:.2f}", (175, 125), FONT, SIZE, WHITE)
    cv2.imshow("Simulated Annealing", frame)
    cv2.waitKey(5)
    
WIDTH = 640
HEIGHT = 480
CITY_COUNT = 20
INITIAL_TEMPERATURE = 1000
STOPPING_TEMPERATURE = 1
TEMPERATURE_DECAY = 0.999
FONT = cv2.FONT_HERSHEY_DUPLEX
SIZE = 0.7
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

if __name__ == "__main__":
    cities = Generate(WIDTH, HEIGHT, CITY_COUNT)
    current_solution = Initialize(CITY_COUNT)
    current_score = Evaluate(cities, current_solution)
    best_score = worst_score = current_score
    temperature = INITIAL_TEMPERATURE
    while (temperature > STOPPING_TEMPERATURE):
        new_solution = Modify(current_solution)
        new_score = Evaluate(cities, new_solution)
        best_score = min(best_score, new_score)
        worst_score = max(worst_score, new_score)
        if new_score < current_score:
            current_solution = new_solution
            current_score = new_score
        else:
            delta = new_score - current_score
            probability = numpy.exp(-delta / temperature)
            if probability > numpy.random.uniform():
                current_solution = new_solution
                current_score = new_score
        temperature *= TEMPERATURE_DECAY
        infos = (temperature, current_score, best_score, worst_score)
        Draw(WIDTH, HEIGHT, cities, current_solution, infos)
