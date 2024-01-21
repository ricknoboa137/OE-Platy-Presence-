import cv2
import numpy as np
import base64
image = ""  # raw data with base64 encoding
decoded_data = base64.b64decode(image)
np_data = np.fromstring(decoded_data,np.uint8)
img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
cv2.imshow("test", img)
cv2.waitKey(0)
