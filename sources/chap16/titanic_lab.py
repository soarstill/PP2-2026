import pandas as pd

# 1. 데이터 읽기
df = pd.read_csv("titanic.csv")

# 2. 필요한 열만 사용 (예시)
#    Pclass: 선실 등급, Sex: 성별, Age: 나이
df = df[["Survived", "Pclass", "Sex", "Age"]]

# 3. Sex를 숫자로 변환 (male=0, female=1)
df["SexCode"] = df["Sex"].map({"male": 0, "female": 1})

# 4. Age 결측치는 중앙값으로 채우기
df["Age"] = df["Age"].fillna(df["Age"].median())

# 5. 입력(X), 타깃(y) 분리
X = df[["Pclass", "SexCode", "Age"]]
y = df["Survived"]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0 )

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# 1. 모델 객체 생성
log_clf = LogisticRegression(max_iter=1000)  # 반복 횟수 여유롭게

# 2. 학습
log_clf.fit(X_train, y_train)

# 3. 예측
y_pred_log = log_clf.predict(X_test)

# 4. 정확도
acc_log = accuracy_score(y_test, y_pred_log)
print("로지스틱 회귀 정확도:", acc_log)

from sklearn.tree import DecisionTreeClassifier

# 1. 모델 객체 생성 (깊이 제한 예시)
tree_clf = DecisionTreeClassifier(max_depth=3, random_state=0)

# 2. 학습
tree_clf.fit(X_train, y_train)

# 3. 예측
y_pred_tree = tree_clf.predict(X_test)

# 4. 정확도
acc_tree = accuracy_score(y_test, y_pred_tree)
print("결정 트리 정확도:", acc_tree)