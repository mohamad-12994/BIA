from django.shortcuts import render, redirect
from .forms import StationForm
import numpy as np
import random

stations = []  # تخزين المحطات في متحول مؤقت

def home(request):
    global stations
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            station_data = form.cleaned_data
            latitude = station_data['latitude']
            longitude = station_data['longitude']

            # التحقق من صحة الإحداثيات
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                return render(request, 'route_optimizer/error.html', {'message': 'خطوط الطول والعرض غير صحيحة.'})

            station = {
                'name': station_data['name'],
                'latitude': latitude,
                'longitude': longitude
            }
            stations.append(station)
            return redirect('home')
        
    # حذف المحطات المختارة
    if 'delete_selected' in request.POST:
        selected_indices = request.POST.getlist('selected_stations')
        stations = [station for index, station in enumerate(stations) if str(index) not in selected_indices]
        return redirect('home')

    form = StationForm()
    context = {
        'stations': stations,
        'form': form
    }
    return render(request, 'route_optimizer/home.html', context)

def optimize_route(request):
    if len(stations) < 2:
        return render(request, 'route_optimizer/error.html', {'message': 'يجب إدخال محطتين على الأقل لبدء التحسين.'})

    num_stations = len(stations)
    distances = np.zeros((num_stations, num_stations))
    for i in range(num_stations):
        for j in range(num_stations):
            distances[i][j] = np.sqrt(
                (stations[i]['latitude'] - stations[j]['latitude'])**2 +
                (stations[i]['longitude'] - stations[j]['longitude'])**2
            )

    best_route = genetic_algorithm(num_generations=100, population_size=20, distances=distances)
    route_length = calculate_route_length(best_route, distances)
    best_route_stations = [stations[i] for i in best_route]
    route_safety = calculate_route_safety(best_route, distances)

    report = [
        f'تم اختيار هذا المسار بناءً على أقل مسافة ممكنة.',
        f'معدل الأمان يقدر بـ {route_safety}%.',
        f'إجمالي طول المسار هو {route_length} كم.'
    ]

    context = {
        'best_route': best_route_stations,
        'route_length': route_length,
        'route_safety': route_safety,
        'report': report
    }
    return render(request, 'route_optimizer/result.html', context)

def calculate_route_length(route, distances):
    length = sum(distances[route[i], route[i + 1]] for i in range(len(route) - 1))
    return round(length, 2)

def calculate_route_safety(route, distances):
    avg_distance = sum(distances[route[i], route[i + 1]] for i in range(len(route) - 1)) / (len(route) - 1)
    safety_score = 1 / (1 + avg_distance)*6
    return round(safety_score * 100, 2)

def genetic_algorithm(num_generations, population_size, distances):
    num_stations = len(distances)
    population = [random.sample(range(num_stations), num_stations) for _ in range(population_size)]
    
    for generation in range(num_generations):
        population = sorted(population, key=lambda route: calculate_route_length(route, distances))
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
