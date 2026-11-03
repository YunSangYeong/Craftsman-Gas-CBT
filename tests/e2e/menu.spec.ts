import { expect, test, type Page } from '@playwright/test';

for (const viewport of [{width:390,height:480}, {width:740,height:360}]) {
 for (const input of ['wheel','touch'] as const) {
  test(`메뉴 실제 ${input} 위아래 입력 ${viewport.width}×${viewport.height}`, async ({page,isMobile})=>{
   test.skip(!isMobile, '터치 가능한 Pixel 7 에뮬레이션에서 검사');
   await page.setViewportSize(viewport);
   await page.goto('');
   await page.getByRole('button',{name:'메뉴 열기'}).click();
   const sidebar=page.locator('.sidebar');
   await expect(sidebar).toHaveClass(/open/);
   await expect.poll(()=>sidebar.evaluate(el=>el.getBoundingClientRect().x)).toBe(0);
   await expect(sidebar).toBeVisible();
   const initial=await sidebar.evaluate(el=>({height:el.clientHeight,content:el.scrollHeight,top:el.scrollTop}));
   expect(initial.content).toBeGreaterThan(initial.height);
   const session=await page.context().newCDPSession(page);
   async function scroll(direction:1|-1){
    if(input==='wheel'){
     await page.mouse.move(125,viewport.height/2);
     await page.mouse.wheel(0,direction*1800);
    } else {
     // Dispatch native touch start/move/end through Chromium's input pipeline.
     // Several bounded swipes keep the finger inside the short viewport.
     for(let swipe=0;swipe<5;swipe++){
      const start=direction===1?viewport.height*0.8:viewport.height*0.2;
      const end=direction===1?viewport.height*0.2:viewport.height*0.8;
      await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:125,y:start}]});
      for(let step=1;step<=12;step++){
       await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:125,y:start+(end-start)*step/12}]});
       await page.waitForTimeout(20);
      }
      await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
      await page.waitForTimeout(100);
     }
    }
   }
   await scroll(1);
   await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
   const reset=sidebar.getByRole('button',{name:'데이터 초기화',exact:true});
   const backup=sidebar.getByRole('button',{name:'학습 기록 백업',exact:true});
   await expect(reset).toBeInViewport();
   await expect(backup).toBeInViewport();
   const download=page.waitForEvent('download');
   if(input==='touch') await backup.tap(); else await backup.click();
   expect((await download).suggestedFilename()).toBe('gas-study-backup.json');
   if(input==='touch') await reset.tap(); else await reset.click();
   await expect(page.getByRole('dialog')).toBeVisible();
   await page.getByRole('button',{name:'돌아가기',exact:true}).click();
   await scroll(-1);
   await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBe(0);
   const dashboard=sidebar.getByRole('button',{name:'학습 대시보드',exact:true});
   await expect(dashboard).toBeInViewport();
   if(input==='touch') await dashboard.tap(); else await dashboard.click();
   await expect(sidebar).not.toHaveClass(/open/);
   await expect(page.getByRole('heading',{name:'가스기능사 필기 CBT',exact:true})).toBeVisible();
  });
 }
}

test('모든 화면 상단 배너 부재와 확대된 모바일 메뉴',async({page,isMobile})=>{
 await page.goto('');
 for(const name of ['학습 대시보드','실전 모의시험','랜덤 문제풀이','오답노트','북마크','학습 통계','문제은행 관리']){
  if(isMobile) await page.getByRole('button',{name:'메뉴 열기'}).click();
  await page.getByRole('navigation').getByRole('button',{name,exact:true}).click();
  await expect(page.locator('.criteria-note')).toHaveCount(0);
  await expect(page.getByLabel('학습 기준')).toHaveCount(0);
 }
 if(isMobile){
  await page.setViewportSize({width:390,height:480});
  await page.addStyleTag({content:'.sidebar {font-size:150%} .sidebar nav button {font-size:18px;min-height:65px}'});
  await page.getByRole('button',{name:'메뉴 열기'}).click();
  const sidebar=page.locator('.sidebar');
  await expect.poll(()=>sidebar.evaluate(el=>el.getBoundingClientRect().x)).toBe(0);
  await page.mouse.move(125,240);await page.mouse.wheel(0,2000);
  await expect(sidebar.getByRole('button',{name:'데이터 초기화',exact:true})).toBeInViewport();
  await page.mouse.wheel(0,-2000);
  await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBe(0);
  await expect(sidebar.getByRole('button',{name:'학습 대시보드',exact:true})).toBeInViewport();
 }
 await page.screenshot({path:`test-results/${isMobile?'mobile':'desktop'}-bank.png`,fullPage:true});
});
