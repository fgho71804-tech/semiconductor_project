# 반도체 품질관리 / 평가및분석 직무 대비 사이드 프로젝트 가이드라인

> 목표 직무: SK하이닉스 기반기술, 삼성전자 Foundry사업부 평가및분석, 품질관리/평가 데이터 분석 직무  
> 추천 메인 프로젝트: **SECOM 반도체 공정 데이터 기반 수율 Fail 예측 및 핵심 불량 인자 후보 도출**

---

## 0. 이 프로젝트의 목적

이 프로젝트는 단순히 머신러닝 모델을 만드는 것이 아니라, **반도체 평가및분석 / 품질관리 엔지니어가 실제로 수행하는 사고 흐름**을 경험하고 포트폴리오로 정리하는 것을 목표로 한다.

삼성전자 Foundry사업부 평가및분석 직무는 반도체 특성 평가와 분석에 필요한 테스트 솔루션을 개발하고, 평가 데이터를 분석해 수율 및 특성 개선 항목을 발굴하며, 제품 개발과 양산을 위한 기술적 솔루션을 제공하는 직무로 설명된다. 또한 품질관리 측면에서는 제품 신뢰성 및 품질을 보증하고, 평가 방법론과 통계적 분석 방법을 개발하며, 균일한 양산품질 확보를 위한 통계적 품질관리를 수행한다.

따라서 프로젝트의 핵심 방향은 다음과 같다.

- 평가 데이터를 분석한다.
- Pass / Fail 수율 결과를 예측한다.
- Fail과 연관된 핵심 측정 인자 후보를 찾는다.
- 통계적 품질관리 관점에서 모니터링 방안을 제안한다.
- 결과를 자소서와 면접에서 설명 가능한 형태로 정리한다.

---

## 1. 프로젝트 제목

### 추천 제목

**반도체 공정 평가 데이터 기반 수율 Fail 예측 및 핵심 불량 인자 후보 도출 프로젝트**

### 포트폴리오용 한 줄 설명

> 공개 반도체 공정 데이터인 SECOM을 활용하여 평가 데이터 전처리, 결측/이상치 분석, 불균형 수율 Fail 예측, 핵심 측정 인자 후보 도출, 통계적 모니터링 Rule 제안까지 수행한 프로젝트입니다.

### 자소서용 한 줄 설명

> 반도체 유관 경험 부족을 보완하기 위해 공개 반도체 공정 데이터를 활용해 수율 Fail 예측 및 핵심 측정 인자 후보 도출 프로젝트를 수행하며, 평가/품질 데이터 분석의 전체 흐름을 경험했습니다.

---

## 2. 사용할 데이터셋

## 2.1 메인 데이터셋: SECOM

### 데이터 개요

- 데이터명: SECOM Semiconductor Manufacturing Data
- 데이터 성격: 반도체 제조 공정 중 수집된 센서/계측 데이터와 Pass/Fail 라벨
- 샘플 수: 약 1,567개
- Feature 수: 약 591개
- Target: Pass / Fail
- 특징:
  - 실제 반도체 제조 데이터와 유사하게 결측값이 많다.
  - Feature명이 비식별화되어 있다.
  - Fail 샘플 수가 적어 class imbalance가 존재한다.
  - 수율 저하와 연관된 feature 후보를 찾는 문제에 적합하다.

### 추천 이유

SECOM은 처음 반도체 데이터 분석 프로젝트를 시작하기에 가장 적합하다.

- 반도체 제조 공정 데이터라는 직무 연관성이 높다.
- Pass / Fail 라벨이 있어 품질관리 문제로 풀기 좋다.
- 결측값, 불균형, 고차원 feature 등 실무형 데이터 이슈가 있다.
- 모델 성능뿐 아니라 원인 후보 분석, 품질 모니터링까지 확장할 수 있다.

### 주의할 점

SECOM 데이터의 feature는 비식별화되어 있으므로, 특정 feature를 실제 공정명이나 장비명으로 단정하면 안 된다.

잘못된 표현:

> feature_103이 Etch 공정 문제의 원인입니다.

올바른 표현:

> feature_103은 Fail 샘플에서 통계적으로 다른 분포를 보였고, 모델 중요도와 SHAP 분석에서도 상위에 위치했으므로 수율 저하와 연관된 핵심 측정 인자 후보로 판단했습니다. 실제 원인 규명을 위해서는 공정 Step, 장비, 소재 Lot, 계측 이력과의 추가 검증이 필요합니다.

---

## 3. 프로젝트 최종 목표

이 프로젝트의 최종 목표는 세 가지다.

| 목표 | 설명 | 직무 연결성 |
|---|---|---|
| Fail 예측 | 평가 데이터를 기반으로 최종 Fail 가능성을 예측 | 평가 데이터 분석, Test Screening |
| 핵심 인자 후보 도출 | Fail과 연관성이 높은 feature를 찾음 | 불량 원인 후보 발굴, 수율 개선 항목 도출 |
| 품질 모니터링 제안 | 핵심 feature 중심의 관리도와 이상 감지 기준 제안 | 통계적 품질관리, 양산품질 안정화 |

---

## 4. 전체 진행 로드맵

추천 기간은 4~6주다.

| 주차 | 목표 | 산출물 |
|---|---|---|
| 1주차 | 문제 정의, 데이터 다운로드, 데이터 품질 진단 | `01_data_quality_check.ipynb` |
| 2주차 | EDA, Pass/Fail 분포 비교, 통계검정 | `02_eda_fail_pattern_analysis.ipynb` |
| 3주차 | Baseline 모델링, 불균형 데이터 대응 | `03_modeling_fail_prediction.ipynb` |
| 4주차 | Feature importance, SHAP, 원인 후보 도출 | `04_feature_importance_root_cause_candidate.ipynb` |
| 5주차 | SPC/관리도, Screening Rule 제안 | `05_spc_monitoring_rule.ipynb` |
| 6주차 | README, 최종 보고서, 면접용 1페이지 정리 | `final_report.md`, `interview_summary_1page.pdf` |

처음 하는 경우 6주를 권장한다. 이미 Python과 pandas에 익숙하다면 4주 안에도 가능하다.

---

# Part 1. 문제 정의

## 1.1 문제 상황 설정

다음과 같은 실무 상황을 가정한다.

> 반도체 제조 공정에서 다수의 센서 및 계측 데이터가 수집되었다. 각 샘플은 최종적으로 Pass 또는 Fail 판정을 받는다. Fail 비율은 낮지만, Fail을 조기에 감지하지 못하면 수율 저하, 추가 검사 비용, 고객 품질 리스크로 이어질 수 있다. 따라서 평가 데이터를 기반으로 Fail 가능성을 예측하고, Fail과 연관된 핵심 측정 인자 후보를 도출해 품질 모니터링 및 추가 검사 전략을 수립하고자 한다.

## 1.2 프로젝트 문제 정의 예시

README 첫 부분에 아래 문장을 넣는다.

```text
본 프로젝트는 반도체 제조 공정에서 수집된 다수의 계측/센서 데이터를 활용하여 최종 수율 Fail을 예측하고, Fail 발생과 연관성이 높은 핵심 측정 인자 후보를 도출하는 것을 목표로 한다. 단순 예측 정확도보다 Fail 검출률, 불량 원인 후보의 해석 가능성, 품질관리 관점의 활용 가능성을 중점적으로 평가한다.
```

## 1.3 평가 지표 방향

이 프로젝트에서 Accuracy를 1순위 지표로 두면 안 된다.

Fail 샘플이 적기 때문에 모든 샘플을 Pass로 예측해도 Accuracy가 높게 나올 수 있다. 품질관리 관점에서는 Fail을 놓치는 것이 더 치명적이므로 다음 지표를 중심으로 봐야 한다.

| 지표 | 의미 | 왜 중요한가 |
|---|---|---|
| Fail Recall | 실제 Fail 중 모델이 잡아낸 비율 | 불량 유출 방지 관점에서 중요 |
| Precision | Fail이라고 예측한 것 중 실제 Fail 비율 | 과도한 추가 검사 방지 |
| PR-AUC | 불균형 데이터에서 모델 성능 평가 | Fail class가 적을 때 유용 |
| Balanced Accuracy | Pass/Fail 균형을 고려한 정확도 | class imbalance 보정 |
| Confusion Matrix | TP, FP, FN, TN 확인 | 실제 품질 의사결정에 직관적 |

---

# Part 2. 데이터 품질 진단

## 2.1 목표

첫 단계의 목표는 모델링이 아니라 **데이터가 어떤 상태인지 진단하는 것**이다.

실제 평가/품질 직무에서도 데이터 분석 전에 먼저 확인해야 할 것은 데이터의 신뢰성이다.

## 2.2 해야 할 일

아래 항목을 순서대로 확인한다.

| 확인 항목 | 목적 |
|---|---|
| 데이터 shape 확인 | 샘플 수와 feature 수 파악 |
| Pass/Fail 개수 확인 | class imbalance 확인 |
| 결측값 비율 확인 | 사용 불가능한 측정 항목 제거 기준 설정 |
| 상수 feature 확인 | 정보가 없는 측정값 제거 |
| 중복 feature 확인 | 불필요한 feature 제거 |
| 고상관 feature 확인 | 유사한 측정값 그룹 확인 |
| 시간 정보 확인 | 특정 시점에 Fail이 몰렸는지 확인 |

## 2.3 산출물 형식

`01_data_quality_check.ipynb` 마지막에 아래 표를 만든다.

| 항목 | 값 |
|---|---:|
| 전체 샘플 수 |  |
| 전체 feature 수 |  |
| Pass 샘플 수 |  |
| Fail 샘플 수 |  |
| Fail 비율 |  |
| 결측값이 있는 feature 수 |  |
| 결측률 50% 이상 feature 수 |  |
| 상수 feature 수 |  |
| 제거 후 남은 feature 수 |  |

## 2.4 전처리 기준 예시

처음에는 아래 기준을 사용한다.

| 항목 | 기준 |
|---|---|
| 결측률 높은 feature | 결측률 50% 이상 제거 |
| 상수 feature | unique 값이 1개인 feature 제거 |
| 결측치 대체 | train set median으로 대체 |
| 스케일링 | StandardScaler 적용 |
| 데이터 분할 | train / validation / test 또는 stratified k-fold |

주의할 점은 데이터 누수 방지다.

결측치 대체, 스케일링, feature selection은 반드시 train set 기준으로 `fit`해야 한다. validation/test set에는 `transform`만 적용한다.

면접에서 이 부분을 설명하면 좋다.

> 실무 데이터 분석에서는 모델 성능보다 평가 방법론의 신뢰성이 중요하다고 판단했습니다. 따라서 결측치 대체, 스케일링, feature selection은 train set 기준으로만 학습하고 validation/test에는 transform만 적용하여 데이터 누수를 방지했습니다.

---

# Part 3. EDA와 Fail 패턴 분석

## 3.1 목표

EDA의 목표는 단순히 그래프를 많이 그리는 것이 아니다.

핵심 질문은 다음이다.

> Fail 샘플은 정상 Pass 샘플과 어떤 측정값에서 다르게 보이는가?

## 3.2 필수 분석 목록

| 분석 | 목적 |
|---|---|
| Pass/Fail 비율 시각화 | class imbalance 확인 |
| Feature별 결측률 시각화 | 데이터 신뢰성 확인 |
| Pass/Fail별 feature 분포 비교 | Fail에서 달라지는 측정값 후보 확인 |
| 평균 차이 분석 | Fail과 Pass 간 중심값 차이 확인 |
| 분산 차이 분석 | Fail 샘플에서 변동성이 커지는 feature 확인 |
| Mann-Whitney U test 또는 t-test | Pass/Fail 차이의 통계적 유의성 확인 |
| Correlation heatmap | 유사 feature 그룹 확인 |
| PCA 또는 UMAP | Pass/Fail 분리 가능성 확인 |

## 3.3 Top feature 후보 선정 기준

처음에는 다음 기준을 조합해 Top 20 후보를 선정한다.

- Pass/Fail 평균 차이가 큰 feature
- 통계검정 p-value가 낮은 feature
- Fail에서 분산이 크게 증가한 feature
- 결측률이 높고 Fail과 동시 발생하는 feature
- 모델 중요도에서 상위에 위치한 feature

## 3.4 산출물 예시

`02_eda_fail_pattern_analysis.ipynb` 마지막에 아래 표를 만든다.

| Rank | Feature | 근거 | Fail에서의 경향 | 해석 |
|---:|---|---|---|---|
| 1 | feature_XX | 평균 차이 큼, p-value 낮음 | Fail에서 높음 | 수율 Fail 연관 후보 |
| 2 | feature_YY | Fail 분산 큼 | Fail에서 변동성 증가 | 공정/계측 변동성 후보 |
| 3 | feature_ZZ | 결측률 높음 | Fail 샘플에서 결측 동반 | 데이터 품질 또는 계측 안정성 확인 필요 |

---

# Part 4. Fail 예측 모델링

## 4.1 목표

모델링의 목적은 단순히 높은 Accuracy를 얻는 것이 아니다.

목표는 다음과 같다.

- Fail을 최대한 놓치지 않는다.
- False Alarm을 과도하게 늘리지 않는다.
- 모델이 어떤 feature를 근거로 판단했는지 설명한다.
- 품질관리 의사결정에 활용 가능한 threshold를 찾는다.

## 4.2 모델링 순서

처음부터 복잡한 모델로 가지 않는다. 반드시 baseline부터 시작한다.

| 순서 | 모델 | 목적 |
|---:|---|---|
| 1 | Dummy Classifier | 전부 Pass 예측 기준선 확인 |
| 2 | Logistic Regression | 해석 가능한 baseline |
| 3 | Random Forest | 비선형 관계 및 feature importance 확인 |
| 4 | Gradient Boosting / XGBoost / LightGBM | 성능 개선 |
| 5 | Top-N feature 모델 | 검사 효율화 관점 검증 |

## 4.3 불균형 데이터 대응

Fail class가 적으므로 다음 방법을 비교한다.

| 방법 | 설명 |
|---|---|
| class_weight 적용 | Fail class에 더 큰 가중치 부여 |
| threshold 조정 | Fail 판정 기준을 낮춰 Recall 확보 |
| SMOTE | 소수 class oversampling. 단, 검증 시 주의 필요 |
| PR-AUC 중심 평가 | ROC-AUC보다 불균형 데이터에 적합 |
| stratified split | train/test에 Fail 비율이 유지되도록 분할 |

처음에는 `class_weight='balanced'`와 threshold 조정부터 적용한다. SMOTE는 후순위로 둔다.

## 4.4 평가 지표 표

모델별 결과를 아래 표로 정리한다.

| Model | Accuracy | Balanced Accuracy | Fail Recall | Precision | PR-AUC | 비고 |
|---|---:|---:|---:|---:|---:|---|
| Dummy |  |  |  |  |  | 기준선 |
| Logistic Regression |  |  |  |  |  | 해석 용이 |
| Random Forest |  |  |  |  |  | 중요도 확인 |
| XGBoost/LightGBM |  |  |  |  |  | 성능 개선 |
| Top 30 Features Model |  |  |  |  |  | 검사 효율화 검토 |

## 4.5 Confusion Matrix 해석 문장

포트폴리오에는 단순히 표만 넣지 말고 해석 문장을 넣는다.

예시:

> 품질관리 관점에서는 Fail을 Pass로 예측하는 False Negative가 가장 위험하다고 판단했다. 따라서 Accuracy보다 Fail Recall을 우선 지표로 설정했으며, threshold를 조정해 Fail Recall을 높이는 대신 False Positive 증가 폭을 함께 확인했다.

---

# Part 5. 핵심 불량 인자 후보 도출

## 5.1 목표

모델링 이후 가장 중요한 단계다.

단순 ML 프로젝트와 반도체 품질/평가 프로젝트를 구분하는 지점은 **모델 성능이 아니라 해석과 원인 후보 도출**이다.

## 5.2 사용할 방법

| 방법 | 목적 |
|---|---|
| Logistic Regression coefficient | feature 영향 방향 확인 |
| Random Forest importance | 비선형 모델의 중요 feature 확인 |
| Permutation importance | 성능에 실질적으로 기여한 feature 확인 |
| SHAP | 개별 Fail 샘플의 예측 근거 설명 |
| 분포 비교 | 엔지니어가 이해 가능한 시각화 제공 |

## 5.3 핵심 후보 선정 기준

최종 핵심 feature 후보는 한 가지 기준만으로 선정하지 않는다.

아래 기준을 종합한다.

- 통계검정에서 유의한 차이를 보이는가?
- 모델 중요도 상위에 반복적으로 등장하는가?
- SHAP에서 Fail 예측에 강하게 기여하는가?
- Pass/Fail 분포 차이가 시각적으로 확인되는가?
- 결측 또는 이상치와 함께 품질 리스크를 만들 가능성이 있는가?

## 5.4 산출물 예시

`04_feature_importance_root_cause_candidate.ipynb` 마지막에 아래 표를 만든다.

| Feature | 분석 근거 | Fail에서의 경향 | 품질 관점 해석 | 후속 검증 제안 |
|---|---|---|---|---|
| feature_XX | SHAP 상위, 통계검정 유의 | Fail에서 값 증가 | 수율 저하 연관 후보 | 공정 Step/장비/소재 Lot 연계 분석 |
| feature_YY | Permutation importance 상위 | Fail에서 분산 증가 | 공정 변동성 후보 | 관리도 기반 모니터링 |
| feature_ZZ | 결측률 높고 Fail과 동시 발생 | 결측 동반 | 계측 신뢰성 이슈 가능 | 계측 Recipe 및 장비 로그 확인 |

## 5.5 면접용 표현

좋은 표현:

> 공개 데이터 특성상 feature명이 비식별화되어 있어 실제 공정 원인을 확정할 수는 없었습니다. 대신 통계검정, 모델 중요도, SHAP 분석을 종합해 Fail과 연관된 핵심 측정 인자 후보를 도출했고, 실제 엔지니어링 환경이라면 공정 Step, 장비 로그, 소재 Lot, 계측 이력과 연계해 추가 검증해야 한다고 정리했습니다.

피해야 할 표현:

> 머신러닝으로 불량 원인을 찾았습니다.

더 좋은 표현:

> 머신러닝과 통계 분석을 활용해 불량 원인 후보를 좁혔습니다.

---

# Part 6. 품질관리 / 모니터링 Rule 제안

## 6.1 목표

여기까지 하면 프로젝트가 평가및분석/품질관리 직무와 훨씬 강하게 연결된다.

목표는 다음이다.

- 핵심 feature 중심의 품질 모니터링 방안을 만든다.
- 이상치 발생 시 추가 검사 또는 Review가 필요하다는 Rule을 제안한다.
- 전체 feature를 모두 쓰지 않아도 Fail 검출이 가능한지 검토한다.

## 6.2 추천 분석

| 분석 | 설명 |
|---|---|
| 관리도(Control Chart) | 정상 샘플 기준 평균과 관리한계 설정 |
| Rolling Fail Rate | 시간 순서에 따른 Fail 비율 변화 확인 |
| Z-score 이상치 Flag | 핵심 feature가 정상 범위를 벗어나는 샘플 탐지 |
| IQR 기반 이상치 Rule | 비정규 분포 feature에 적용 |
| Top-N feature 모델 | 주요 feature만으로 Fail 검출 가능한지 검증 |
| Screening Rule | Fail 가능성이 높은 샘플을 추가 검사 대상으로 분류 |

## 6.3 관리도 접근 예시

정상 Pass 샘플을 기준으로 평균과 표준편차를 계산한다.

- UCL = mean + 3 * std
- LCL = mean - 3 * std

특정 핵심 feature가 UCL/LCL을 벗어나면 이상 샘플로 flagging한다.

포트폴리오 표현:

> 모델 중요도와 SHAP 분석에서 상위로 도출된 feature를 대상으로 정상 Pass 샘플 기준 관리한계를 설정했다. 관리한계를 초과하는 샘플은 추가 검사 대상으로 분류하는 Screening Rule을 제안했다.

## 6.4 Screening Rule 예시

```text
Rule 1. 핵심 feature 중 3개 이상이 관리한계를 벗어나면 추가 검사 대상으로 분류한다.
Rule 2. 모델 Fail probability가 0.35 이상이면 Review 대상으로 분류한다.
Rule 3. 결측률이 높은 특정 feature에서 결측이 발생하고 동시에 Fail probability가 높으면 계측 안정성 확인 대상으로 분류한다.
```

## 6.5 Top-N feature 모델 검토

전체 591개 feature를 모두 사용하는 모델과 Top 30개 feature만 사용하는 모델을 비교한다.

| 모델 | 사용 feature 수 | Fail Recall | Precision | PR-AUC | 해석 |
|---|---:|---:|---:|---:|---|
| Full Model | 591 |  |  |  | 전체 측정값 활용 |
| Top 50 Model | 50 |  |  |  | 검사 항목 축소 가능성 |
| Top 30 Model | 30 |  |  |  | 핵심 인자 중심 screening 가능성 |
| Top 10 Model | 10 |  |  |  | 성능 저하 여부 확인 |

면접용 표현:

> 전체 feature를 사용하는 모델과 Top-N feature 모델을 비교해, 핵심 측정 인자 중심으로도 Fail 검출 성능을 어느 정도 유지할 수 있는지 확인했습니다. 이는 평가 항목 최적화와 Test Screening 효율화 관점에서 의미가 있다고 판단했습니다.

---

# Part 7. 최종 산출물 구성

## 7.1 추천 폴더 구조

```text
semiconductor-yield-quality-analysis/
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_data_quality_check.ipynb
│   ├── 02_eda_fail_pattern_analysis.ipynb
│   ├── 03_modeling_fail_prediction.ipynb
│   ├── 04_feature_importance_root_cause_candidate.ipynb
│   └── 05_spc_monitoring_rule.ipynb
├── src/
│   ├── preprocessing.py
│   ├── modeling.py
│   └── visualization.py
├── reports/
│   ├── final_report.md
│   └── interview_summary_1page.pdf
├── requirements.txt
└── .gitignore
```

## 7.2 README 필수 구성

README에는 반드시 아래 항목을 넣는다.

```text
1. Background
2. Dataset
3. Problem Definition
4. Methodology
5. Results
6. Key Findings
7. Quality Monitoring Proposal
8. Limitations
9. Interview Talking Points
```

## 7.3 README 문장 템플릿

### Background

```text
반도체 제조에서는 공정 및 평가 데이터의 미세한 변화가 수율과 품질에 영향을 줄 수 있다. 특히 Fail 비율이 낮은 불균형 데이터에서는 단순 정확도보다 Fail을 조기에 탐지하고, 수율 저하와 연관된 핵심 인자 후보를 도출하는 것이 중요하다.
```

### Problem Definition

```text
본 프로젝트는 반도체 공정 평가 데이터를 기반으로 최종 Pass/Fail을 예측하고, Fail 발생과 연관성이 높은 핵심 측정 인자 후보를 도출하는 것을 목표로 한다.
```

### Methodology

```text
데이터 품질 진단, 결측/상수 feature 제거, class imbalance 대응, baseline 모델링, feature importance 및 SHAP 분석, 핵심 feature 기반 SPC 모니터링 Rule 제안 순서로 프로젝트를 수행했다.
```

### Limitations

```text
본 데이터는 feature명이 비식별화되어 있어 실제 공정명, 장비명, 소재 정보와 직접 연결할 수 없다. 따라서 분석 결과는 원인 확정이 아닌 수율 Fail과 연관된 후보 인자 도출로 해석해야 하며, 실제 양산 환경에서는 공정 Step, 장비 로그, 소재 Lot, 계측 이력과의 추가 검증이 필요하다.
```

---

# Part 8. 자소서와 면접 연결법

## 8.1 자소서용 문장

```text
반도체 유관 경험 부족을 보완하기 위해 공개 반도체 공정 데이터인 SECOM을 활용해 수율 Fail 예측 및 핵심 측정 인자 후보 도출 프로젝트를 수행했습니다. 단순 모델 정확도보다 품질 리스크 관점에서 Fail Recall과 False Alarm을 함께 평가했고, 결측/상수 feature 제거, 불균형 데이터 대응, feature importance 분석을 통해 수율 저하와 연관된 후보 인자를 도출했습니다. 이를 바탕으로 핵심 인자 중심의 모니터링 및 추가 검사 전략을 제안하며 평가/품질 데이터 분석의 전체 흐름을 경험했습니다.
```

## 8.2 면접 1분 설명

```text
저는 반도체 평가및분석 직무에서 중요한 역량이 평가 데이터를 해석하고 수율 저하 원인 후보를 논리적으로 좁히는 능력이라고 생각했습니다. 이를 보완하기 위해 SECOM 반도체 공정 데이터를 활용한 수율 Fail 예측 프로젝트를 진행했습니다. 먼저 결측률, 상수 feature, Pass/Fail 불균형을 진단하고 데이터 신뢰성을 확인했습니다. 이후 Accuracy보다 Fail Recall과 PR-AUC를 중심으로 모델을 평가했고, Logistic Regression, Random Forest, Gradient Boosting 모델을 비교했습니다. 마지막으로 SHAP과 permutation importance를 활용해 Fail과 연관된 핵심 측정 인자 후보를 도출하고, 해당 feature를 중심으로 관리도 기반 모니터링 Rule을 제안했습니다. 공개 데이터라 실제 공정 원인을 확정할 수는 없었지만, 평가 데이터 기반으로 불량 원인 후보를 좁히고 품질관리 방안까지 제안하는 흐름을 경험했다는 점에서 직무와 연결된 프로젝트라고 생각합니다.
```

## 8.3 면접 예상 질문과 답변 방향

| 예상 질문 | 답변 방향 |
|---|---|
| 왜 이 프로젝트를 했나요? | 반도체 유관 경험 부족을 보완하고 평가/품질 데이터 분석 흐름을 경험하기 위해 |
| 왜 Accuracy를 중심으로 보지 않았나요? | Fail class가 적어 Accuracy가 왜곡될 수 있고, 품질관리에서는 Fail 미검출이 더 위험하기 때문 |
| 어떤 전처리가 중요했나요? | 결측률 높은 feature 제거, 상수 feature 제거, train 기준 결측치 대체와 스케일링 |
| 데이터 누수는 어떻게 방지했나요? | train set에서만 imputer/scaler/feature selection을 fit하고 test에는 transform만 적용 |
| 모델 성능보다 중요하게 본 것은 무엇인가요? | Fail Recall, False Alarm, 핵심 인자 후보의 해석 가능성 |
| 원인을 찾았다고 볼 수 있나요? | 원인 확정은 아니며, 수율 저하와 통계적으로 연관된 후보 인자를 도출한 것 |
| 실제 회사 데이터라면 무엇을 더 보겠나요? | 공정 Step, 장비 로그, 소재 Lot, 계측 Recipe, Wafer map, 시간대별 생산 이력 |
| 평가및분석 직무와 어떻게 연결되나요? | 평가 데이터 분석, 수율 개선 항목 발굴, Test Screening, 품질 모니터링과 연결됨 |
| 품질관리 직무와 어떻게 연결되나요? | 통계적 품질관리, 관리도, 이상 감지, 추가 검사 Rule 제안과 연결됨 |

---

# Part 9. 코드 진행 체크리스트

## 9.1 1주차 체크리스트

- [ ] 데이터 다운로드
- [ ] GitHub repository 생성
- [ ] Python 가상환경 생성
- [ ] `requirements.txt` 작성
- [ ] 데이터 shape 확인
- [ ] Pass/Fail 개수 확인
- [ ] Fail 비율 계산
- [ ] Feature별 결측률 계산
- [ ] 결측률 높은 feature 리스트업
- [ ] 상수 feature 리스트업
- [ ] README에 문제 정의 작성

## 9.2 2주차 체크리스트

- [ ] Pass/Fail 분포 시각화
- [ ] 결측률 상위 feature 시각화
- [ ] Pass/Fail별 feature 분포 비교
- [ ] 평균 차이 상위 feature 도출
- [ ] 통계검정 수행
- [ ] 상관관계 분석
- [ ] PCA 또는 UMAP 시각화
- [ ] Top 20 후보 feature 정리

## 9.3 3주차 체크리스트

- [ ] train/test split
- [ ] preprocessing pipeline 구성
- [ ] Dummy Classifier 학습
- [ ] Logistic Regression 학습
- [ ] Random Forest 학습
- [ ] Gradient Boosting 계열 모델 학습
- [ ] Confusion Matrix 작성
- [ ] Fail Recall, Precision, PR-AUC 비교
- [ ] threshold 조정 실험

## 9.4 4주차 체크리스트

- [ ] Logistic coefficient 분석
- [ ] Random Forest feature importance 분석
- [ ] Permutation importance 분석
- [ ] SHAP 분석
- [ ] Top feature 분포 시각화
- [ ] 핵심 불량 인자 후보 표 작성
- [ ] 후속 검증 제안 작성

## 9.5 5주차 체크리스트

- [ ] 핵심 feature 관리도 작성
- [ ] Rolling Fail Rate 분석
- [ ] Z-score 이상치 flag 생성
- [ ] Screening Rule 제안
- [ ] Full feature 모델과 Top-N feature 모델 비교
- [ ] 품질관리 관점 해석 작성

## 9.6 6주차 체크리스트

- [ ] README 정리
- [ ] `final_report.md` 작성
- [ ] 면접용 1페이지 요약 작성
- [ ] 자소서 문장 작성
- [ ] GitHub 코드 정리
- [ ] 불필요한 output 제거
- [ ] 그래프와 표 저장
- [ ] 프로젝트 한계점 명확히 작성

---

# Part 10. 추천 기술 스택

## 10.1 Python 패키지

```text
pandas
numpy
matplotlib
scikit-learn
scipy
xgboost 또는 lightgbm
shap
jupyter
```

## 10.2 선택 패키지

```text
missingno
umap-learn
imbalanced-learn
streamlit
```

처음에는 선택 패키지까지 모두 쓰지 않아도 된다. 핵심은 pandas, scikit-learn, scipy, matplotlib, shap 정도다.

---

# Part 11. 확장 프로젝트 후보

메인 프로젝트를 완성한 뒤 시간이 남으면 아래 중 하나를 추가한다.

## 11.1 Wafer Map 불량 패턴 분류

### 데이터셋

WM-811K Wafer Map Dataset

### 직무 연결성

- SK하이닉스 기반기술 DMI
- 삼성 평가및분석의 불량 분석
- Wafer map 기반 defect pattern classification
- 이미지 기반 결함 분류

### 프로젝트 방향

- Wafer map 이미지 전처리
- Center, Donut, Edge-Ring 등 defect pattern 분류
- CNN 또는 classical ML 비교
- 불량 패턴별 공정 원인 후보 정리

### 난이도

중간 이상. 메인 프로젝트를 완료한 후 진행 권장.

## 11.2 장비 이상 감지 / RUL 예측

### 데이터셋

PHM 계열 반도체 장비 센서 데이터

### 직무 연결성

- 기반기술 Machine Engineering
- 설비/공정 데이터 분석
- 이상 감지
- 예지보전

### 프로젝트 방향

- 센서 시계열 데이터 전처리
- 이상치 탐지
- 고장 예측
- 주요 센서 feature importance 분석

### 난이도

높음. 첫 프로젝트로는 비추천.

## 11.3 Streamlit Dashboard

### 목적

분석 결과를 품질관리 대시보드 형태로 시각화한다.

### 구성 예시

- Pass/Fail 비율
- Fail probability 분포
- 핵심 feature 관리도
- Confusion Matrix
- Top feature importance
- Screening 대상 샘플 목록

### 직무 연결성

- 평가 데이터 리포팅
- 품질 모니터링
- 엔지니어링 커뮤니케이션

---

# Part 12. 프로젝트에서 반드시 피해야 할 실수

## 12.1 Accuracy만 강조하기

Fail 비율이 낮은 데이터에서는 Accuracy가 높아도 의미가 작을 수 있다. 반드시 Fail Recall과 Confusion Matrix를 함께 설명한다.

## 12.2 원인을 확정적으로 말하기

공개 데이터에서는 feature명이 비식별화되어 있다. 따라서 원인 확정이 아니라 원인 후보 도출이라고 표현해야 한다.

## 12.3 데이터 누수 발생

결측치 대체, 스케일링, feature selection을 전체 데이터에 대해 먼저 수행하면 데이터 누수가 발생한다. 반드시 train set 기준으로 fit한다.

## 12.4 모델만 만들고 끝내기

모델 성능만 제시하면 일반 데이터 분석 프로젝트처럼 보인다. 반드시 핵심 인자 후보, 품질관리 Rule, 후속 검증 제안을 포함한다.

## 12.5 반도체 직무 언어 없이 설명하기

단순히 “머신러닝을 했습니다”라고 말하지 않는다.

대신 다음 표현을 사용한다.

- 평가 데이터 분석
- 수율 Fail 예측
- 핵심 측정 인자 후보 도출
- 통계적 품질관리
- 관리도 기반 모니터링
- Test Screening
- 불량 원인 후보 검증
- 후속 공정/장비/소재 이력 연계 분석

---

# Part 13. 최종 보고서 목차

`reports/final_report.md`는 아래 목차로 작성한다.

```text
# Final Report

## 1. Project Background
## 2. Dataset Description
## 3. Problem Definition
## 4. Data Quality Check
    4.1 Class Imbalance
    4.2 Missing Values
    4.3 Constant Features
    4.4 Preprocessing Strategy
## 5. Exploratory Data Analysis
    5.1 Pass/Fail Distribution
    5.2 Feature Distribution Comparison
    5.3 Statistical Test
    5.4 Candidate Features
## 6. Modeling
    6.1 Baseline Model
    6.2 Class Imbalance Handling
    6.3 Model Comparison
    6.4 Threshold Analysis
## 7. Feature Importance and Root Cause Candidate Analysis
    7.1 Feature Importance
    7.2 SHAP Analysis
    7.3 Candidate Root Cause Features
## 8. Quality Monitoring Proposal
    8.1 Control Chart
    8.2 Screening Rule
    8.3 Top-N Feature Model
## 9. Limitations
## 10. Interview Talking Points
```

---

# Part 14. 첫 번째 실행 과제

가장 먼저 할 일은 아래 8개다.

```text
1. SECOM 데이터 다운로드
2. GitHub repository 생성
3. Python 환경 세팅
4. 데이터 shape 확인
5. Pass/Fail 개수 확인
6. feature별 결측률 계산
7. 상수 feature 개수 확인
8. README에 문제 정의 작성
```

첫 번째 체크포인트 결과는 아래 형식으로 정리한다.

```text
전체 샘플 수:
전체 feature 수:
Pass 개수:
Fail 개수:
Fail 비율:
결측값이 있는 feature 수:
결측률 50% 이상 feature 수:
상수 feature 수:
제거 후 남은 feature 수:
```

---

# Part 15. 이 프로젝트가 보여주는 직무 역량

| 직무 역량 | 프로젝트에서 보여주는 방식 |
|---|---|
| 평가 데이터 분석 | Pass/Fail 수율 라벨 기반 분석 |
| 품질관리 | Fail 검출, 관리도, 모니터링 Rule 제안 |
| 수율 개선 사고 | 핵심 불량 인자 후보 도출 |
| 통계적 접근 | 통계검정, SPC, PR-AUC, threshold 분석 |
| Test Engineering 관점 | Top-N feature 기반 screening 전략 |
| Data Science | ML 모델링, SHAP, feature importance |
| 문제 해결력 | 데이터 진단 → 가설 → 검증 → 개선안 제안 |
| 커뮤니케이션 | 원인 확정과 후보 도출의 차이를 명확히 설명 |

---

# Part 16. 최종 포트폴리오 핵심 메시지

프로젝트를 완성한 뒤 네가 가져가야 할 핵심 메시지는 다음이다.

> 저는 단순히 모델을 학습시키는 것이 아니라, 반도체 평가/품질 데이터에서 수율 Fail을 조기에 감지하고, 통계적/모델 기반 분석을 통해 불량 원인 후보를 좁히며, 핵심 인자 중심의 품질 모니터링 방안을 제안하는 흐름을 경험했습니다.

이 메시지가 SK하이닉스 기반기술, 삼성전자 Foundry 평가및분석, 품질관리 직무에 모두 연결된다.

---

## 마지막 메모

이 프로젝트의 완성도는 모델 성능보다 **보고서의 해석 품질**에서 결정된다.

반드시 아래 표현을 지킨다.

- “원인 확정”이 아니라 “원인 후보 도출”
- “정확도 향상”이 아니라 “Fail 검출과 품질 리스크 관리”
- “머신러닝 적용”이 아니라 “평가 데이터 기반 수율/품질 개선 항목 발굴”
- “결과가 좋다”가 아니라 “실제 양산 환경에서는 어떤 추가 검증이 필요한지 제안”

