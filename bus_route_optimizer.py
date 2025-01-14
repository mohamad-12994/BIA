import numpy as np
import random
import matplotlib.pyplot as plt

# فرضية: لدينا 10 محطات لحافلة مدرسية
num_stations = 10
distances = np.random.randint(1, 100, size=(num_stations, num_stations))
safe_routes = np.random.randint(0, 2, size=(num_stations, num_stations))  # الطرق الآمنة (0 غير آمنة، 1 آمنة)

# دالة لحساب طول المسار
def calculate_route_length(route):
    length = 0
    for i in range(len(route) - 1):
        length += distances[route[i], route[i + 1]]
    return length

# دالة لحساب مدى الأمان للمسار
def calculate_route_safety(route):
    safety = 0
    for i in range(len(route) - 1):
        safety += safe_routes[route[i], route[i + 1]]
    return safety

# تهيئة الخوارزمية الجينية
def genetic_algorithm(num_generations, population_size):
    population = [random.sample(range(num_stations), num_stations) for _ in range(population_size)]
    
    for generation in range(num_generations):
        population = sorted(population, key=lambda route: (calculate_route_length(route), -calculate_route_safety(route)))
        
        selected_population = population[:population_size // 2]
        
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            crossover_point = random.randint(1, num_stations - 1)
            
            child = parent1[:crossover_point] + [x for x in parent2 if x not in parent1[:crossover_point]]
            if random.random() < 0.1:
                swap_idx = random.sample(range(num_stations), 2)
                child[swap_idx[0]], child[swap_idx[1]] = child[swap_idx[1]], child[swap_idx[0]]
            
            new_population.append(child)
        
        population = new_population
    
    return population[0]

# تجربة الكود
best_route = genetic_algorithm(num_generations=100, population_size=20)
print("أفضل مسار:", best_route)
print("طول المسار:", calculate_route_length(best_route))
print("مدى الأمان:", calculate_route_safety(best_route))
