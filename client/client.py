import grpc

import greeter_pb2
import greeter_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = greeter_pb2_grpc.GreeterStub(channel)

response = stub.SayHello(greeter_pb2.HelloRequest(name='World'))
print(response.message)