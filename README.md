# JaneStreetKaggle


## idea

- 시각화를 통해서 feature간 상관관계가 있음을 확인함. 
    - 횡단면 종단면 상관없이 그냥 feature간 상관관계가 있는 것 같음. 
    - 해당 feature에 대해서 차원축소 or drop 진행
    - 존재함!
    - target value와의 corr 측정

- responder6을 직접예측하는 건 어려울 수 있음.
    - responder6과 responder3은 약간의 상관관계가 존재함
    - responder3과 responder0은 약간의 상관관계가 존재함
    - responder0과 feature들은 약간의 상관관계가 존재함
    
    - -> responder0을 BootStrapping 헐 수 있지 않을까?
        - 좀 귀찮아 지긴함. 
        - 경험상 큰 임팩트는 없던것 같긴함. 

- 데이터는 횡단면 종단면 모두 존재함.

- 횡단면 분석은 symbol
    - 만약 비슷한 symbol이 있다면 통합
        - 다만 이 가설이 성립하려면 data가 비슷할 때 output이 비슷해야함. -> 추가분석 진행 
        - ## 어떻게 해야할까??
            1. feature수 줄이기 
                - 어떻게 줄일지 의논해보기
                - pca, corr기반, svd, auto-encoder
            2. cos 유사도, clustering 진행 
                - 나는 방법 잘 모르겠는데 필요하다고 생각함
                - 하지만 만약 오래걸리는 계산에 비해서 임팩트가 적다면 패스해도 된다는 의견이 있지않을까..
            3. 분산분석 & 비모수검정 & t-test 진행? 
                



- 종단면 분석은 time
    - 내 생각에는 시계열 예측의 정확도를 높이기 위해서 각 symbol에 대한 look-back window를 줘야할 것 같음. 
    - 만약 정상시계열을 가지는 feature가 있다면 powerful할 것 같음!
        - symbol별로 feature 정상성 분석 


