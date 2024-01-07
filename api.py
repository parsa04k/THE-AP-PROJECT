from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database                                # How to user (baraye to ino neveshtam ailin)
database = {                                                # import requests
    "1": 25,                                                # id_and_capacity = requests.get('http://127.0.0.1:5000/slots')
    "2": 15,                                                # print( eval(id_and_capacity) )
    "3": 15,                                                    # output: ye dictionary be shekl hamin database to file api hast
    "4": 20,                                                    # va agar key ro begiri behet zarfiat mide
    "5": 30,
    "6": 9,
    "7": 8
}

@app.route('/slots', methods=['GET'])
def get_slots():
    return jsonify(database)

@app.route('/reserve', methods=['GET'])
def reserve_slot():
    data      = request.json
    clinic_id = str(data.get('id'))
    reserved  = data.get('reserved', 0)

    if clinic_id in database and database[clinic_id] >= reserved:
        database[clinic_id] -= reserved
        return jsonify({"success": True, "remaining_slots": database[clinic_id]})
    else:
        return jsonify({"success": False, "message": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True)
