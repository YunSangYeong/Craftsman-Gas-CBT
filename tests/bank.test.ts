import { describe, expect, it } from 'vitest';
import { BASE_BANK as bank, SUBJECTS, fingerprint, validateQuestion } from '../src/model';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
// Independent JS evaluation, not imported from the Python Decimal generator.
const evaluate: Record<string, (v:number[])=>number> = {
 boyle: ([p,v,p2])=>v/(p2/p),
 charles: ([t,v,t2])=>v*(t2/t),
 combined: ([p,v,t2])=>(p/200)*v*(t2/300),
 partial: ([p,y])=>p*y,
 methaneOxygen: ([v])=>v*2,
 propaneOxygen: ([v])=>v*5,
 heat: ([v,h])=>h*v,
 airRatio: ([theory,actual])=>actual/theory,
 massFlow: ([density,flow])=>flow*density,
 velocity: ([area,flow])=>flow/area,
 cylinderVolume: ([d,l])=>3.14*(d/2)**2*l,
 expansion: ([l,alpha,dt])=>l*(alpha*1e-6)*dt*1000,
 pumpPower: ([q,p])=>q*(p*1000)/1000,
 efficiency: ([input,output])=>100*output/input,
 thermalLoad: ([m,c,t])=>t*m*c,
 vaporization: ([m,h])=>h*m,
 ppm: ([percent])=>percent/100*1e6,
 mixtureFraction: ([gas,air])=>100/(1+air/gas),
 airChanges: ([volume,flow])=>flow/volume,
 idealDilution: ([initial,factor])=>factor*initial,
 pressureUnit: ([mpa])=>mpa*1e6/1000,
 absolutePressure: ([atm,gauge])=>gauge+atm,
 leakBalance: ([flow,time])=>time*flow,
 oxygenMix: ([fraction,air,inert])=>100*fraction/(1+inert/air),
};
function halfUp(n:number) { return Math.round((n+Number.EPSILON*Math.max(1,n))*100)/100; }
describe('가스 문제은행 실제 등록·중복·출처',()=>{
 it('1000개 고유 문항, 영역별 336/332/332, 연도·회차 없는 자체 제작',()=>{
  expect(bank).toHaveLength(1000);
  expect(new Set(bank.map(q=>q.id)).size).toBe(1000);
  expect(new Set(bank.map(fingerprint)).size).toBe(1000);
  expect(SUBJECTS.map(s=>bank.filter(q=>q.subject===s).length)).toEqual([336,332,332]);
  for(const q of bank){
   expect(()=>validateQuestion(q)).not.toThrow();
   expect(q).toMatchObject({type:'original',year:null,session:null,verificationStatus:'reviewed',version:'gas-main'});
   expect(q.rights).toContain('CC BY 4.0');
   expect(q.reviewNote).toContain('외부');
   expect(q.explanation.length).toBeGreaterThan(30);
  }
 });
 it('개념 60개와 24유형 940개 변형을 구별한다',()=>{
  expect(bank.filter(q=>!q.family)).toHaveLength(60);
  expect(bank.filter(q=>q.family)).toHaveLength(940);
  expect(new Set(bank.filter(q=>q.family).map(q=>q.family)).size).toBe(24);
  for(const kind of Object.keys(evaluate)){
   const family=bank.filter(q=>q.calculation?.kind===kind);
   expect([39,40]).toContain(family.length);
   expect(new Set(family.map(q=>JSON.stringify(q.calculation!.values))).size).toBe(family.length);
  }
 });
 it('결정적 재생성이 데이터 전체를 그대로 보존한다',()=>{
  const before=readFileSync('src/data/questions.json','utf8');
  execFileSync('python3',['scripts/generate_bank.py']);
  expect(readFileSync('src/data/questions.json','utf8')).toBe(before);
 });
 for(const q of bank.filter(q=>q.calculation)) it(`독립 수치·단위·선택지: ${q.id}`,()=>{
  const c=q.calculation!;
  expect(evaluate[c.kind]).toBeDefined();
  const result=halfUp(evaluate[c.kind](c.values));
  expect(c.result).toBeCloseTo(result,8);
  expect(q.choices[q.answer-1]).toBe(`${result} ${c.unit}`);
  const values=q.choices.map(choice=>Number(choice.slice(0,-(c.unit.length+1))));
  expect(values.every(Number.isFinite)).toBe(true);
  expect(new Set(values).size).toBe(4);
  expect(values.filter(v=>Math.abs(v-result)<1e-8)).toHaveLength(1);
  expect(q.explanation).toContain(`${result} ${c.unit}`);
 });
});
