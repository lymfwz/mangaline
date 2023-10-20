# // RPC 必备的包，以及刚刚生成的俩文件
import base64
import concurrent
import io
import os
import shutil
import threading

import grpc
from PIL import Image

import msg_pb2
import msg_pb2_grpc

# // 并发
from concurrent import futures
import time
import cv2
import numpy as np

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
try:
    from tensorflow.keras.models import load_model

    # 加载预训练模型
    model = load_model("model.h5")
except Exception as e:
    print(e)
# TODO
# 处理图像的函数
def process_image(img):
    ori_img = img
    try:
        R = 2 ** 3
        # 读取图片
        # img = cv2.imdecode(np.fromfile(img, dtype=np.uint8), -1)

        # 转换为灰度图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 对图像执行亮度校正
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
        img = clahe.apply(img)

        # 调整图像尺寸
        img_predict = cv2.resize(img, (img.shape[1] // R * R, img.shape[0] // R * R),
                                 interpolation=cv2.INTER_AREA)
        img_predict = np.reshape(img_predict, (1, img_predict.shape[0], img_predict.shape[1], 1))
        img_predict = img_predict.astype(np.float32) * 0.003383

        # 使用模型进行预测
        result = model.predict(img_predict, batch_size=1)[0]

        # 根据结果生成输出图像
        img_res = (result - np.mean(result) + 1.) * 255
        img_res = cv2.resize(img_res, (img.shape[1], img.shape[0]))

        # 保存输出图像
        out_dir = os.path.join(os.getcwd(), "output")
        print(out_dir)
        cv2.imencode(".jpg", img_res)[1].tofile(
            os.path.join(out_dir, "res.jpg"))
        # cv2.imshow(img_res)
        print("图像处理完成")
        return img_res
    except Exception as e:
        print(e)
        return ori_img
    # return ori_img

# 启动一个线程来处理图像
def process_image_thread(input_image):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(process_image, input_image)
        img_res = future.result()
    # # 创建线程
    # thread = threading.Thread(target=process_image, args=input_image)
    # # 启动线程
    # thread.start()
    # # 等待线程完成
    # thread.join()

    return img_res  # 返回原始图像或处理后的图像

# // service 实现GetMsg方法
class MsgServicer(msg_pb2_grpc.MsgServiceServicer):

    def GetMsg(self, request, context):
        # 2. 解码图像字符串
        image_bytes = base64.b64decode(request.name)
        # 3. 创建图像对象
        # img = Image.open(io.BytesIO(image_bytes))

        # TODO 图像处理 == 阻塞
        print("Received img")
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # img1 = process_image_thread(np.array(img))
        img1 = process_image_thread(img)
        img1 = Image.open(os.path.join(os.getcwd(), "output\\res.jpg"))
        # cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
        # img = Image.open(os.path.join(os.getcwd(), "output\\res.png"))

        # 将图像转换为字节数组
        with io.BytesIO() as output:
            img1.save(output, format="JPEG")  # 指定图像格式，根据需要更改
            image_data = output.getvalue()
        img_res_str = base64.b64encode(image_data).decode()
        print("结果简略："+img_res_str[0:100])
        # print("Received name: %s" % request.name)
        return msg_pb2.MsgResponse(msg='Hello, %s!' % img_res_str)
        # return msg_pb2.MsgResponse(img_res_str)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msg_pb2_grpc.add_MsgServiceServicer_to_server(MsgServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()