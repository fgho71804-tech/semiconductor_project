# Semiconductor Yield Fail Prediction & Quality Data Analysis

반도체 공정 평가 데이터 기반 수율 Fail 예측 및 품질 데이터 분석 프로젝트입니다. UCI Machine Learning Repository의 SECOM 데이터셋을 사용해 데이터 품질을 진단하고, Fail과 통계적으로 연관된 측정 feature 후보를 선별하며, 이후 Fail 검출 중심의 예측 모델과 품질 모니터링 방안을 설계합니다.

## 분석 목표

1. 결측·상수 feature와 클래스 불균형을 진단합니다.
2. Pass/Fail 간 차이가 큰 측정 feature 후보를 선별합니다.
3. Accuracy보다 Fail Recall, Precision, PR-AUC, Balanced Accuracy를 중심으로 모델을 평가합니다.
4. 분석 결과를 실제 원인 확정이 아닌 추가 검증이 필요한 품질 이상 후보로 해석합니다.

## 데이터

- 데이터셋: SECOM Data Set
- 출처: UCI Machine Learning Repository
- Feature URL: <https://archive.ics.uci.edu/ml/machine-learning-databases/secom/secom.data>
- Label URL: <https://archive.ics.uci.edu/ml/machine-learning-databases/secom/secom_labels.data>
- 파일: `secom.data`, `secom_labels.data`
- 원본 라벨: `-1 = Pass`, `1 = Fail`
- 분석 라벨: `is_fail = 0`은 Pass, `is_fail = 1`은 Fail

원본 파일은 저장소에 올리지 않습니다. 두 파일을 `data/raw/`에 배치한 뒤 노트북을 실행합니다.

## 프로젝트 구조

```text
.
├── data/raw/                         # 원본 데이터(버전 관리 제외)
├── notebooks/
│   ├── 00_environment_test.ipynb
│   ├── 01_data_quality_check.ipynb
│   └── 02_eda_fail_pattern_analysis.ipynb
├── reports/
│   └── step1_summary.csv
├── src/
│   └── secom_analysis.py
├── .gitignore
├── README.md
└── requirements.txt
```

## 실행 방법

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

노트북은 `00` → `01` → `02` 순서로 실행합니다. `01`은 Step 1 보고서 CSV를, `02`는 평균 차이와 통계 검정 기반 feature 후보 CSV를 생성합니다.

## Step 1. Data Quality Check Result

SECOM 반도체 공정 데이터를 대상으로 모델링 전 데이터 품질 진단을 수행했습니다.

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
| 제거 후보 반영 후 분석 feature 수 | 446 |

### Key Findings

1. Fail 비율은 6.64%로 심한 클래스 불균형이 존재합니다. 모든 샘플을 Pass로 예측해도 Accuracy가 93.36%이므로 Accuracy만으로 모델을 평가하면 안 됩니다.
2. 후속 모델은 Fail Recall, Precision, F1-score, PR-AUC, Balanced Accuracy와 Confusion Matrix를 함께 평가해야 합니다.
3. 590개 feature 중 538개에 일부 결측값이 있습니다. 결측률 50% 이상인 28개 feature는 측정 신뢰성이 낮은 후보로 분류합니다.
4. 값의 변화가 없는 상수 feature 116개는 Pass/Fail 구분에 기여하지 않아 제거 후보로 분류합니다.
5. 두 제거 조건의 합집합을 제외하면 후속 분석 대상은 446개 feature입니다.

### Interpretation

이 데이터는 실제 반도체 평가·품질 데이터처럼 결측값, 불균형 클래스, 고차원 feature 구조를 가집니다. 따라서 데이터 품질 진단과 전처리 기준 수립이 모델링보다 먼저 필요합니다. 후속 분석에서는 정상 샘플 예측 정확도뿐 아니라 Fail 검출률과 False Alarm의 균형을 중점적으로 평가합니다.

## Step 2. Fail Pattern EDA Result

Step 1에서 선별한 446개 feature를 대상으로 Pass/Fail 간 표준화 평균 차이와 Mann-Whitney U 검정을 계산했습니다. 446개 동시 검정에 따른 우연한 발견을 줄이기 위해 Benjamini-Hochberg 방식으로 FDR을 보정했습니다.

- 분석 feature 수: 446개
- FDR 5% 기준 유의 feature 후보: 20개
- 효과크기 상위 후보: `feature_59`, `feature_103`, `feature_129`, `feature_28`, `feature_510`
- FDR 상위 후보: `feature_59`, `feature_103`, `feature_247`, `feature_519`, `feature_510`

`feature_59`와 `feature_103`은 효과크기와 통계적 유의성 양쪽에서 모두 상위권이므로 우선 모니터링 후보입니다. 다만 이 분석은 단변량 연관성 분석이며, 결측 대체 방식·공정 시간 변화·feature 간 상관관계와 모델 기반 중요도를 함께 검증해야 합니다.

## 해석상 주의점

SECOM feature 이름은 비식별화되어 있으므로 통계적으로 유의한 feature를 실제 물리 공정 원인으로 단정할 수 없습니다. 결과는 공정 엔지니어가 설비·공정 이력과 함께 추가 검증할 측정 인자 후보로 사용합니다.
