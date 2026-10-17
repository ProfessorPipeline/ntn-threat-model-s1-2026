"""Generate a portable read-only snapshot. Run from any working directory."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from ntn.repository import Repository
from ntn.server import CSV_FIELDS

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=ROOT / "data/ntn.sqlite3")
    args = parser.parse_args()
    repo = Repository(args.db)
    payload = json.dumps({"threats": repo.threats(), "references": repo.references(), "csv_fields": CSV_FIELDS}, ensure_ascii=False).replace("<", "\\u003c")
    svg = (ROOT / "web/architecture.svg").read_text(encoding="utf-8")
    html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>S1 NTN · Offline backup</title>
<style>body{font:14px "Segoe UI",Arial,sans-serif;color:#1c2e3c;background:#f3f6f8;margin:0}header{background:#132332;color:white;padding:30px max(24px,calc((100vw - 1100px)/2))}header p{color:#b7d2d5}main{max-width:1100px;margin:25px auto;padding:0 22px}h1{font-size:28px;margin:8px 0}h2{font-size:20px}p{line-height:1.7}.notice{background:#fff8e2;border:1px solid #e1ce96;padding:15px;border-radius:8px;font-size:12px}section,article{background:white;border:1px solid #dce5e9;border-radius:10px;padding:22px;margin:18px 0}svg{width:100%;height:auto}select,input,button{font:inherit;padding:10px;border:1px solid #cfdee3;border-radius:6px;margin:5px 10px 5px 0}button{background:#126b64;color:white;cursor:pointer}label{font-size:11px;display:inline-block}summary{cursor:pointer;font-size:16px;font-weight:600;padding:5px 0}small{color:#627584}b{color:#24564f}.badge{font-size:11px;background:#edf3ef;border-radius:5px;padding:5px 8px;display:inline-block;margin:10px 0}.evidence{background:#f7f9fa;padding:12px;border-radius:7px;font-size:12px;margin-top:9px}.muted{color:#627584}a{color:#126b64}table{border-collapse:collapse;width:100%}td,th{text-align:left;border-bottom:1px solid #ddd;padding:12px;font-size:12px}@media print{header{background:white;color:black}button,input,select{display:none}article,section{break-inside:avoid}}</style>
<header><small>READ-ONLY SEMINAR BACKUP / S1</small><h1>NTN threat model</h1><p>Portable catalogue and architecture. No Python or Docker required.</p></header><main>
<div class="notice">This is a fixed snapshot. It contains no completed independent scoring or invented evaluation results. Check the generation time before using it. The live database may have newer records.<br>Generated: TIMESTAMP</div>
<section><h2>Architecture · S1</h2>DIAGRAM<p>The gNB remains on the ground. F1 and F2 are physical segments of one access path. This is an existing 5G NTN baseline for future 6G discussion. No live attacks or RF measurements.</p></section>
<section><h2>Team-adapted priority method</h2><p>Attack feasibility × impact. Both use levels 1–4. Low 1–3 · Medium 4–7 · High 8–11 · Critical 12–16. Unscored records sort last.</p><p>The 4×4 matrix and bands are the team’s adaptation. Ansong et al. use a different matrix. Four levels use concrete criteria and avoid a neutral middle value. Priority is qualitative and confidence is separate.</p></section>
<section><h2>Threat catalogue</h2><label>Component<br><select id="component"><option value="">All components</option></select></label><label>STRIDE<br><select id="stride"><option value="">All categories</option></select></label><button id="export">Export selected CSV</button><p id="count" class="muted"></p><div id="records"></div></section>
<section><h2>Supplied references</h2><div id="sources"></div><p>Check the source register and review-pack notes for prepared locators and their limits. Student source validation remains pending.</p></section></main>
<script>const data=PAYLOAD;
const e=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const selected=()=>data.threats.filter(t=>(!component.value||t.components.includes(component.value))&&(!stride.value||t.stride===stride.value));
const component=document.getElementById('component'),stride=document.getElementById('stride');
for(const id of ['C1','C2','C3','C4','C5','C6'])component.add(new Option(id,id));
for(const s of ['Spoofing','Tampering','Repudiation','Information Disclosure','Denial of Service','Elevation of Privilege'])stride.add(new Option(s,s));
function render(){const items=selected();document.getElementById('count').textContent=items.length+' records shown';document.getElementById('records').innerHTML=items.map(t=>`<article><details ${t.id==='T-02'?'open':''}><summary>${e(t.id)} · ${e(t.title)}</summary><div class="badge">${t.score===null?'Unscored':e(t.score)+' · '+e(t.band)+' · F'+t.feasibility+' × I'+t.impact}</div><p>${e(t.description)}</p><p><b>Actor:</b> ${e(t.actor)}<br><b>Conditions:</b> ${e(t.conditions)}<br><b>Controls:</b> ${e(t.controls)}</p><p><b>F reason:</b> ${e(t.feasibility_reason)}<br><b>I reason:</b> ${e(t.impact_reason)}</p><p><b>Mappings:</b> ${e([...t.components,...t.assets,...t.flows,...t.boundaries].join(' · '))}</p><p><b>Confidence:</b> ${e(t.confidence)} · ${e(t.confidence_reason)}</p>${t.evidence.map(s=>`<div class="evidence"><b>${e(s.basis)} · ${e(s.reference_id||'No source')} · ${s.checked?'Student check recorded':'Student check pending'}</b><br>${e(s.note)}${s.locator?'<br>Locator: '+e(s.locator):''}</div>`).join('')}<h3>Candidate mitigations</h3>${t.mitigations.map(m=>`<p>${e(m.text)}<br><small>${e(m.reference_id||'Assumption')} · ${e(m.note)}</small></p>`).join('')}<p><small>${e(t.review_status)} · ${e(t.origin)}</small></p></details></article>`).join('');}
component.onchange=stride.onchange=render;render();
document.getElementById('sources').innerHTML=data.references.map(r=>`<p><b>${e(r.id)}</b> · ${e(r.citation)}${r.doi?'<br>DOI: '+e(r.doi):''}</p>`).join('');
document.getElementById('export').onclick=()=>{const keys=data.csv_fields;const cell=x=>{let raw=typeof x==='object'&&x!==null?JSON.stringify(x):String(x??'');if(/^\\s*[=+@-]/.test(raw))raw="'"+raw;return '"'+raw.replace(/"/g,'""')+'"';};const rows=[keys,...selected().map(t=>keys.map(k=>t[k]))];const blob=new Blob(['\\ufeff'+rows.map(r=>r.map(cell).join(',')).join('\\r\\n')],{type:'text/csv;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='s1-offline-threats.csv';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);};
</script></html>'''
    from ntn.repository import now
    html = html.replace("DIAGRAM", svg).replace("TIMESTAMP", now()).replace("PAYLOAD", payload)
    output = ROOT / "web/backup.html"
    output.write_text(html, encoding="utf-8")
    print(f"Read-only snapshot written: {output}")

if __name__ == "__main__":
    main()
