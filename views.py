from django.shortcuts import render

BLOCKED_NODES = {"I", "O"}


def is_allowed_node(node):
    """Validate node letters and block I/O as requested."""
    return node.isalpha() and len(node) == 1 and node.upper() not in BLOCKED_NODES


def q1(request):
    result = None

    if request.method == "POST":
        start = request.POST.get("start", "").strip().upper()
        steps_raw = request.POST.get("steps", "0").strip()
        direction = request.POST.get("direction", "left").strip().lower()

        if is_allowed_node(start):
            try:
                steps = int(steps_raw)
            except ValueError:
                steps = 0

            if steps > 0 and direction in {"left", "right"}:
                ascii_code = ord(start)
                delta = -1 if direction == "left" else 1
                moves = 0

                while moves < steps:
                    ascii_code += delta
                    if ascii_code < ord("A"):
                        ascii_code = ord("Z")
                    elif ascii_code > ord("Z"):
                        ascii_code = ord("A")

                    candidate = chr(ascii_code)
                    if candidate in BLOCKED_NODES:
                        continue

                    moves += 1

                result = chr(ascii_code)

    return render(request, "q1.html", {"result": result})


def q2(request):
    route = None

    if request.method == "POST":
        flights = [
            {"source": "A", "destination": "D", "distance": 12},
            {"source": "C", "destination": "L", "distance": 35},
            {"source": "H", "destination": "M", "distance": 18},
            {"source": "I", "destination": "B", "distance": 40},
            {"source": "F", "destination": "O", "distance": 42},
        ]

        valid_flights = [
            f
            for f in flights
            if f["source"] not in BLOCKED_NODES and f["destination"] not in BLOCKED_NODES
        ]

        if valid_flights:
            route = max(valid_flights, key=lambda x: x["distance"])

    return render(request, "q2.html", {"route": route})


def q3(request):
    route = None

    if request.method == "POST":
        source = request.POST.get("source", "").strip().upper()
        destination = request.POST.get("destination", "").strip().upper()

        if is_allowed_node(source) and is_allowed_node(destination):
            # Replace this with Dijkstra/BFS over your graph.
            route = {
                "source": source,
                "destination": destination,
                "distance": 20,
            }

    return render(request, "q3.html", {"route": route})
