from flask import Flask
from flask import request, jsonify
from models import Queue

#Flask Config 
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'


queue = Queue()
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/new', methods=['POST'])
def get_user():
    name = request.json.get('name', None)
    email = request.json.get('email', None)
    phone = request.json.get('phone', None)

    if name and email and phone:
        info = request.get_json()
        queue.enqueue(info)
        return jsonify({"msg": f"User with name {name} was added to the queue"}), 200
    else:
        return jsonify({"msg": "You have to input a name, email and phone"}),401


@app.route('/next', methods=['GET'])
def next_user():
    return jsonify({"msg": f"{queue.dequeue()} not loner in the queue"})
    

@app.route('/all', methods=['GET'])
def get_all():
    queue.get_queue()
    return jsonify({"msg": f"A list with {queue.size()} entries has been send"})

if __name__ == '__main__':
    app.run()
