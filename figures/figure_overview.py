"""Vector scientific overview: schematic joint geometry and one frozen trace.

Run here, or from the packaged figures directory beside overview_data.json.
All displayed performance values come from the retained data.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

HERE=Path(__file__).resolve().parent
if (HERE/'restored_results_audit.json').exists():
    DATA=HERE/'restored_results_audit.json'
    OUT=HERE.parent/'output/jsac_submission/figures'
else:
    DATA=HERE/'overview_data.json'
    OUT=HERE
trace=json.loads(DATA.read_text())['wireless_trace']
before,after=trace[1],trace[2]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,
                     'pdf.fonttype':42,'ps.fonttype':42,'axes.linewidth':.65})
navy='#17354B'; teal='#16796F'; orange='#B56422'; muted='#60737F'; grey='#E7EBED'
fig=plt.figure(figsize=(7.2,4.25),facecolor='white')
canvas=fig.add_axes([0,0,1,1]); canvas.set(xlim=(0,1),ylim=(0,1));canvas.axis('off')
def txt(x,y,s,size=8,color=navy,**kw):
    return canvas.text(x,y,s,fontsize=size,color=color,**kw)
def box(x,y,w,h,title,body,edge=navy,fill='#F5F8FA',title_size=8.2,body_size=7.5):
    canvas.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.006,rounding_size=0.01',
                                  linewidth=.8,edgecolor=edge,facecolor=fill))
    txt(x+w/2,y+h*.73,title,title_size,ha='center',va='center',fontweight='bold',color=edge)
    txt(x+w/2,y+h*.30,body,body_size,ha='center',va='center',color=edge)
def arrow(x1,y1,x2,y2,color=navy,**kw):
    canvas.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=8,
                                   linewidth=.8,color=color,**kw))

txt(.015,.972,'(a) A goal-driven evidence loop',10,fontweight='bold',va='center')
box(.015,.775,.185,.13,'Goal changes',r'$24\;\to\;12.6\;\to\;9.5$ ms')
box(.258,.775,.200,.13,'P2  Reuse evidence','Same model-validity interval\nCounts, sums, operators',edge=teal,fill='#EFF8F5',body_size=6.8)
box(.516,.775,.205,.13,'P1  Check obligations','Own feasibility +\nexclude cheaper competitors')
box(.785,.775,.200,.13,'P3  Select a measurement','Target remaining gaps\nwithin shared resources',edge=orange,fill='#FCF5ED',title_size=7.0)
for a,b in [(.20,.258),(.458,.516),(.721,.785)]:arrow(a,.836,b,.836)
txt(.748,.851,'open',6.5,ha='center')
# Measurement feedback uses a separate upper route.
canvas.plot([.885,.885,.358],[.905,.940,.940],color=orange,lw=.8)
arrow(.358,.940,.358,.905,color=orange)
txt(.615,.944,'New physical report updates the evidence',7,color=orange,ha='center',va='bottom')
box(.516,.589,.205,.079,'Certified decision','All obligations pass',edge=teal,fill='#EFF8F5')
arrow(.618,.775,.618,.668,color=teal)
txt(.628,.712,'pass',6.8,color=teal)
box(.785,.589,.200,.079,'Unresolved','No admissible continuation',edge=muted,fill='#F3F4F5')
arrow(.885,.775,.885,.668,color=muted)
txt(.901,.709,'no legal\nreport',6.5,color=muted)
txt(.023,.695,'The agent chooses what to measure;\nthe verifier checks whether the evidence suffices.',8.1,
    va='center',linespacing=1.5)
txt(.023,.600,'P1: decision-relative observability\nP2: goal-dependent evidence value\nP3: information for instrument choice',7.1,
    va='center',linespacing=1.4,color=muted)
canvas.plot([.015,.985],[.538,.538],color='#D3DBE0',lw=.7)

txt(.015,.505,'(b) Joint exclusion can avoid stage diagnosis',8.5,fontweight='bold')
ax=fig.add_axes([.080,.176,.335,.290])
ax.set(xlim=(-1.3,2.4),ylim=(-1.3,2.4))
ax.add_patch(Polygon([(-1.3,-1.3),(0,-1.3),(0,0),(-1.3,0)],facecolor=grey,edgecolor='none'))
xx=np.linspace(-1.3,2.4,600)
ax.fill_between(xx,1.05-xx,1.75-xx,color='#CFE5E4',alpha=1)
ax.plot(xx,1.05-xx,color=teal,lw=.9)
ax.plot(xx,1.75-xx,color=teal,lw=.9)
ax.scatter([-.55,1.95],[1.95,-.55],s=16,color=navy,zorder=3)
ax.axhline(0,color=muted,lw=.65);ax.axvline(0,color=muted,lw=.65)
ax.set_xticks([-1,0,1,2]);ax.set_yticks([-1,0,1,2]);ax.tick_params(labelsize=6.6,length=2)
ax.set_xlabel('Radio-stage excess',fontsize=7,labelpad=2)
ax.set_ylabel('Server-stage excess',fontsize=7,labelpad=3)
ax.text(-.68,-.64,'Jointly feasible\ncompetitor',fontsize=6.7,ha='center',va='center',color=navy)
ax.text(1.45,1.58,'Retained\nconfidence band',fontsize=6.7,ha='center',color=teal)
ax.spines[['top','right']].set_visible(False)
txt(.015,.030,'The band excludes joint feasibility;\neither individual stage can still be feasible.',7.4,
    color=muted,linespacing=1.4)

txt(.495,.505,'(c) A recorded wireless decision at 9.5 ms',8.5,fontweight='bold')
ax2=fig.add_axes([.598,.188,.363,.247])
ax2.set(xlim=(5.8,12.5),ylim=(-.4,3.9))
ax2.axvline(9.5,color=orange,ls=(0,(3,2)),lw=1)
for y,i,rec,color in [(3.4,4,before,muted),(2.5,5,before,muted),(.9,4,after,teal),(0.,5,after,teal)]:
    lo,hi=rec['delay_lower'][i],rec['delay_upper'][i]
    ax2.plot([lo,hi],[y,y],color=color,lw=2,solid_capstyle='round')
    ax2.plot([lo,hi],[y,y],marker='|',ls='none',color=color,ms=7)
ax2.set_yticks([3.4,2.5,.9,0.],['R2-S2','R2-S3','R2-S2','R2-S3'])
ax2.set_xticks([6,8,9.5,12],['6','8','9.5','12'])
ax2.tick_params(axis='both',labelsize=6.8,length=2)
ax2.spines[['top','right','left']].set_visible(False)
ax2.tick_params(axis='y',length=0)
ax2.set_xlabel('Mean task delay (ms)',fontsize=7,labelpad=2)
ax2.text(6.1,3.9,'Retained evidence',color=muted,fontsize=6.9,va='bottom')
ax2.text(6.1,1.50,'After targeted reports',color=teal,fontsize=6.9,va='bottom')
txt(.495,.069,r'$L_{22}=9.501>9.5;\quad U_{23}=9.434<9.5$ ms.',7.4)
txt(.495,.030,'Exclude R2-S2 and certify R2-S3.',7.6,color=teal,fontweight='bold')

OUT.mkdir(parents=True,exist_ok=True)
fig.savefig(OUT/'joint_service_overview.pdf',dpi=300)
fig.savefig(OUT/'joint_service_overview.png',dpi=220)
plt.close(fig)
print(str(OUT/'joint_service_overview.pdf'))
