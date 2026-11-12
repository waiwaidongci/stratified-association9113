import hashlib,json,math
from .cmh_algorithm import calculate_cmh
from .exact_algorithm import exact_test

def analyze(snapshot,alpha):
 if isinstance(alpha,bool) or not isinstance(alpha,(int,float)) or not math.isfinite(alpha) or not .001<=alpha<=.1:raise ValueError('alpha须在.001..0.1之间')
 tables=sorted(snapshot['tables'],key=lambda t:t['code']);cmh=calculate_cmh(tables);exact=exact_test(cmh['strata'],cmh['observed_sum_a'],alpha)
 canonical={'version':'cmh-mean-distance-exact-v1','snapshot':{**snapshot,'tables':tables},'alpha':alpha}
 fingerprint=hashlib.sha256(json.dumps(canonical,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
 return {**cmh,'exact':exact,'alpha':alpha,'input_snapshot':canonical['snapshot'],'fingerprint':fingerprint,'method_version':canonical['version'],'interpretation':'独立层内观察、固定边际条件零假设；精确p为均值距离双侧。共同OR仅加权汇总，未检验层间同质；分层关联不是封装效果的因果保证，稀疏表渐近p只作对照。'}
