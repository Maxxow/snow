from flask import Flask, jsonify, request
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

# --- Lógica de cálculo de coordenadas ---
def koch_recursive(points, x1, y1, x2, y2, order):
    if order == 0:
        points.append((x1, y1))
    else:
        dx, dy = x2 - x1, y2 - y1
        x_third_1, y_third_1 = x1 + dx / 3, y1 + dy / 3
        x_third_2, y_third_2 = x1 + 2 * dx / 3, y1 + 2 * dy / 3
        
        angle = math.radians(60)
        x_peak = x_third_1 + (x_third_2 - x_third_1) * math.cos(angle) - (y_third_2 - y_third_1) * math.sin(angle)
        y_peak = y_third_1 + (x_third_2 - x_third_1) * math.sin(angle) + (y_third_2 - y_third_1) * math.cos(angle)
        
        koch_recursive(points, x1, y1, x_third_1, y_third_1, order - 1)
        koch_recursive(points, x_third_1, y_third_1, x_peak, y_peak, order - 1)
        koch_recursive(points, x_peak, y_peak, x_third_2, y_third_2, order - 1)
        koch_recursive(points, x_third_2, y_third_2, x2, y2, order - 1)

def get_koch_coordinates(order, size=400, is_complete=True):
    points = []
    
    p1 = (-size / 2, -size / (2 * math.sqrt(3)))
    p2 = (size / 2, -size / (2 * math.sqrt(3)))
    p3 = (0, size * math.sqrt(3) / 2 - size / (2 * math.sqrt(3)))

    if is_complete:
        koch_recursive(points, p1[0], p1[1], p2[0], p2[1], order)
        koch_recursive(points, p2[0], p2[1], p3[0], p3[1], order)
        koch_recursive(points, p3[0], p3[1], p1[0], p1[1], order)
        points.append(p1)
    else:
        p1_half = (-size/1.5, 0)
        p2_half = (0, 0)
        p3_half = (-size/3, size * math.sqrt(3) / 3)

        koch_recursive(points, p1_half[0], p1_half[1], p2_half[0], p2_half[1], order)
        koch_recursive(points, p2_half[0], p2_half[1], p3_half[0], p3_half[1], order)
        points.append(p3_half)
    
    return points

@app.route('/generate_snowflake', methods=['POST'])
def generate_snowflake():
    data = request.json
    order = int(data.get('order', 0))
    is_complete = bool(data.get('is_complete', True))
    
    coords = get_koch_coordinates(order, is_complete=is_complete)
    return jsonify(coords)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)