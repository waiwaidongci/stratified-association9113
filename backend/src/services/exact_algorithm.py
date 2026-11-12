"""Fixed-margin hypergeometric convolution, with declared mean-distance two-sided tail."""
import numpy as np
from scipy.stats import hypergeom

def conditional_distribution(rows):
 prob=np.array([1],dtype=np.longdouble);offset=0;layers=[]
 for t in rows:
  n=t['n'];r=t['row_a'];c=t['success_total'];lo=max(0,r-(n-c));hi=min(r,c)
  support=np.arange(lo,hi+1);logs=hypergeom.logpmf(support,n,c,r)
  pmf=np.exp(np.asarray(logs,dtype=np.longdouble));mass=pmf.sum()
  if not mass>0 or not np.isfinite(mass):raise ValueError('超几何概率计算失败')
  pmf/=mass
  if len(prob)+len(pmf)-1>1201:raise ValueError('卷积支持域超过1201个点的资源限额')
  prob=np.convolve(prob,pmf);offset+=lo;layers.append({'code':t['code'],'lower':lo,'upper':hi,'support_count':len(support)})
 mass=prob.sum();prob/=mass;support=np.arange(offset,offset+len(prob));return support,prob,layers

def exact_test(rows,observed,alpha):
 support,prob,layers=conditional_distribution(rows)
 # Exact rational mean-distance ordering via common integer denominators avoids asymmetric-tail float ties.
 from fractions import Fraction
 mean=sum((Fraction(t['row_a']*t['success_total'],t['n']) for t in rows),Fraction(0))
 distance=abs(Fraction(observed)-mean);mask=np.array([abs(Fraction(int(s))-mean)>=distance for s in support])
 p=prob[mask].sum();numeric=float(p);logp=float(np.log(p)) if p>0 else None
 mean_numeric=float(np.sum(support*prob));var_numeric=float(np.sum((support-mean_numeric)**2*prob))
 return {'p_value':numeric if numeric>0 else None,'p_log':logp,'p_underflow':bool(p>0 and numeric==0),'p_display':np.format_float_scientific(p,precision=8,unique=False),'below_alpha':bool(p<=alpha),'alpha':alpha,'mean_numerator':mean.numerator,'mean_denominator':mean.denominator,'observed_sum':observed,'support_lower':int(support[0]),'support_upper':int(support[-1]),'support_size':len(support),'probability_sum':float(prob.sum()),'distribution_mean':mean_numeric,'distribution_variance':var_numeric,'layers':layers,'distribution':[{'s':int(s),'probability':float(v),'log_probability':float(np.log(v)) if v>0 else None,'in_tail':bool(k)} for s,v,k in zip(support,prob,mask)],'tail_rule':'所有支持点s中 |s−E[S]| ≥ |观察S−E[S]| 的概率之和；用有理数精确判定并列。非Fisher概率排序双侧。','numeric':'logpmf→longdouble exponent/convolution;JSON保存double概率与log值。'}
