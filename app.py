import os
import subprocess
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Directory where the executable files (scripts) are stored
SCRIPT_DIR = "/home/atharva/ros2_ws/src/amogh/amogh/helloworld.py"  # Replace with the actual path

# Route to render the HTML page
@app.route('/')
def index():
    # List files in the directory
    scripts = [f for f in os.listdir(SCRIPT_DIR) if os.path.isfile(os.path.join(SCRIPT_DIR, f))]
    return render_template('index.html', scripts=scripts)

# Route to run the selected file
@app.route('/run_script/<script_name>', methods=['GET'])
def run_script(script_name):
    script_path = os.path.join(SCRIPT_DIR, script_name)

    # Check if the file exists
    if os.path.exists(script_path) and os.path.isfile(script_path):
        try:
            # Execute the script and capture the output
            result = subprocess.check_output([script_path], shell=True, text=True)
            return jsonify({'output': result, 'status': 'success'})
        except subprocess.CalledProcessError as e:
            return jsonify({'output': str(e), 'status': 'error'})
    else:
        return jsonify({'output': 'Script not found', 'status': 'error'})

if __name__ == '__main__':
    app.run(debug=True)
