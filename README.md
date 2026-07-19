# Semiconductor Yield Fail Prediction & Quality Data Analysis

## 1. Background

반도체 제조/평가 공정에서는 다수의 계측 및 센서 데이터가 수집되며,
이 데이터는 수율 저하, 공정 이상, 품질 리스크를 조기에 발견하는 데 활용될 수 있다.

본 프로젝트는 공개 반도체 공정 데이터인 SECOM 데이터를 활용하여
Pass/Fail 수율 결과를 분석하고, Fail과 연관된 핵심 측정 인자 후보를 도출하는 것을 목표로 한다.

## 2. Dataset

- Dataset: SECOM Data Set
- Source: UCI Machine Learning Repository
- Domain: Semiconductor manufacturing process
- Target: Pass/Fail yield label
- Label definition:
  - -1: Pass
  - 1: Fail

## 3. Project Goal

본 프로젝트의 목표는 다음과 같다.

1. 반도체 공정/평가 데이터의 품질 상태를 진단한다.
2. Pass/Fail 불균형 구조를 확인한다.
3. 결측값, 상수 feature 등 모델링 전처리 이슈를 파악한다.
4. 이후 Fail 예측 모델링과 핵심 불량 인자 후보 도출을 위한 기반을 마련한다.

## 4. Step 1. Data Quality Check Result

SECOM 반도체 공정 데이터를 대상으로 모델링 전 데이터 품질 진단을 수행하였다.

| 항목 | 결과 |
|---|---:|
| 전체 샘플 수 | 1,567 |
| 전체 feature 수 | 590 |
| Pass 개수 | 1,463 |
| Fail 개수 | 104 |
| Fail 비율 | 6.64% |
| 결측값이 있는 feature 수 | 538 |
| 결측률 50% 이상 feature 수 | 28 |
| 상수 feature 수 | 116 |
| 제거 후보 반영 후 남은 feature 수 | 446 |

### Key Findings

1. 전체 샘플 중 Fail 비율은 6.64%로, 데이터가 심한 class imbalance 구조를 가진다.
2. 따라서 후속 모델링에서는 단순 Accuracy보다 Fail Recall, Precision, PR-AUC, Confusion Matrix를 중심으로 평가할 필요가 있다.
3. 전체 590개 feature 중 538개 feature에 일부 결측값이 존재하였다.
4. 결측률이 50% 이상인 feature는 28개로, 데이터 신뢰성이 낮은 측정 인자로 판단하여 1차 제거 후보로 분류하였다.
5. 값의 변화가 없는 상수 feature는 116개로 확인되었으며, Pass/Fail 구분에 기여하기 어렵기 때문에 제거 후보로 분류하였다.
6. 결측률 50% 이상 feature와 상수 feature를 제외하면 후속 분석 대상 feature는 446개로 정리된다.

### Interpretation

반도체 평가 및 품질관리 업무에서는 단순히 데이터를 모델에 입력하는 것보다,
측정 데이터의 신뢰성, 결측 발생 패턴, 불량 class의 불균형성을 먼저 파악하는 것이 중요하다.

특히 Fail 샘플은 전체 데이터에서 소수이기 때문에,
후속 모델링 단계에서는 단순 Accuracy보다 Fail Recall, Precision, PR-AUC, Confusion Matrix를 중심으로 평가할 예정이다.

본 데이터는 실제 반도체 평가/품질 데이터처럼 결측값, 불균형 class, 고차원 feature 구조를 가지고 있다.
따라서 모델링에 앞서 데이터 품질 진단과 전처리 기준 수립이 중요하다.
특히 Fail 샘플이 소수이므로, 향후 분석에서는 정상 샘플 예측 정확도보다 Fail 검출률과 False Alarm 간 균형을 중점적으로 평가할 예정이다.


