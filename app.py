
from flask import Flask, render_template, Response, redirect, url_for
from object_tracking import generate_frames  # Import the function from your object tracking code

app = Flask(__name__)

# Initialize streaming status
is_streaming = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    global is_streaming
    is_streaming = True
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop')
def stop():
    global is_streaming
    is_streaming = False
    return redirect(url_for('index'))

@app.route('/resume')
def resume():
    global is_streaming
    is_streaming = True
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
