### 1. Data Quality Diagnosis

분석 대상 SECOM 데이터는 1,567개 샘플과 590개 공정/센서 feature로 구성되어 있다.
최종 수율 label 기준 Pass 샘플은 1,463개, Fail 샘플은 104개로 Fail 비율은 6.64%에 불과하였다.
이는 반도체 품질 데이터에서 흔히 나타나는 class imbalance 문제로, 단순 Accuracy 기반 모델 평가는 부적절하다고 판단하였다.

또한 전체 590개 feature 중 538개 feature에서 일부 결측값이 확인되었으며,
결측률이 50% 이상인 feature는 28개였다.
값의 변화가 없는 상수 feature는 116개로 확인되었고,
이들은 Pass/Fail 구분에 기여하기 어렵기 때문에 모델링 전 제거 후보로 분류하였다.

결측률 50% 이상 feature와 상수 feature를 1차 제거 후보로 반영한 결과,
후속 분석 대상 feature는 446개로 정리되었다.
다만 결측 발생 자체가 공정/계측 이상과 연관될 가능성도 있으므로,
결측 feature의 최종 제거 여부는 Pass/Fail 분포 및 모델 성능 비교를 통해 추가 검토할 예정이다.