import base64
import io

from PIL import Image

filepath = r'D:\project\grpc-client\a12345.txt'

import base64
from PIL import Image
import io

# 1. 从文本文件中读取图像字符串
with open(filepath, "r") as file:
    image_string = file.read()

# 2. 解码图像字符串
image_bytes = base64.b64decode(image_string)

# 3. 创建图像对象
img = Image.open(io.BytesIO(image_bytes))

# 4. 显示、保存或进一步处理图像
img.show()  # 显示图像
img.save("restored_image.jpg")  # 保存图像到文件
