"""One bibliographic source generates both the paper and cite_check input."""
import json
from pathlib import Path
root=Path(__file__).resolve().parent
refs=json.loads((root/'references.json').read_text())
def tex(x):
    return x.replace('&',r'\&').replace('%',r'\%').replace('Γ',r'$\Gamma$').replace('‘', '`').replace('’', "'").replace('–','--')
lines=[r'\begin{thebibliography}{99}']
md=['# Bibliographic claims for cite_check','',
    'Generated from references.json, the same source as bibliography.tex.','']
for ref in refs:
    if 'doi' in ref:
        url='https://doi.org/'+ref['doi']; label='doi:'+ref['doi']
    else:
        url='https://arxiv.org/abs/'+ref['arxiv']; label='arXiv:'+ref['arxiv']
    lines += [r'\bibitem{'+ref['key']+'}',tex(ref['authors'])+'.',
              r'\emph{'+tex(ref['title'])+'}.',
              tex(ref['venue'])+f" ({ref['year']}).",
              r'\href{'+url+'}{'+tex(label)+'}.']
    md += ['- Title: '+ref['title']+'; Authors: '+ref['authors']+'; Year: '+str(ref['year'])+'; '+label.split(':')[0]+': '+url,'']
    if 'doi' in ref and 'arxiv' in ref:
        companion='https://arxiv.org/abs/'+ref['arxiv']
        lines += [r'Also \href{'+companion+'}{arXiv:'+ref['arxiv']+'}.']
        md += ['- Title: '+ref['title']+'; Authors: '+ref['authors']+'; Year: '+str(ref['arxiv_first_year'])+'; arXiv: '+companion, '']
lines += [r'\end{thebibliography}']
(root/'bibliography.tex').write_text('\n'.join(lines)+'\n')
(root/'REFERENCES.md').write_text('\n'.join(md)+'\n')
print(f'Generated {len(refs)} references from one source.')
