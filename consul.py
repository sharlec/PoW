import time
import grpc
import consul
import json
from concurrent import futures
 
import test_pb2_grpc
import test_pb2


def test(request, context):
 # 实际调用到的函数
    json_response = test_pb2.JSONResponse()
    json_response.rst_string = json.dumps({"ret":"Hi gRPC"})# 构造出proto文件中定义的返回值格式
    return json_response

class OrderHandler(test_pb2_grpc.OrderHandlerServicer):
    def create_order(self, request, context):
        return test(request, context)

def register(server_name, ip, port):
    c = consul.Consul() # 连接consul 服务器，默认是127.0.0.1，可用host参数指定host
    print(f"开始注册服务{server_name}")
    check = consul.Check.tcp(ip, port, "10s") # 健康检查的ip，端口，检查时间
    c.agent.service.register(server_name, f"{server_name}-{ip}-{port}",
         address=ip, port=port, check=check) # 注册服务部分
    print(f"注册服务{server_name}成功")

def unregister(server_name, ip, port):
    c = consul.Consul()
    print(f"开始退出服务{server_name}")
    c.agent.service.deregister(f'{server_name}-{ip}-{port}')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_OrderHandlerServicer_to_server(OrderHandler(), server)
    server.add_insecure_port('[::]:{}'.format(12006))
    register("order_server", "0.0.0.0", 12006)
    server.start()
    try:
        while True:
            time.sleep(186400)
    except KeyboardInterrupt:
        unregister("order_server", "0.0.0.0", 12006)
        server.stop(0)
serve()