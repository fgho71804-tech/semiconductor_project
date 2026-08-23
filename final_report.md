# Semiconductor Yield Fail Prediction & Quality Data Analysis

## 1. Executive Summary

UCI SECOM 반도체 공정 데이터를 사용해 수율 Fail 위험을 분석하고, 품질관리 관점에서 우선 확인할 측정 feature 후보와 모니터링 방향을 도출했다.

전체 1,567개 샘플 중 Fail은 104개(6.64%)로 심한 클래스 불균형이 존재했다. 모델링 전에 결측·상수 feature를 진단해 590개 중 446개를 후속 분석 대상으로 정리했다. 단변량 통계, Random Forest 중요도, Test permutation importance를 교차 검증한 결과 `feature_59`, `feature_129`, `feature_125`가 네 가지 근거에서 모두 상위 후보로 확인됐다.

무작위 stratified Test에서 Recall 85.71%를 확보할 수 있었지만 Precision은 10.29%였고 False Alarm이 157건 발생했다. 시간순 미래 Test에서는 PR-AUC가 0.200에서 0.097로 하락했다. Recall 94.12%를 확보한 threshold에서는 False Alarm이 261건 발생했다. 따라서 현재 모델은 자동 판정 모델이 아니라 후속 확인 검사를 전제로 한 탐색적 스크리닝 도구로 해석해야 한다.

## 2. Business and Quality Question

핵심 질문은 다음과 같다.

> 수율 Fail을 가능한 한 놓치지 않으면서, 추가 확인이 필요한 측정 인자 후보와 False Alarm 비용을 함께 설명할 수 있는가?

반도체 품질관리에서는 전체 Accuracy보다 다음 항목이 중요하다.

- 실제 Fail 중 검출한 비율인 Fail Recall
- 경보 중 실제 Fail 비율인 Precision
- 불균형 데이터에 적합한 PR-AUC
- 놓친 Fail인 False Negative
- 추가 확인 비용을 만드는 False Positive
- 시간 변화에 따른 성능과 기준값의 안정성

## 3. Dataset

| 항목 | 내용 |
|---|---|
| Dataset | UCI SECOM Data Set |
| 기간 | 2008-07-19 ~ 2008-10-17 |
| 샘플 수 | 1,567 |
| 원본 feature 수 | 590 |
| Pass | 1,463 |
| Fail | 104 |
| Fail 비율 | 6.64% |
| 원본 label | `-1 = Pass`, `1 = Fail` |

feature 이름은 비식별화되어 있어 공정 step, 장비, 소재와 직접 연결할 수 없다.

## 4. Step 1 — Data Quality Diagnosis

| 진단 항목 | 결과 |
|---|---:|
| 결측값이 있는 feature | 538 |
| 결측률 50% 이상 feature | 28 |
| 상수 feature | 116 |
| 제거 후보 반영 후 feature | 446 |

Fail 비율이 6.64%이므로 모든 샘플을 Pass로 예측해도 Accuracy는 약 93.36%다. 따라서 Accuracy만 높은 모델은 품질관리 목적을 달성했다고 볼 수 없다.

결측률 50% 이상 feature와 상수 feature는 1차 제거 후보로 처리했다. 결측률과 상수 여부의 합집합을 제외한 446개 feature를 후속 분석에 사용했다. 결측치 대체는 모델 Pipeline 내부에서 Train 데이터로만 학습해 데이터 누수를 방지했다.

## 5. Step 2 — Fail Pattern EDA

446개 feature에 대해 Pass/Fail 표준화 평균 차이와 Mann-Whitney U 검정을 계산했다. 446개 동시 검정에 따른 우연한 발견을 줄이기 위해 Benjamini-Hochberg FDR을 적용했다.

- FDR 5% 기준 유의 후보: 20개
- 효과크기 상위: `feature_59`, `feature_103`, `feature_129`, `feature_28`, `feature_510`
- FDR 상위: `feature_59`, `feature_103`, `feature_247`, `feature_519`, `feature_510`

단변량 결과는 Fail과의 연관성 후보이며 실제 불량 원인이나 인과관계를 의미하지 않는다.

## 6. Step 3 — Baseline Fail Prediction

20% stratified Test를 분리하고 Train 데이터에서 5-fold × 3회 반복 교차검증을 수행했다.

| 모델 | Train CV PR-AUC | Train CV Fail Recall | Test PR-AUC |
|---|---:|---:|---:|
| Random Forest (balanced) | 0.198 | 0.000 | 0.200 |
| HistGradientBoosting (balanced) | 0.168 | 0.024 | 0.182 |
| Logistic Regression (balanced) | 0.163 | 0.305 | 0.118 |
| Dummy prior | 0.066 | 0.000 | 0.067 |

Train CV PR-AUC가 가장 높은 Random Forest를 선택했다. 기본 threshold 0.5에서는 Fail을 검출하지 못했으므로 Train out-of-fold 확률에서 Recall 80% 이상을 만족하는 threshold를 탐색했다.

### Stratified Test operating point

| 지표 | 결과 |
|---|---:|
| Threshold | 0.06 |
| Fail Recall | 85.71% |
| Precision | 10.29% |
| F1-score | 18.37% |
| PR-AUC | 0.200 |
| Balanced Accuracy | 66.07% |
| True Positive | 18 |
| False Negative | 3 |
| False Positive | 157 |
| True Negative | 136 |

Fail 검출률을 높일 수 있었지만 경보의 약 90%가 False Alarm이었다. 이 operating point는 자동 판정보다 스크리닝과 후속 확인 검사에 적합하다.

## 7. Step 4 — Feature Evidence and Monitoring Candidates

Random Forest Train impurity importance로 상위 후보를 정한 뒤 Test PR-AUC 감소 기반 permutation importance를 계산했다. 이를 Step 2 효과크기 및 FDR 순위와 결합했다.

| Feature | Fail 변화 방향 | 상위 근거 수 | 판단 |
|---|---|---:|---|
| `feature_59` | 증가 | 4/4 | 최우선 추가 검증 후보 |
| `feature_129` | 증가 | 4/4 | 모델·통계 근거가 일관된 후보 |
| `feature_125` | 감소 | 4/4 | Fail에서 낮아지는 공통 후보 |

복수 근거와 Train 결측률 20% 이하 조건을 만족한 모니터링 후보는 다음과 같다.

```text
feature_59, feature_129, feature_125, feature_205, feature_477,
feature_130, feature_33, feature_452, feature_510, feature_103
```

Pass Train 분포의 median과 MAD를 사용해 탐색적 스크리닝 범위를 계산했다. 이 범위는 실제 관리도 한계나 출하 spec이 아니다. 장비별 분포, 계측 신뢰성, 시간 안정성, 실제 공정 허용 범위를 확인한 뒤에만 운영 규칙으로 발전시켜야 한다.

## 8. Step 5 — Temporal Validation

timestamp 기준 앞 80%를 Train, 뒤 20%를 미래 Test로 분리했다.

시간순 Fail 비율은 다음처럼 변했다.

| 시간 구간 | Fail 비율 |
|---:|---:|
| 1 | 14.01% |
| 2 | 6.71% |
| 3 | 3.51% |
| 4 | 3.51% |
| 5 | 5.41% |

시간순 Train 내부 validation으로 threshold를 결정한 결과는 다음과 같다.

| 평가 방식 | Threshold | Recall | Precision | PR-AUC | FN | FP |
|---|---:|---:|---:|---:|---:|---:|
| Temporal threshold | 0.04 | 94.12% | 5.78% | 0.097 | 1 | 261 |
| Step 3 threshold 고정 | 0.06 | 64.71% | 6.40% | 0.097 | 6 | 161 |

시간순 Test PR-AUC는 무작위 Test의 0.200보다 크게 낮았다. 높은 Recall을 유지하려면 대부분의 Pass를 경보로 처리해야 했다. 이는 class 비율과 feature 분포 변화에 따라 threshold와 모델 성능이 불안정하다는 의미다.

## 9. Step 6 — Top-10 Feature Budget Efficiency

원본 590개 feature 중 품질 기준을 통과한 446개를 대상으로 Step 4 통합 근거 상위 10개를 누적 적용해 Balanced Random Forest의 성능과 비용을 비교했다.

상위 순위는 다음과 같다.

```text
1 feature_59   2 feature_129  3 feature_125  4 feature_205  5 feature_519
6 feature_477  7 feature_247  8 feature_130  9 feature_33  10 feature_452
```

| 누적 feature 수 | CV PR-AUC | Temporal PR-AUC | Fit 시간/fold | 평균 토큰/샘플 |
|---:|---:|---:|---:|---:|
| 1 | 0.1064 | 0.0535 | 2.383초 | 9.90 |
| 2 | 0.1300 | 0.0557 | 1.884초 | 18.49 |
| 3 | 0.1502 | 0.0744 | 1.556초 | 26.76 |
| 4 | 0.1913 | 0.0699 | 2.227초 | 34.75 |
| 5 | 0.1908 | 0.0782 | 1.849초 | 42.33 |
| 6 | 0.2107 | 0.0861 | 1.818초 | 51.22 |
| 7 | 0.2065 | 0.0922 | 1.990초 | 58.80 |
| 8 | 0.2107 | 0.1293 | 1.586초 | 67.67 |
| 9 | **0.2446** | 0.1553 | 1.964초 | 76.56 |
| 10 | 0.2444 | **0.1615** | 1.798초 | 85.46 |

토큰량은 feature 수에 거의 완전 선형으로 증가했다(R² 0.9996). CV PR-AUC는 전체적인 선형 상승 추세가 강했지만(R² 0.9174), 5·7·10개 구간에서 성능이 정체 또는 하락해 단조 선형 관계는 아니었다. 학습시간과 추론시간은 feature 수와 선형 관계가 없었다. 작은 feature 집합에서는 tree 분기 구조와 시스템 변동이 feature 수 자체보다 실행시간에 더 큰 영향을 준 것으로 해석한다.

평균 CV PR-AUC 최고점과 one-standard-error rule 모두 9개 feature를 선택했다. 10번째 `feature_452`를 추가하면 전체 데이터 입력량이 119,963에서 133,908 토큰으로 11.6% 증가하지만 CV PR-AUC는 0.24457에서 0.24437로 소폭 감소했다. 따라서 CV 성능과 토큰 효율을 함께 고려한 공식 optimum은 9개다. Temporal PR-AUC는 10개에서 0.0062 높으므로 미래 안정성을 중시한다면 추가 rolling backtest가 필요하다.

Random Forest는 실제 LLM 토큰을 소비하지 않는다. 토큰값은 각 샘플의 feature-value를 소수점 6자리 compact JSON으로 직렬화하고 `cl100k_base` tokenizer로 계산한 입력 footprint이며, 고정 prompt overhead는 제외했다.

## 10. Quality Monitoring Proposal

현재 결과를 실제 업무에 적용한다면 다음 단계의 스크리닝 구조가 적절하다.

1. 상위 모니터링 feature의 결측률과 분포 drift를 먼저 감시한다.
2. 모델 확률과 개별 feature 이상 신호를 함께 사용해 검토 대상을 선별한다.
3. 모델 경보를 즉시 불량 판정으로 사용하지 않고 후속 계측·공정 이력 확인 대상으로 보낸다.
4. 기간별 Recall, Precision, False Negative, False Alarm을 모니터링한다.
5. threshold는 놓친 Fail 비용과 확인 검사 비용을 반영해 승인한다.
6. rolling backtest를 통해 재학습 및 threshold 재조정 주기를 결정한다.

## 11. Limitations

- feature 비식별화로 물리적 원인을 확정할 수 없다.
- Fail 표본이 104개뿐이라 성능과 중요도 추정의 분산이 크다.
- Temporal validation도 약 3개월 데이터의 단일 분할이다.
- Random Forest impurity importance는 연속형·상관 feature에 편향될 수 있다.
- permutation importance는 Test Fail 21개에 민감하다.
- 실제 장비, lot, wafer, 공정 step 단위 group 정보가 없어 group leakage를 검증할 수 없다.
- 후보 monitoring limit은 실제 spec이나 통계적 관리한계가 아니다.

## 12. Conclusion

이 프로젝트의 핵심 성과는 높은 Accuracy를 만드는 것이 아니라 품질 데이터의 현실적인 제약을 확인하고 Fail 검출과 False Alarm 사이의 trade-off를 정량화한 것이다.

모델은 무작위 Test에서 Fail 21건 중 18건을 검출했지만 False Alarm 157건을 발생시켰다. 시간순 Test에서는 성능이 더 낮아졌고, Recall 94.12%를 확보하기 위해 False Alarm 261건을 허용해야 했다. 따라서 현재 결과는 자동 판정 모델이 아니라 추가 확인 검사를 지원하는 위험 스크리닝과 원인 후보 우선순위화 도구로 해석하는 것이 타당하다.

## 13. Interview Talking Points

### 60-second summary

> UCI SECOM 반도체 공정 데이터로 수율 Fail 예측과 품질 데이터 분석 프로젝트를 수행했습니다. 먼저 1,567개 샘플 중 Fail이 104개로 6.64%에 불과한 불균형 구조를 확인했고, 결측률이 높은 feature와 상수 feature를 진단해 분석 대상을 446개로 정리했습니다. 모델 평가는 Accuracy가 아니라 Fail Recall과 PR-AUC, False Alarm을 중심으로 설계했습니다. Random Forest의 threshold를 Train 데이터에서 조정해 무작위 Test Fail 21건 중 18건을 검출했지만 False Alarm이 157건 발생했습니다. 이후 시간순 검증에서는 PR-AUC가 0.097로 하락해 drift 위험을 확인했습니다. 또한 통계 검정과 모델 중요도를 교차 검증해 feature_59, feature_129, feature_125를 우선 확인 후보로 도출했습니다. 결과를 실제 원인으로 단정하지 않고, 후속 계측과 공정 이력 검증이 필요한 스크리닝 후보로 제안한 것이 이 프로젝트의 핵심입니다.

### Follow-up points

- 왜 Accuracy를 사용하지 않았는가: 모든 샘플을 Pass로 예측해도 약 93.36%이기 때문이다.
- 왜 Random Forest를 선택했는가: Train 반복 CV PR-AUC가 비교 모델 중 가장 높았기 때문이다.
- 왜 threshold를 낮췄는가: 기본 0.5에서는 Fail을 거의 검출하지 못했기 때문이다.
- 모델이 충분히 좋은가: 아니다. Recall은 높일 수 있지만 Precision과 시간 안정성이 낮다.
- 분석 결과를 어떻게 활용할 수 있는가: 자동 판정이 아니라 후속 확인 대상을 줄이는 스크리닝과 feature 검토 우선순위화에 활용한다.
