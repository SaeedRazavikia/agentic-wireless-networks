"""Standalone scientific plots for revision v31.

Run beside figure_data.json; if run in research_v31, export to the manuscript.
All chart values come from frozen, previously audited numerical studies.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Patch
from matplotlib.ticker import FuncFormatter
import numpy as np
import subprocess
from matplotlib.text import Text

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'figure_data.json').read_text())
OUT=HERE.parent/'output/jsac_submission/figures' if HERE.name=='research_v31' else HERE
plt.rcParams.update({'font.family':'serif','font.serif':['Times'],'text.usetex':True,'pgf.texsystem':'pdflatex','pgf.rcfonts':False,'pgf.preamble':r'\usepackage[T1]{fontenc}\renewcommand{\rmdefault}{ptm}\usepackage{amsmath,amssymb}','font.size':8,
    'pdf.fonttype':42,'ps.fonttype':42,'axes.linewidth':.7,'axes.labelsize':8,
    'xtick.labelsize':7,'ytick.labelsize':7,'savefig.facecolor':'white'})
NAVY='#123650';TEAL='#087F78';BLUE='#237BC1';AMBER='#B87708';GREY='#86A2B6';PALE='#E9EFF3'

def save(fig,name):
    for artist in fig.findobj(Text):
        artist.set_text(artist.get_text().replace('%',r'\%'))
    fig.savefig(OUT/(name+'.pdf'),dpi=300)
    subprocess.run(['/usr/bin/pdftoppm','-singlefile','-r','230','-png',str(OUT/(name+'.pdf')),str(OUT/name)],check=True)
    plt.close(fig)

# Former panel (b): its own one-column figure, with the same geometry.
fig,ax=plt.subplots(figsize=(3.5,2.65))
fig.subplots_adjust(left=.18,bottom=.24,right=.96,top=.94)
ax.set(xlim=(-1.3,2.4),ylim=(-1.3,2.4))
ax.add_patch(Polygon([(-1.3,-1.3),(0,-1.3),(0,0),(-1.3,0)],facecolor=PALE,edgecolor='none'))
xx=np.linspace(-1.3,2.4,500)
ax.fill_between(xx,1.05-xx,1.75-xx,color='#CFE5E4')
ax.plot(xx,1.05-xx,color=TEAL,lw=.9);ax.plot(xx,1.75-xx,color=TEAL,lw=.9)
ax.scatter([-.55,1.95],[1.95,-.55],s=19,color=NAVY,zorder=3)
ax.axhline(0,color=GREY,lw=.7);ax.axvline(0,color=GREY,lw=.7)
ax.set_xticks([-1,0,1,2]);ax.set_yticks([-1,0,1,2])
ax.set_xlabel('Radio-stage excess',labelpad=3);ax.set_ylabel('Server-stage excess',labelpad=4)
ax.text(-.68,-.64,'Jointly feasible\nrival',fontsize=7.3,ha='center',va='center',color=NAVY)
ax.text(1.44,1.66,'Retained\nconfidence band',fontsize=7.5,ha='center',color=TEAL)
ax.spines[['top','right']].set_visible(False)
fig.text(.53,.035,'Joint feasibility is excluded; the violated stage is unidentified.',ha='center',fontsize=7,color=NAVY)
save(fig,'joint_exclusion_geometry')

# Former panel (c): one-column replayed confidence intervals, not new data.
before,after=DATA['wireless_trace'][1],DATA['wireless_trace'][2]
fig,ax=plt.subplots(figsize=(3.5,2.7))
fig.subplots_adjust(left=.20,bottom=.28,right=.96,top=.88)
ax.set(xlim=(5.8,12.5),ylim=(-.40,4.08))
ax.axvline(9.5,color=AMBER,ls=(0,(3,2)),lw=1.1)
for y,i,r,c in [(3.3,4,before,GREY),(2.4,5,before,GREY),(.9,4,after,TEAL),(0.,5,after,TEAL)]:
    lo,hi=r['delay_lower'][i],r['delay_upper'][i]
    ax.plot([lo,hi],[y,y],color=c,lw=2.2,solid_capstyle='round')
    ax.plot([lo,hi],[y,y],marker='|',ls='none',color=c,ms=8)
ax.set_yticks([3.3,2.4,.9,0],['R2-S2','R2-S3','R2-S2','R2-S3'])
ax.set_xticks([6,8,9.5,12],['6','8','9.5','12'])
ax.tick_params(axis='y',length=0)
ax.spines[['top','right','left']].set_visible(False)
ax.set_xlabel('Mean completion time (ms)',labelpad=4)
ax.text(6.0,3.93,'Retained evidence',fontsize=8,color=GREY)
ax.text(6.0,1.52,'After targeted reports',fontsize=8,color=TEAL)
fig.text(.59,.945,'Current deadline: 9.5 ms',fontsize=8.2,color=AMBER,ha='center')
fig.text(.53,.080,r'$L_{22}=9.501>9.5;\quad U_{23}=9.434<9.5$',fontsize=8,ha='center')
fig.text(.53,.028,'Exclude R2-S2 and certify R2-S3.',fontsize=8.2,ha='center',color=TEAL,fontweight='bold')
save(fig,'wireless_confidence_trace')

# Column-width cost charts: all labels retain their final printed point size.
fig,ax=plt.subplots(figsize=(3.5,3.00))
fig.subplots_adjust(left=.055,bottom=.145,right=.96,top=.865)
ys=np.array([3.55,2.50,1.45,.40])
ratios=[100*r['proposed_mean']/r['baseline_mean'] for r in DATA['comparisons']]
labels=[
    'Two-stage witness allocation (64 decisions)',
    'Two-stage maximin allocation (32 decisions)',
    'Wireless maximin allocation (32 decisions)',
    'Scalar quotas with reuse (32 goal sequences)',
]
ax.barh(ys,np.full(4,100),height=.20,color=PALE,edgecolor=GREY,linewidth=.55)
ax.barh(ys,ratios,height=.20,color=TEAL,edgecolor=TEAL,linewidth=.55)
ax.set(xlim=(0,100),ylim=(-.08,4.10))
ax.set_yticks([])
ax.set_xticks([0,25,50,75,100])
ax.set_xlabel('Mean cost relative to the named comparator (%)',fontsize=7.6,labelpad=4)
ax.spines[['top','right','left']].set_visible(False)
for y,label,row in zip(ys,labels,DATA['comparisons']):
    ax.text(0,y+.30,label,fontsize=7.8,color=NAVY,ha='left',va='center')
    ax.text(0,y-.29,f"{row['baseline_mean']:,.2f} to {row['proposed_mean']:,.2f}",fontsize=7.5,color=NAVY,ha='left',va='center')
    ax.text(100,y-.29,f"{row['reduction_percent']:.1f}% lower",fontsize=8.1,fontweight='bold',color=TEAL,ha='right',va='center')
fig.legend(handles=[Patch(facecolor=PALE,edgecolor=GREY,label='Comparator = 100%'),Patch(facecolor=TEAL,label='Residual joint allocation')],
    loc='upper center',bbox_to_anchor=(.505,.985),ncol=2,frameon=False,fontsize=7.5,handlelength=1.1,columnspacing=1.0,handletextpad=.45)
save(fig,'certification_costs')

# The common subset and the full study share one linear axis and exact labels.
fig,ax=plt.subplots(figsize=(3.5,3.04))
fig.subplots_adjust(left=.245,bottom=.23,right=.985,top=.815)
ys=np.arange(4)[::-1];height=.23
allmeans=np.array([r['mean_expenditure_all'] for r in DATA['execution']])
subset=np.array([r['mean_expenditure_reached_completion'] for r in DATA['execution']])
b1=ax.barh(ys+.15,allmeans,height,color=BLUE,label='All 120 trials')
b2=ax.barh(ys-.15,subset,height,color=AMBER,label='Common 14-trial completion subset')
ax.set_xlim(0,46500);ax.set_ylim(-.5,3.50)
ax.set_yticks(ys,['Full quota','Block\nprefix','Proportional\nprefix','Goal-directed\nprefix'],fontsize=7.8)
ax.set_xlabel('Mean additional cost (modeled units)',fontsize=7.6,labelpad=4)
ax.xaxis.set_major_formatter(FuncFormatter(lambda value,pos:f'{value:,.0f}'))
ax.set_xticks([0,15000,30000]);ax.xaxis.grid(True,color='#DCE4E9',lw=.55);ax.set_axisbelow(True)
ax.tick_params(axis='y',length=0,pad=6)
ax.spines[['top','right','left']].set_visible(False)
for bars in [b1,b2]:
    ax.bar_label(bars,labels=[f'{bar.get_width():,.2f}' for bar in bars],padding=3,fontsize=7.3,color=NAVY)
fig.legend(handles=[b1,b2],labels=[b1.get_label(),b2.get_label()],loc='upper center',bbox_to_anchor=(.5,.995),ncol=1,frameon=False,fontsize=7.7,handlelength=1.5,labelspacing=.5)
fig.text(.5,.079,f"{DATA['execution_saving_subset_percent']:.1f}% lower in the common completion subset",fontsize=8.3,fontweight='bold',color=AMBER,ha='center')
fig.text(.5,.029,f"{DATA['execution_saving_all_percent']:.1f}% lower across all 120 trials",fontsize=8.3,fontweight='bold',color=BLUE,ha='center')
save(fig,'execution_stopping_costs')
print('Exported four vector figures; cost charts use native column-width typography.')
