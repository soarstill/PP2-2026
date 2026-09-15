import matplotlib.pyplot as plt
import tensorflow as tf

mnist = tf.keras.datasets.mnist

# 훈련 데이터와 테스트 데이터를 가져온다.
(x_train, y_train),(x_test, y_test) = mnist.load_data()	


# 넘파이를 사용하여 입력을 0.0에서 1.0 사이로 만든다. 
x_train, x_test = x_train / 255.0, x_test / 255.0
plt.imshow(x_train[0], cmap="Greys")
model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
model.add(tf.keras.layers.Dense(512, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test)

# 학습 이미지 하나 선택
sample = x_train[100]
label = y_train[100]

# 입력 형태 맞추기
sample_input = sample.reshape(1, 28, 28)

# 예측 수행
prediction = model.predict(sample_input)

# 가장 높은 확률의 클래스 선택
predicted_digit = prediction.argmax()

# 출력
print("정답 라벨:", label)
print("모델 예측:", predicted_digit)

# 이미지 표시
plt.imshow(sample, cmap="Greys")
plt.title(f"Label: {label}, Predicted: {predicted_digit}")
plt.show()