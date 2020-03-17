"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///desserts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/api/cupcakes')
def send_info_for_all_cupcakes():
    """Sends json info for all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>')
def send_info_for_one_cupcake(cupcake_id):
    """Sends json info for one cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a cupcake and returns info"""
  
    cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'],image=request.json['image'] or None)


    db.session.add(cupcake)
    db.session.commit()

    json_response = jsonify(cupcake=cupcake.serialize())
    return (json_response, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates a cupcake and returns new cupcake info"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)


    db.session.add(cupcake)
    db.session.commit()

    json_response = jsonify(cupcake=cupcake.serialize())
    return json_response

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Cupcake deleted")

@app.route('/api/cupcakes/search/<search_term>')
def search_cupcakes(search_term):

    if search_term.isdigit():
        cupcakes = Cupcake.query.filter(Cupcake.rating == f"{search_term}")
    else:
        cupcakes = Cupcake.query.filter((Cupcake.flavor.ilike(f'%{search_term}%')) | (Cupcake.size.ilike(f'%{search_term}%')))

    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)
  














