from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

root=Path(__file__).resolve().parent.parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(7.25,2.0))
ax.set(xlim=(-.05,10.5),ylim=(-.58,2.18));ax.axis('off')
def box(x,y,text,w=2.05,h=.6,fill='#f3f6f8'):
 ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.03,rounding_size=.055',lw=.85,edgecolor='#263d4c',facecolor=fill))
 ax.text(x,y,text,ha='center',va='center',fontsize=9)
def arrow(a,b,label=None,offset=(0,0)):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=9,lw=.9,color='#263d4c'))
 if label:ax.text((a[0]+b[0])/2+offset[0],(a[1]+b[1])/2+offset[1],label,ha='center',va='center',fontsize=7.7)
box(1.1,1.62,'Goal and context')
box(3.7,1.62,'Operating proposal')
box(6.3,1.62,'Common verifier',fill='#e2eef4')
box(9.0,1.62,'Certified answer')
box(3.7,.24,'Evidence memory\nReports and epoch')
box(6.3,.24,'Acquisition controller\nand resource gate')
box(9.0,.24,'Physical probes')
arrow((2.16,1.62),(2.64,1.62))
arrow((4.76,1.62),(5.24,1.62))
arrow((7.36,1.62),(7.94,1.62),'passes',(0,.2))
arrow((6.3,1.29),(6.3,.57),'needs evidence',(.72,0))
arrow((4.0,.57),(5.46,1.29),'retained data',(-.22,.10))
arrow((4.76,.24),(5.24,.24))
arrow((7.36,.24),(7.94,.24))
# A routed report-return edge avoids crossing any node or label.
ax.plot([9,9,3.7],[ -.10,-.48,-.48],lw=.9,color='#263d4c')
arrow((3.7,-.48),(3.7,-.10))
ax.text(6.35,-.36,'new physical reports',ha='center',va='center',fontsize=8)
ax.text(1.13,.3,'Unresolved when\nthe procedure cannot\ncertify within its limits',ha='center',va='center',fontsize=8,color='#364b58')
fig.subplots_adjust(left=.005,right=.995,top=.995,bottom=.015)
out=root/'figures/agent_architecture.pdf'
fig.savefig(out,transparent=False)
fig.savefig(root/'figures/agent_architecture.png',dpi=180)
plt.close(fig)
print('Architecture figure generated.')
