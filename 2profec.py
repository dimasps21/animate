import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Загружаем предобученную модель MobileNetV2
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Загружаем изображение (замените 'image.jpg' на путь к вашему изображению)
img_path = 'i (5).webr' # 
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

# Делаем предсказание
predictions = model.predict(x)
decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]

# Выводим результаты
print('Предсказания:')
for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
    print(f"{i+1}: {label} ({score:.2f})")