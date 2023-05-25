import grpc
import image_service_pb2
import image_service_pb2_grpc
import cv2
import os
import shutil
import time
import numpy as np
from io import BytesIO
from pixellib.torchbackend.instance import instanceSegmentation
from concurrent import futures

class ImageServiceServicer(image_service_pb2_grpc.ImageServiceServicer):
    def ProcessImage(self, request, context):
        ins = instanceSegmentation()
        ins.load_model("C:/Users/user/OneDrive/Desktop/3th_semester/thesis2/Coding/another_example/model/pointrend_resnet50.pkl")
        image_path = request.image_path

        # Perform instance segmentation
        result =ins.segmentImage('../app/screenshot.jpg', show_bboxes=True, output_image_name="output_image.jpg")
        my_dict = dict(result[0])
        with open('result.txt', 'w') as file:
            for key, values in my_dict["object_counts"].items():
                values_str = str(values)
                file.write(f"{key}: {values_str}\n")
        response = image_service_pb2.ImageResponse()
        response.result_dict.update(result)

        return response
    


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_service_pb2_grpc.add_ImageServiceServicer_to_server(
        ImageServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()