import warnings


import pandas as pd
import numpy as np
import gzip
from zipfile import ZipFile
import os
import re


from matplotlib import pyplot as plt
from IPython.display import display



figpath = "C:/Users/fdoll/BINF6310coding/figures/"
data_path = "C:/Users/fdoll/BINF6310coding/data/data/"

warnings.filterwarnings("ignore")


LLR_FILE = './ALL_hum_isoforms_ESM1b_LLR.zip'
TEST_FILE = './test.csv'

def set_ax_border_color(ax, color):

    import matplotlib.pyplot as plt

    for child in ax.get_children():
        if isinstance(child, plt.matplotlib.spines.Spine):
            child.set_color(color)

def savefig(fig, base_name, svg = True, png = True, pdf = True, dpi = 300, dir = '/data/figures/', \
        kwargs = dict(bbox_inches = 'tight')):

    base_path = os.path.join(dir, base_name)

    if svg:
        fig.savefig(base_path + '.svg', format = 'svg', **kwargs)

    if png:
        fig.savefig(base_path + '.png', format = 'png', dpi = dpi, **kwargs)

    if pdf:
        fig.savefig(base_path + '.pdf', format = 'pdf', **kwargs)

def get_alignment_indices(alignments):
  idx=[]
  for i in range(len(alignments)):
    U = alignments[i]
    total_gaps=[]
    for k in range(len(U)):
      total_gaps+=[count_gaps(U[k].seqA)+count_gaps(U[k].seqB)]
    idx+=[np.argmin(total_gaps)]

  return idx

def get_alignment_index(alignments):
    total_gaps=[]
    for k in range(len(alignments)):
      total_gaps+=[count_gaps(alignments[k].seqA)+count_gaps(alignments[k].seqB)]
    return np.argmin(total_gaps)

def count_gaps(x):
  gaps=0
  gapflag=False
  for k in x:
    if k == '-' and gapflag==False:
      gapflag=True
      gaps+=1
    elif k != '-' and gapflag==True:
      gapflag=False
  return gaps

def colidx(seq,pos=None):
  if pos==None:
    c=[]
    pos_=0
    for i in list(seq):
      if i =='-':
        c+=[i]
      else:
        pos_+=1
        c+=[i+' '+str(pos_)]
  else:
    c=[]
    pos_=0
    for i in list(seq):
      if i =='-':
        c+=[i]
      else:
        c+=[i+' '+pos[pos_]]
        pos_+=1
  return c

def getseq(LLR):
  return ''.join([i.split(' ')[0] for i in LLR.columns])
def getpos(LLR):
  return [i.split(' ')[1] for i in LLR.columns]



##### figure 2a

import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)
import matplotlib.pyplot as plt
#%matplotlib inline

res = pd.read_csv(data_path+'ClinVar_ALL_isoform_missense_predictions.csv',index_col=0)
res_min = pd.read_csv(data_path+'ClinVar_ALL_isoform_missense_predictions_groupby_AlleleID.csv')
res2= pd.read_csv(data_path+'final_updated_file_two.csv')
res_min2 = res2.groupby(['uniprot_isoform_id', 'aa_change']).agg({'ESM1b_score':'mean','common_gnomad':'last','clinvar_label':'last','Gold_Stars':'last','EVE_scores_ASM':'last'})
res_min2=res_min2.reset_index()

#res_min2['hgmd_label'] = np.nan
#res_min2.loc[res_min2.hgmd_class.isin(['DM'])  ,'hgmd_label'] = 1
#res_min2.loc[res_min2.common_gnomad==1  ,'hgmd_label'] = 0

plt.figure(figsize=(10,8))
plt.rc('xtick', labelsize=20)
# plt.rc('ytick', labelsize=12)

tmp=res_min[res_min.ClinicalSignificance.isin(['Pathogenic'])]
plt.hist(tmp.ESM1b_score_mean,bins=25,density=1,color='orange',label='ClinVar: Pathogenic (11403)',)
tmp=res_min[res_min.ClinicalSignificance.isin(['Benign'])]
plt.hist(tmp.ESM1b_score_mean,alpha=0.7,bins=25,density=1,color='cornflowerblue',label='ClinVar: Benign (13557)')

#tmp=res_min2[res_min2.hgmd_label==1]
#plt.hist(tmp.ESM1b_score,bins=25,density=1,color='red',label='HGMD: Disease-causing (76151)',histtype=u'step',linewidth=2)
tmp=res_min2[res_min2.common_gnomad==1]
plt.hist(tmp.ESM1b_score,bins=25,density=1,color='mediumblue',label='gnomAD: MAF>0.01 (30262)',histtype=u'step',linewidth=2)
plt.xlim([-29,9])
plt.legend(fontsize=17,loc='upper left')
plt.xlabel('ESM1b LLR score',fontsize=22)
plt.yticks([])
# plt.axvline(x=-7.5, color='k', linestyle='--') # Add vertical dashed line at x = -7.5
plt.vlines(x=-7.5, ymin=0, ymax=0.165, color='k', linestyle='--')

figname = 'Fig2A-1'
# plt.savefig(f"{figpath}/{figname}.svg", format='svg',bbox_inches = 'tight')
plt.savefig(f"{figpath}/{figname}.pdf", format='pdf',bbox_inches = 'tight')
# plt.savefig(f"{figpath}/{figname}.png", dpi=300,bbox_inches = 'tight')

plt.show()
len(res_min2[res_min2.hgmd_label==1]),len(res_min2[res_min2.common_gnomad==1])
