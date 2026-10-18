from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})
A=Path('assets'); dark='#14263D'; teal='#087F8C'; blue='#2764B5'; orange='#C5631C'
def box(ax,xy,w,h,title,subtitle='',color=blue):
 x,y=xy
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.14',facecolor='#F4F8FC',edgecolor=color,lw=1.5))
 ax.text(x+w/2,y+h*.65,title,ha='center',va='center',fontsize=12,fontweight='bold',color=dark)
 if subtitle: ax.text(x+w/2,y+h*.29,subtitle,ha='center',va='center',fontsize=9,color='#40566C')
def arrow(ax,a,b): ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=15,lw=1.5,color='#6A8195'))
def save(fig,name):
 for ext in ['png','svg']: fig.savefig(A/f'{name}.{ext}',dpi=180,bbox_inches='tight',facecolor='white')
 plt.close(fig)
fig,ax=plt.subplots(figsize=(12,9)); ax.set(xlim=(0,12),ylim=(0,9)); ax.axis('off')
ax.text(.2,8.7,'PATTERN SHIELD',fontsize=23,fontweight='bold',color=dark)
ax.text(.2,8.25,'Two representations. One request classifier.',fontsize=13,color='#40566C')
box(ax,(4,7),4,.8,'Request text','Offline input; no requests are sent',teal)
box(ax,(.4,5.55),5,.9,'Normalize + encode','Up to two decoding passes; first 256 UTF-8 bytes')
box(ax,(6.6,5.55),5,.9,'Statistical feature extraction','8 lexical features; at most 16,384 characters',teal)
arrow(ax,(5,7),(2.9,6.5)); arrow(ax,(7,7),(9.1,6.5))
box(ax,(.4,4.15),5,.9,'Token + position embeddings','48 dimensions; token 0 reserved for padding')
box(ax,(6.6,4.15),5,.9,'Standardize features','Scaler fitted on training requests only',teal)
arrow(ax,(2.9,5.5),(2.9,5.1)); arrow(ax,(9.1,5.5),(9.1,5.1))
box(ax,(.4,2.75),5,.9,'Transformer + masked pooling','2 encoder layers; 4 heads; 48-value representation')
arrow(ax,(2.9,4.1),(2.9,3.7))
box(ax,(6.6,2.75),5,.9,'Concatenate + classification head','48 learned values + 8 features = 56 values',teal)
arrow(ax,(5.45,3.2),(6.55,3.2)); arrow(ax,(9.1,4.1),(9.1,3.7))
box(ax,(6.6,1.3),5,.95,'Benign / SQLi / XSS','Softmax scores + validation-selected alert threshold',orange)
arrow(ax,(9.1,2.7),(9.1,2.3))
ax.text(.5,1.65,'64,579 trainable parameters\nTrained from scratch\nNo pretrained language model',fontsize=12,color=dark,linespacing=1.6)
ax.text(.2,.3,'Research prototype • Synthetic default data • Scores are not calibrated attack probabilities',fontsize=11,color='#40566C')
save(fig,'architecture')
fig,ax=plt.subplots(figsize=(12,8)); ax.set(xlim=(0,12),ylim=(0,8)); ax.axis('off')
ax.text(.2,7.6,'EVALUATION WITHOUT TEST-SET TUNING',fontsize=20,fontweight='bold',color=dark)
box(ax,(3.5,6.05),5,1,'Assign templates to splits','Then generate variants and remove canonical duplicates',teal)
for x,title,sub in [(.25,'Train • 1,467','Fit model, scaler and baseline'),(4.25,'Validation • 360','Select checkpoint and alert threshold'),(8.25,'Test + challenge • 750','Evaluate only after selection')]:
 box(ax,(x,3.8),3.5,1.15,title,sub,color=blue)
 arrow(ax,(6,6),(x+1.75,5))
arrow(ax,(3.8,4.3),(4.2,4.3)); arrow(ax,(7.8,4.3),(8.2,4.3))
box(ax,(3.5,1.7),5,1.1,'Review errors and report limitations','No model or threshold fitting on test/challenge',orange)
arrow(ax,(10,3.75),(8.1,2.85))
ax.text(.3,.6,'Challenge results measure limited held-out-template generalization—not zero-day detection.',fontsize=12,color='#40566C')
save(fig,'evaluation_flow')
m=json.loads(Path('results/metrics.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(12,5))
x=[0,1]; width=.32
axes[0].bar([v-width/2 for v in x],[m[s]['transformer_macro_f1'] for s in ['test','challenge']],width,label='Transformer',color=blue)
axes[0].bar([v+width/2 for v in x],[m[s]['baseline_macro_f1'] for s in ['test','challenge']],width,label='TF–IDF baseline',color=teal)
axes[0].set(xticks=x,xticklabels=['Test','Challenge'],ylim=(0,1.15),ylabel='Macro-F1',title='Baseline wins on both partitions')
axes[0].legend(frameon=False,fontsize=9)
for container in axes[0].containers: axes[0].bar_label(container,fmt='%.3f',padding=3,fontsize=9)
vals=[100*m[s]['binary_alert_false_positive_rate'] for s in ['test','challenge']]
bars=axes[1].bar(x,vals,color=[blue,orange],width=.55)
axes[1].bar_label(bars,fmt='%.2f%%',padding=4)
axes[1].set(xticks=x,xticklabels=['Test','Challenge'],ylim=(0,65),ylabel='Benign requests flagged (%)',title='Transformer alert false-positive rate')
for ax in axes:
 ax.spines[['top','right']].set_visible(False); ax.grid(axis='y',alpha=.15); ax.set_axisbelow(True)
fig.suptitle('Pattern Shield • Synthetic-data evaluation',fontsize=17,fontweight='bold',color=dark)
fig.text(.5,.01,'One local run. These figures are not production accuracy estimates.',ha='center',fontsize=10,color='#40566C')
fig.tight_layout(rect=[0,.04,1,.95]); save(fig,'evaluation')
h=pd.read_csv('results/training_history.csv')
fig,axes=plt.subplots(1,2,figsize=(11,4))
axes[0].plot(h.epoch,h.loss,'o-',color=blue); axes[0].set(xlabel='Epoch',ylabel='Mean batch training loss',title='Training loss')
axes[1].plot(h.epoch,h.val_macro_f1,'o-',color=teal); axes[1].set(xlabel='Epoch',ylabel='Validation macro-F1',ylim=(0,1.05),title='Validation checkpoint criterion')
for ax in axes: ax.spines[['top','right']].set_visible(False); ax.grid(alpha=.2)
fig.tight_layout(); save(fig,'training_history')
print('Generated four diagrams/charts in PNG and SVG formats.')
