const assert=require('node:assert/strict'),fs=require('node:fs'),e=require('./dist/engine.js'),d=JSON.parse(fs.readFileSync('./dist/data.json'));
const f={ward:'PHC-S',organism:d.organisms.indexOf('Escherichia coli'),specimen:'urine',sex:'ALL',age:'ALL',date:'2026-09-27'};
const result=e.compute(d,f),amp=result.metrics.find(a=>a.antibiotic_code==='AMP');
assert.equal(result.recent.length,74);assert.equal(amp.now.r,34);assert.equal(amp.status,'watch');assert(amp.q>.05);assert.equal(e.shift('2026-09-27',-27),'2026-08-31');
const filtered=e.compute(d,{...f,sex:'F',age:'65'});assert(filtered.recent.every(r=>r[6]==='F'&&r[7]>=65));
const earlier=e.compute(d,{...f,date:'2026-08-30'});assert(earlier.recent.every(r=>r[2]<='2026-08-30'));assert(!earlier.base.some(r=>r[2]>=e.shift('2026-08-30',-27)));
const rows=[['i1','p1','2026-09-01','W',0,'urine','F',60,{AMP:1},0,0,'c1'],['i2','p1','2026-09-02','W',0,'urine','F',60,{AMP:0},0,0,'c2'],['i3','p2','2026-09-03','W',0,'urine','F',60,{},0,0,'c3']];const co=e.cohort({rows},{...f,ward:'W',organism:0},'2026-09-01','2026-09-27');assert.equal(co.length,2);assert.deepEqual(e.counts(co,'AMP'),{n:1,r:1,s:0,rate:1});
assert(e.fisher({n:50,r:30},{n:500,r:50})<.00001);assert(e.fisher({n:50,r:0},{n:500,r:100})>.99);
for(const a of result.metrics){assert(a.q>=a.p-1e-10);const [l,h]=e.wilson(a.now.s,a.now.n);assert(l>=0&&h<=1&&l<=h);}
console.log('PASS: real-data counts, cohort filters, repeat removal, missing-test exclusion, date boundaries, replay cutoff, Fisher and interval sanity.');
