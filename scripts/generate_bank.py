"""Deterministic gas learning questions; no copied past papers or legal thresholds.
Decimal generation is checked separately in TypeScript using physical identities.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import json
ROOT = Path(__file__).resolve().parents[1]
D = lambda x: Decimal(str(x))
SUBJECTS = ['가스일반', '가스장치 및 기기', '가스안전관리']
# kind, topic, wording, values, evaluator, unit, worked formula
FAMILIES = [
('boyle','보일 법칙','온도가 일정한 이상기체의 절대압력은 {0} kPa, 부피는 {1} L이다. 절대압력을 {2} kPa로 바꾼 후 부피는?',lambda i:[100+5*i,20,200+10*i+(i%3)*20],lambda a,b,c:a*b/c,'L','P₁V₁=P₂V₂, V₂=P₁V₁/P₂'),
('charles','샤를 법칙','압력이 일정한 이상기체가 {0} K에서 {1} L이다. {2} K에서 부피는?',lambda i:[250+i,10+i%7,350+2*i],lambda a,b,c:b*c/a,'L','V₁/T₁=V₂/T₂, V₂=V₁T₂/T₁'),
('combined','결합 기체 법칙','일정량의 이상기체가 {0} kPa(절대), {1} L, 300 K에 있다. 200 kPa(절대), {2} K에서 부피는?',lambda i:[100+3*i,20+i%4,350+i],lambda a,b,c:a*b*c/(D(200)*D(300)),'L','P₁V₁/T₁=P₂V₂/T₂, V₂=P₁V₁T₂/(P₂T₁)'),
('partial','분압','이상 혼합기체의 총 절대압력이 {0} kPa이고 한 성분 몰분율이 {1}이다. 그 성분의 분압은?',lambda i:[200+10*i,D('0.10')+D(i%15)/100],lambda a,b:a*b,'kPa','pᵢ=yᵢP'),
('methaneOxygen','메탄 연소량','같은 온도·압력에서 메탄 {0} L를 완전연소시킬 때 필요한 순수 산소의 이론 부피는?',lambda i:[10+i*2],lambda a:a*2,'L','CH₄+2O₂→CO₂+2H₂O, 산소 부피=2×메탄 부피'),
('propaneOxygen','프로판 연소량','같은 온도·압력에서 프로판 {0} L를 완전연소시킬 때 필요한 순수 산소의 이론 부피는?',lambda i:[5+i*2],lambda a:a*5,'L','C₃H₈+5O₂→3CO₂+4H₂O, 산소 부피=5×프로판 부피'),
('heat','발열량','연료 기체 부피 {0} m³, 단위부피 발열량 {1} MJ/m³이다. 두 부피의 기준 상태가 같고 손실이 없을 때 총 발열량은?',lambda i:[2+i,D('35')+i%5],lambda a,b:a*b,'MJ','Q=V×H, m³×MJ/m³=MJ'),
('airRatio','공기비','이론공기량 {0} m³, 실제 공급 공기량 {1} m³이다. 공기비는?',lambda i:[20+i,30+2*i],lambda a,b:b/a,'배','공기비=실제 공급 공기량/이론공기량'),
('massFlow','질량유량','해당 운전 상태에서 기체 밀도 {0} kg/m³, 체적유량 {1} m³/h이다. 질량유량은?',lambda i:[D('1.1')+D(i)/100,20+i],lambda a,b:a*b,'kg/h','ṁ=ρQ'),
('velocity','유속','일정한 관 단면적이 {0} m²이고 그 상태의 체적유량은 {1} m³/s이다. 단면 평균 유속은?',lambda i:[D('0.01')+D(i)/1000,D('0.1')+D(i)/100],lambda a,b:b/a,'m/s','평균 유속 u=Q/A'),
('cylinderVolume','원통 체적','원통형 저장 공간의 내경은 {0} m, 유효 길이는 {1} m이다. 끝부분을 평면으로 가정하고 π=3.14일 때 내부 체적은?',lambda i:[D('1')+D(i)/20,2+i%5],lambda a,b:D('3.14')*a*a*b/4,'m³','V=(πd²/4)L'),
('expansion','선팽창','배관 원래 길이 {0} m, 선팽창계수 {1}×10⁻⁶/K, 온도 상승 {2} K이다. 자유 선팽창량은?',lambda i:[10+i,12,20+i%9],lambda a,b,c:a*b*c/1000,'mm','ΔL=αLΔT, m→mm로 1000배 변환'),
('pumpPower','유체 동력','비압축성 액체의 체적유량 {0} m³/s, 펌프 전후 압력 증가 {1} kPa이다. 높이·속도 변화가 없을 때 유체에 전달되는 동력은?',lambda i:[D('0.01')+D(i)/1000,100+5*i],lambda a,b:a*b,'kW','P=QΔp, m³/s×kPa=kW'),
('efficiency','효율','장치 입력 동력 {0} kW, 유효 출력 {1} kW이다. 효율은?',lambda i:[100+2*i,60+i],lambda a,b:b/a*100,'%','η=유효 출력/입력×100'),
('thermalLoad','현열','비열이 일정한 물질 {0} kg을 비열 {1} kJ/(kg·K), 온도 상승 {2} K로 가열한다. 상변화·열손실이 없을 때 필요한 열량은?',lambda i:[10+i,D('2'),20+i%7],lambda a,b,c:a*b*c,'kJ','Q=mcΔT'),
('vaporization','기화 열량','액화가스 {0} kg의 기화 잠열을 {1} kJ/kg으로 가정한다. 포화액을 같은 압력의 포화증기로 바꾸는 데 필요한 열량은?',lambda i:[2+i,350+i%11],lambda a,b:a*b,'kJ','Q=mL, 현열과 열손실은 제외'),
('ppm','농도 환산','체적 농도 {0} %를 ppm으로 환산하면? (같은 체적 기준)',lambda i:[D('0.01')+D(i)/1000],lambda a:a*10000,'ppm','1%=10,000 ppm, ppm=체적%×10,000'),
('mixtureFraction','완전 혼합','반응하지 않는 추적 기체 {0} L와 공기 {1} L를 같은 온도·압력에서 혼합한다. 부피가 가산된다고 가정할 때 추적 기체 농도는?',lambda i:[1+i,1000+10*i],lambda a,b:a/(a+b)*100,'%','농도=추적 기체 부피/(추적 기체+공기 부피)×100. 실제 누출 안전 판단용이 아닌 이상 혼합 계산'),
('airChanges','환기 횟수','체적 {0} m³인 빈 공간에 환기 유량 {1} m³/h를 공급한다. 명목 시간당 환기 횟수는?',lambda i:[100+5*i,300+20*i],lambda a,b:b/a,'회/h','명목 환기 횟수=환기 유량/공간 체적. 유효 환기 및 안전 판정과 구별'),
('idealDilution','이상 희석','추가 발생원이 없고 완전 혼합되는 공간의 초기 추적 기체 농도가 {0} ppm이다. 환기 후 농도가 초기의 {1}배라고 주어질 때 최종 농도는?',lambda i:[100+10*i,D('0.1')+D(i%7)/10],lambda a,b:a*b,'ppm','최종 농도=초기 농도×잔류 비율. 비율은 문제에서 주어진 값이며 안전 허용 기준이 아님'),
('pressureUnit','압력 단위','압력 {0} MPa를 kPa로 환산하면?',lambda i:[D('0.1')+D(i)/20],lambda a:a*1000,'kPa','1 MPa=1000 kPa'),
('absolutePressure','절대압력','대기압이 {0} kPa이고 게이지압력이 {1} kPa이다. 절대압력은?',lambda i:[100+i%4,10+3*i],lambda a,b:a+b,'kPa','절대압력=게이지압력+주위 대기압'),
('leakBalance','단순 물질수지','완전 밀폐된 이상 계산 공간에 반응하지 않는 추적 기체가 {0} L/min로 {1}분 동안 들어온다. 유출·반응이 없을 때 유입 부피 합계는? (모든 부피 동일 기준 상태)',lambda i:[D('0.1')+D(i)/10,2+i%8],lambda a,b:a*b,'L','유입 부피 합계=일정 유입 체적유량×시간. 실제 누출 대응·안전 판정용 모델이 아님'),
('oxygenMix','이상 혼합 산소','산소 체적분율 {0}인 공기 {1} L와 산소가 없는 불활성 기체 {2} L를 같은 온도·압력에서 혼합한다. 부피 가산을 가정한 산소 체적 농도는?',lambda i:[D('0.21'),100+5*i,20+i],lambda a,b,c:a*b/(b+c)*100,'%','산소 농도=기존 산소 부피/(공기+불활성 기체 부피)×100. 출입 안전 기준이 아닌 이상 혼합 계산'),
]
def fmt(x):
    s=format(D(x),'f'); return s.rstrip('0').rstrip('.') if '.' in s else s
def rounded(x):return x.quantize(D('.01'), rounding=ROUND_HALF_UP)
bank=[]
def add(subject,topic,text,choices,explanation,family=None,calculation=None):
    idx=len(bank); shift=idx%4
    choices=choices[shift:]+choices[:shift]
    answer=(4-shift)%4+1
    bank.append(dict(id=f'GAS-{idx+1:04}',subject=subject,topic=topic,question=text,choices=choices,answer=answer,explanation=explanation,difficulty='중' if family else '하',year=None,session=None,type='original',sourceUrl='https://github.com/YunSangYeong/Craftsman-Gas-CBT',verificationStatus='reviewed',reviewNote='AI 자체 작성. 내부 문장·정답·선택지 검토 및 계산형 독립 재계산. 외부 전문가 검수·공식 출제기준 대조 미완료. 저장소 URL은 작성 위치이며 외부 정답 증빙이 아님.',version='gas-main',rights='자체 제작 학습문항, CC BY 4.0, Craftsman-Gas-CBT contributors. 외부 기출 복제 없음.',**({'family':family,'calculation':calculation} if family else {})))
for subject,topic,text,choices,explanation in json.loads((ROOT/'scripts/concepts.json').read_text()):
    add(subject,topic,text,choices,explanation)
for f,(kind,topic,text,inputs,evaluate,unit,formula) in enumerate(FAMILIES):
    for i in range(40 if f<4 else 39):
        v=list(map(D,inputs(i))); result=rounded(evaluate(*v))
        candidates=[result,rounded(result*D('.5')),rounded(result*D('1.5')),rounded(result*2)]
        assert result>0 and len(set(candidates))==4
        question=text.format(*map(fmt,v))+' 소수점 셋째 자리에서 반올림하여 둘째 자리까지 구한다.'
        explanation=f'조건: '+', '.join(fmt(x) for x in v)+f'. 적용식: {formula}. 주어진 조건을 대입하면 {fmt(result)} {unit}이다. 소수점 셋째 자리에서 반올림한다. 이 문항은 같은 계산 유형의 숫자 조건 변형이며 법정 기준이나 실제 설비 안전 판정값을 제시하지 않는다.'
        add(SUBJECTS[f//8],topic,question,[f'{fmt(x)} {unit}' for x in candidates],explanation,'gas-'+kind,dict(kind=kind,values=[float(x) for x in v],result=float(result),unit=unit,precision=2))
assert len(bank)==1000
ids=set();texts=set()
for q in bank:
    fingerprint=''.join(q['question'].split())+'|'+ '|'.join(sorted(''.join(c.split()) for c in q['choices']))
    assert q['id'] not in ids and fingerprint not in texts
    ids.add(q['id']);texts.add(fingerprint)
(ROOT/'src/data/questions.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
print('Registered',len(bank),'questions;',len(FAMILIES),'calculation families; 940 variants; 60 concepts')
