"""CMH with no continuity correction and no artificial zero-cell shift."""
import math
import numpy as np
from scipy.special import log_ndtr

def ratio(num,den):
 if den==0:return {'value':None,'status':'unbounded' if num>0 else 'undefined'}
 return {'value':float(num/den),'status':'finite'}
def validate_tables(tables):
 if not isinstance(tables,list) or not 1<=len(tables)<=8:raise ValueError('需要1..8层2×2表')
 seen=set();out=[]
 for i,t in enumerate(tables):
  code=t.get('code',str(i))
  if code in seen:raise ValueError('层编号重复')
  seen.add(code);v=[t.get(k) for k in ['a','b','c','d']]
  if any(isinstance(x,bool) or not isinstance(x,int) or x<0 or x>500 for x in v):raise ValueError('计数须为0..500整数，布尔不算计数')
  n=sum(v)
  if not 1<=n<=1000:raise ValueError('各层总数须1..1000')
  a,b,c,d=v;r1=a+b;r2=c+d;c1=a+c;c2=b+d
  e=r1*c1/n;var=r1*r2*c1*c2/(n*n*(n-1)) if n>1 else 0.
  out.append({**t,'n':n,'row_a':r1,'row_b':r2,'success_total':c1,'failure_total':c2,'expected_a':e,'variance_a':var,'informative':var>0,'odds_ratio':ratio(a*d,b*c),'rate_a':a/r1 if r1 else None,'rate_b':c/r2 if r2 else None})
 return out

def calculate_cmh(tables):
 rows=validate_tables(tables);variance=math.fsum(t['variance_a'] for t in rows)
 if variance<=0:raise ValueError('全部层无有效条件方差，关联检验未定义')
 deviation=math.fsum(t['a']-t['expected_a'] for t in rows);statistic=deviation*deviation/variance
 logp=float(math.log(2)+log_ndtr(-math.sqrt(statistic)));p_numeric=math.exp(logp)
 num=math.fsum(t['a']*t['d']/t['n'] for t in rows);den=math.fsum(t['b']*t['c']/t['n'] for t in rows)
 sums={k:sum(t[k] for t in rows) for k in ['a','b','c','d']};a,b,c,d=[sums[k] for k in ['a','b','c','d']]
 return {'strata':rows,'observed_sum_a':sum(t['a'] for t in rows),'expected_sum_a':math.fsum(t['expected_a'] for t in rows),'variance_sum_a':variance,'cmh':statistic,'asymptotic_p':p_numeric if p_numeric>0 else None,'asymptotic_p_log':logp,'asymptotic_p_display':np.format_float_scientific(np.exp(np.longdouble(logp)),precision=8,unique=False),'asymptotic_p_underflow':p_numeric==0,'adjusted_or':ratio(num,den),'mh_numerator':num,'mh_denominator':den,'pooled':{**sums,'odds_ratio':ratio(a*d,b*c),'rate_a':a/(a+b) if a+b else None,'rate_b':c/(c+d) if c+d else None},'uninformative_codes':[t['code'] for t in rows if not t['informative']],'correction':False,'zero_shift':False}
