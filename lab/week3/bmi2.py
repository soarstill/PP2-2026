# 문제

# 여러 학생들의 이름과 키와 몸무게를 리스트로 입력 받아 BMI 리스트를 출력하는 
# 함수와 테스트하는 함수를 작성하시오.
# BMI 함수는 지난 시간에 작성한 get_bmi 함수를 이용하여 작성하시오.
import sys
from pathlib import Path

# 프로젝트 루트 경로를 모듈 검색 경로에 추가
sys.path.append(str(Path(__file__).resolve().parents[2]))


import lab.week2.bmi as b


def get_bmis(names, heights, weights):
	"""Return each student's name and BMI.

	Heights are given in centimeters and weights in kilograms, matching
	``lab.week2.bmi.get_bmi``.
	"""
	if not (len(names) == len(heights) == len(weights)):
		raise ValueError("names, heights, and weights must have the same length")

	return [
		(name, b.get_bmi(height, weight))
		for name, height, weight in zip(names, heights, weights)
	]


def test_get_bmis():
	"""Test the BMI-list function with a small set of students."""
	result = get_bmis(["민수", "지수"], [170, 160], [65, 50])
	expected = [
		("민수", b.get_bmi(170, 65)),
		("지수", b.get_bmi(160, 50)),
	]
	assert result == expected
	print(result)


if __name__ == "__main__":
	test_get_bmis()