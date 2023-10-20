import cv2

# 打开摄像头
cap = cv2.VideoCapture(0)
# 显示界面
while True:
    # 读取摄像头数据
    ret, frame = cap.read()
    # 显示图像
    cv2.imshow('frame', frame)
    # 按下q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
