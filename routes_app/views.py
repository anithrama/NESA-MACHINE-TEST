from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from collections import deque

from .forms import AirportRouteForm, NodeSearchForm, ShortestRouteForm
from .models import AirportRoute

BLOCKED_CODES = {"I", "O"}

# Q1 tree map with weighted left/right edges.
TREE_MAP = {
	"A": {"left": ("B", 20), "right": ("C", 30)},
	"B": {"left": ("H", 15), "right": ("J", 25)},
	"C": {"left": ("K", 22), "right": ("L", 35)},
	"H": {"left": ("M", 8), "right": ("N", 9)},
	"J": {"left": ("P", 14), "right": ("Q", 16)},
	"K": {"left": ("R", 19), "right": ("S", 21)},
	"L": {"left": ("T", 23), "right": None},
	"M": {"left": None, "right": None},
	"N": {"left": None, "right": None},
	"P": {"left": None, "right": None},
	"Q": {"left": None, "right": None},
	"R": {"left": None, "right": None},
	"S": {"left": None, "right": None},
	"T": {"left": None, "right": None},
}


def _ordered_routes():
	return list(AirportRoute.objects.exclude(airport_code__in=BLOCKED_CODES).order_by("position"))


def _next_index(current_index, direction, total):
	if direction == "left":
		return (current_index - 1) % total
	return (current_index + 1) % total


def add_route(request):
	added_route = None

	if request.method == "POST":
		form = AirportRouteForm(request.POST)
		if form.is_valid():
			new_route = form.save()
			return redirect(f"{reverse('add_route')}?added={new_route.id}")
	else:
		form = AirportRouteForm()

	added_id = request.GET.get("added")
	if added_id and added_id.isdigit():
		added_route = AirportRoute.objects.filter(id=int(added_id)).first()

	routes = AirportRoute.objects.exclude(airport_code__in=BLOCKED_CODES).order_by("position")
	return render(
		request,
		"add_route.html",
		{"form": form, "routes": routes, "added_route": added_route},
	)


def delete_route(request, route_id):
	if request.method == "POST":
		route = get_object_or_404(AirportRoute, id=route_id)
		route.delete()
	return redirect("add_route")


def q1(request):
	result = None
	path = []
	total_distance = 0
	form = NodeSearchForm(request.POST or None)

	if request.method == "POST" and form.is_valid():
		start = form.cleaned_data["start"]
		target = form.cleaned_data["target"]
		direction = form.cleaned_data["direction"]

		current = start
		path = [current]
		if current not in TREE_MAP:
			result = "Invalid Input"
		else:
			if current == target:
				result = "Found"
			while result is None:
				edge = TREE_MAP.get(current, {}).get(direction)
				if not edge:
					result = "No valid path"
					break
				next_node, distance = edge
				if next_node in BLOCKED_CODES:
					result = "No valid path"
					break
				total_distance += distance
				current = next_node
				path.append(current)

				if current == target:
					result = "Found"
					break

			if result is None:
				result = "No valid path"

	return render(
		request,
		"q1.html",
		{
			"form": form,
			"result": result,
			"path": " -> ".join(path),
			"distance": total_distance,
		},
	)


def q2(request):
	def find_longest_path(node, current_path, current_distance):
		max_path = list(current_path)
		max_distance = current_distance

		for direction in ("left", "right"):
			edge = TREE_MAP.get(node, {}).get(direction)
			if not edge:
				continue

			next_node, edge_distance = edge
			if next_node in BLOCKED_CODES:
				continue

			candidate_path, candidate_distance = find_longest_path(
				next_node,
				current_path + [next_node],
				current_distance + edge_distance,
			)

			if candidate_distance > max_distance:
				max_distance = candidate_distance
				max_path = candidate_path

		return max_path, max_distance

	path, distance = find_longest_path("A", ["A"], 0)

	return render(
		request,
		"q2.html",
		{
			"node": path[-1],
			"path": " -> ".join(path),
			"distance": distance,
		},
	)


def q3(request):
	steps_output = []
	shortest_step = None
	result = None
	form = ShortestRouteForm(request.POST or None)

	if request.method == "POST" and form.is_valid():
		source = form.cleaned_data["source"]
		destination = form.cleaned_data["destination"]

		queue = deque([(source, [])])
		visited = set()

		while queue:
			node, edge_path = queue.popleft()

			if node == destination:
				if edge_path:
					min_edge = min(edge_path, key=lambda x: x[2])
					shortest_step = f"{min_edge[0]} → {min_edge[1]} = {min_edge[2]} km"
					steps_output = [f"{src} → {dst} = {dist} km" for src, dst, dist in edge_path]
					result = "Found"
				else:
					result = "Source and destination are the same."
				break

			visited.add(node)

			for direction in ("left", "right"):
				edge = TREE_MAP.get(node, {}).get(direction)
				if not edge:
					continue
				next_node, distance = edge
				if next_node in BLOCKED_CODES:
					continue
				if next_node not in visited:
					queue.append((next_node, edge_path + [(node, next_node, distance)]))

		if result is None:
			result = "No valid path"

	return render(
		request,
		"q3.html",
		{
			"form": form,
			"steps": steps_output,
			"shortest": shortest_step,
			"result": result,
		},
	)
