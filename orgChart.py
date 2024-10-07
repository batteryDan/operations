from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Base path for serving files
base_path = r"C:\_git\operations"  # Base directory for your files

@app.route('/')
def index():
    return send_from_directory(base_path, 'orgChart.html')

@app.route('/orgChart.csv')
def serve_csv():
    return send_from_directory(base_path, 'orgChart.csv')

# Route to serve headshots from the 'final' subdirectory within 'headshots'
@app.route('/headshots/final/<filename>')
def serve_headshots(filename):
    # Construct the path to the 'final' subdirectory within 'headshots'
    headshots_path = os.path.join(base_path, 'headshots', 'final')
    return send_from_directory(headshots_path, filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
