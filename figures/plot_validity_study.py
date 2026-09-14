"""Plot every primary sufficient-controller outcome; no selected-success filter."""
from pathlib import Path
import csv,json,subprocess
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REV=HERE if HERE.name=='research_v34' else ROOT/'methods/validity_study'
OUT=ROOT/'output/jsac_submission/figures' if HERE.name=='research_v34' else HERE
rows=list(csv.DictReader((REV/'trial_results.csv').open()))
groups=[]
for B in [5000,14000]:
    rr=[r for r in rows if r['method']=='audited_sufficient' and int(r['budget'])==B]
    counts=[sum(int(r['immediate']) for r in rr),
            sum(int(r['issued']) and int(r['correct']) for r in rr),
            sum(not int(r['immediate']) and not int(r['issued']) and int(r['correct']) for r in rr),
            sum(int(r['unresolved']) for r in rr)]
    assert len(rr)==720 and sum(counts)==720
    assert sum(int(r['wrong']) for r in rr)==0
    groups.append(dict(budget=B,trials=len(rr),counts=counts))
(REV/'figure_data.json').write_text(json.dumps(groups,indent=2)+'\n')
plt.rcParams.update({'font.family':'serif','font.serif':['Times'],'text.usetex':True,
    'pgf.texsystem':'pdflatex','pgf.rcfonts':False,
    'pgf.preamble':r'\usepackage[T1]{fontenc}\renewcommand{\rmdefault}{ptm}\usepackage{amsmath,amssymb}',
    'font.size':8,'axes.labelsize':8,'xtick.labelsize':7,'ytick.labelsize':8,
    'axes.linewidth':.7,'savefig.facecolor':'white'})
colors=['#173B55','#087F78','#CBD6DE','#AB403B']
labels=['Immediate return','Issued plan','Adaptive discovery','Unresolved']
fig,ax=plt.subplots(figsize=(3.5,2.2))
fig.subplots_adjust(left=.19,bottom=.245,right=.97,top=.68)
for y,row in zip([1,0],groups):
    left=0
    for j,count in enumerate(row['counts']):
        width=100*count/row['trials']
        if count:
            ax.barh(y,width,left=left,height=.37,color=colors[j],edgecolor='white',linewidth=.3)
            if width>=4:
                ax.text(left+width/2,y,str(count),ha='center',va='center',fontsize=7.7,
                        color='white' if j<2 else '#173B55')
            else:
                ax.annotate(str(count),xy=(left+width/2,y+.18),xytext=(left-1,y+.36),
                    ha='right',va='center',fontsize=7,color=colors[j],
                    arrowprops={'arrowstyle':'-','color':colors[j],'lw':.55})
        left+=width
ax.set(xlim=(0,100),ylim=(-.43,1.52))
ax.set_yticks([1,0],['5,000','14,000'])
ax.set_ylabel('Cost budget',labelpad=4)
ax.set_xticks([0,25,50,75,100])
ax.set_xlabel(r'Decisions (\%)',labelpad=3)
ax.tick_params(axis='y',length=0)
ax.spines[['top','right','left']].set_visible(False)
fig.legend(handles=[Patch(facecolor=c,label=l) for c,l in zip(colors,labels)],
    loc='upper center',bbox_to_anchor=(.53,.995),frameon=False,ncol=2,
    fontsize=7.4,handlelength=1.1,columnspacing=1.1,handletextpad=.5,labelspacing=.5)
fig.text(.53,.045,'720 decisions per budget; labels give counts.',ha='center',fontsize=7.3)
target=OUT/'validity_completion_outcomes.pdf'
fig.savefig(target)
plt.close(fig)
subprocess.run(['/usr/bin/pdftoppm','-singlefile','-scale-to','1500','-png',str(target),str(REV/'validity_completion_outcomes')],check=True)
print(target)
