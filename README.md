# 岑岸封装分层率差核对册

把两种封装的成功/失败计数放回预先声明的湿度层，核对总体率、Mantel–Haenszel汇总与固定边际精确证据，再形成独立复验说明。

## 场景与角色

模拟客户为岑岸包装试验室，16位分析员按独立试片记录封装及浸湿结果。原流程从计数表直接比较总体成功率，层构成差异被忽略；稀疏表只看渐近p；核对说明与源数据版本分离。上游匿名独立试片四格计数 → 冻结分层研究 → 下游负责人审阅独立复验方案。不是自动封装采购、现场工艺控制或合格判定。

| 角色 | 页面与权限 | 典型动作 |
|---|---|---|
| analyst 分层分析员 | 六页读取、来源修订、排队及说明创建 | 修订来源后冻结所有预设层 |
| admin 试验负责人 | 分析员权限及说明批准/退回 | 仅对draft作一次审阅 |
| viewer 研究阅读者 | 只读、批准说明CSV | 下载附原始四格、完整支持域及指纹的报告 |

一天的剧本：08:30登录核对 `CN_20261112_封装分层计数.csv`；08:40确认低湿度[18,2,80,20]、高湿度[20,80,2,18]；09:00保存采样批注；09:10以alpha=.05冻结两层；独立worker计算CMH与41点卷积；09:20比较总体A31.7%/B68.3%与各层A更高；09:30记录非因果、未检验同质性边界；10:00负责人批准独立复验；阅读者下载CSV并核对SHA256。

## 启动

```bash
cp .env.example .env
docker compose config --quiet
docker compose up -d --build
# 再次执行不会新增或覆盖已有自然键的用户修改
docker compose exec -T backend python -m scripts.seed_demo
# 测试完成后，仅清本项目演示栈及卷
docker compose down -v --remove-orphans
```

- 前端：<http://localhost:18239>；后端：<http://localhost:19239/docs>；MySQL宿主端口17739。
- Compose固定短名 `stratified-association`，恰好frontend/backend/worker/db/redis五服务，全部有真实健康探针。数据库、Redis和共享产物分别命名卷；Redis/worker不映射宿主端口。
- 账号 `admin@cenan.demo`、`analyst@cenan.demo`、`viewer@cenan.demo`；共同演示密码 `Cenan2026!`。
- 本批最多3个项目Docker栈同时运行。

## 页面与实体

首页展示最新完成研究；分层底稿可建立研究/预设层并写入四格、来源和批注；冻结计算提交任务；结果页读取层内率、CMH与全部精确支持；复验说明经负责人审阅后导出；过程留痕展示持久化动作。

| 实体 | 表 | 全栈入口 |
|---|---|---|
| AssociationStudy | association_studies | models/schemas/study → study_service/controller → /studies → api/studies.ts → 来源、首页、配置 |
| ExposureStratum | exposure_strata | stratum对应文件 → /strata → api/strata.ts → 来源与冻结结果 |
| TableCount | table_counts | count对应文件 → /counts → api/counts.ts → 四格表与编辑 |
| AssociationRun | association_runs | run对应文件 → /runs → stores/research.ts → 队列与完整结果 |
| VerificationNote | verification_notes | note对应文件 → /notes → api/notes.ts → 起草、审阅与CSV |

以上后台路径均在backend/src；前端在frontend/src。另有User/Audit横切表。共享组件包括StudySelect、RunSelect、StratumTable、RateStrips、ExactDistribution、PageHeading、StatusBadge及ErrorNotice；useTask处理错误、usePolling刷新进行中任务。统计量均由后端计算；前端只将服务器返回数值映射到图形。

## 数学与数值口径

每层为`[[a,b],[c,d]]`，a/c为A/B成功，b/d为失败。MH共同优势比为Σ(ad/n)/Σ(bc/n)，与把全部层直接相加的粗OR分别显示。零OR、无界OR和0÷0未定义分别标记；不加.5。CMH使用固定边际期望`E[a]=rA*c成功/n`，方差`rA*rB*c成功*c失败/(n²(n−1))`，统计量`(Σa−ΣE)²/ΣVar`，无连续性修正。无信息层仍保留标记；全部无条件方差时任务真实failed。

精确部分逐层计算Hypergeometric固定边际PMF，再卷积S=Σa。**双侧定义为`|s−E[S]| >= |观察S−E[S]|`的总概率**，并列以Fraction有理数比较；不是Fisher按PMF大小排序的双侧定义。保存每个支持点/概率/log/入尾标记、总质量/均值/方差。

生产计算用logpmf、longdouble指数和卷积。极小概率转换为JSON double会下溢时，数值字段为null并标记underflow，仍保留科学计数文本与有限log；CMH渐近p通过log normal tail避免误呈现为0。longdouble精度取决于平台，不宣称无限精度。各层计数非负整数、每格≤500/每层总数1..1000、每研究2..8完整层、卷积支持域≤1201点；超资源或无有效统计量明确失败。

参考：[statsmodels分层2×2与独立采样模型](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.StratifiedTable.html)、[SciPy超几何分布](https://docs.scipy.org/doc/scipy-1.14.1/reference/generated/scipy.stats.hypergeom.html)。本项目选择的均值距离精确双侧规则已在界面和CSV另行声明。

## 快照、seed与环境

三份合成底稿：CN-REV两层率反转；CN-SPARSE四层稀疏对照；CN-NULL三层含无A样本层。初始3用户/3研究/9层/9计数/1完成研究/1批准说明。提交任务时冻结研究、层、计数、来源与批注；worker只算快照，源计数事后变化不改变旧结果和批准CSV。seed按自然键仅添加缺失项，不覆盖用户改动。

| 环境变量 | 用途 |
|---|---|
| COMPOSE_PROJECT_NAME | 固定语义短名，用于容器名 |
| FRONTEND_PORT / BACKEND_PORT / DB_PORT | 18239 / 19239 / 17739 |
| MYSQL_DATABASE / MYSQL_USER / MYSQL_PASSWORD / MYSQL_ROOT_PASSWORD | 演示MySQL配置，见.env.example |
| JWT_SECRET | 演示JWT签名配置 |
| SEED_DEMO | true时后端启动尝试seed；失败记日志且API继续启动 |

Python3.11/FastAPI0.115.6/SQLAlchemy2.0.36/PyMySQL1.1.1、NumPy2.1.3/SciPy1.14.1、Vue3.5.45/TypeScript5.7.2/Vite6.4.6、MySQL8/Redis7/Nginx1.27。MySQL alpha使用DOUBLE(asdecimal=False)，统计结果JSON保留计算精度。backend/src分routes/controllers/services/models/schemas/middlewares/utils/constants/config；backend/scripts/seed_demo.py；migrations/README.md说明metadata建表范围，不伪称生产迁移链。

本地开发：启动MySQL/Redis后配置DATABASE_URL、REDIS_URL和JWT_SECRET，停止占用本地开发端口的Compose应用服务，在backend安装requirements并运行`uvicorn src.main:app --host 127.0.0.1 --port 19239 --reload`；停止Compose前端后在frontend执行`npm ci`和`npm run dev`，浏览器使用Vite打印地址。vite.config.ts代理/api到本题后端。

共享枚举：backend/src/constants/enums.py中的Role/RunStatus/NoteStatus；frontend/src/constants/enums.ts中的roles/states及types/domain.ts角色定义；后端middlewares/auth.py与前端stores/auth.ts分别应用权限。请求防护为本应用Redis每IP每分钟360请求，健康探针豁免，Redis不可用返回503；错误响应不回显非法浮点input。审计保存登录、来源修订、排队、worker完成、审阅和导出。

## 范围与交付

共同OR是加权汇总，本项目没有Breslow–Day同质性检验；层差异大时不能把它当普遍相同效果。层内观察独立、边际固定的条件零假设需由试验设计支持；未随机化不作因果解释，未拒绝不证明等效。只有本机单worker研究队列，未验证崩溃重投、多worker竞态或生产压力；初始化采用create_all，不含生产升级链。不是检测仪采集或任意文件自动导入，来源字段仅保留追溯元数据。Google字体有本地serif回退。

源码不含截图、测试日志或.env。真实验证脚本/TESTING/PNG/CSV/JSON在同批独立`test-artifacts/gb-0035/`，作为验收证据单独交付。License：MIT，见LICENSE。
