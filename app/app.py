from flask import Flask, render_template, Response
import cv2
import grpc
import image_service_pb2_grpc
import image_service_pb2

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
camera = cv2.VideoCapture(0)


def capture_frame():
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(capture_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/screenshot')
def screenshot():
    success, frame = camera.read()
    if success:
        cv2.imwrite('screenshot.jpg', frame)
        return 'Screenshot captured successfully!'
    else:
        return 'Failed to capture screenshot.'
    
@app.route('/segment-image')
def process_image():
    # Create a gRPC request message
    # request = webcam_pb2.ScreenshotRequest(image_path='../app/static/screenshot.jpg')

    image_path='../app/static/screenshot.jpg'
    channel = grpc.insecure_channel('localhost:50051')
    stub = image_service_pb2_grpc.ImageServiceStub(channel)
    request = image_service_pb2.ImageRequest()
    request.image_path = image_path

    response = stub.ProcessImage(request)

    # Display the segmented image next to the video record
    return render_template(response)

if __name__ == '__main__':
    app.run(debug=True)
