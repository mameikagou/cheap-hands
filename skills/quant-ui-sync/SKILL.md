---
name: quant-ui-sync
description: Maintain the analyze2quant research frontend and result visibility whenever a factor, strategy, spec, run, or its status/result is completed or materially changed. Use before declaring such work finished so run registration, api-schema projections, the single read-only UI, artifact policies, and recurrence guards stay synchronized without page-model copies, runtime file scans, direct database writes, or hardcoded data.
---

# 量化研究 UI 与结果登记同步（analyze2quant 版）

把结果可见性视为因子和策略交付的一部分。研究 Run 完成、失败、淘汰、晋级或重新回测后，主动检查登记与展示链路；不要等用户再次提醒。

主线合同以 `analyze2quant/AGENTS.md` 为权威；本 skill 只规定交付检查动作。若合同与本文件冲突，以 AGENTS.md 为准并回来更新本文件。

## 架构事实（先记住，再动手）

- 唯一产品入口：`analyze2quant` CLI（`src/analyze2quant/cli.py` 装配 `commands/` 下 database、data、research、web 四个命令组）。不得另建入口、脚本旁路或第二套 registry。
- 唯一权威状态：PostgreSQL `analyze2quant_prod`；`migrations/` 是只追加的唯一迁移链（checksum 校验，`db/migrate.py` 执行）。旧库 `qrant_research_prod` 是带 hash 的只读冷档，任何新写入都是合同违规。
- UI/AI 同源投影：`api` schema 不拥有状态，只为 UI 与 AI 生成同一份有界读模型（如 `0005_research_results_read_model`、`0017_research_direction_read_model`）。**不存在也不允许再出现"页面快照表/离线刷新页面模型"这种第二持久副本。**
- 唯一前端：只读 server `src/analyze2quant/web.py` + 静态资源 `web/index.html`、`web/app.js`、`web/styles.css`。`web/app.js` 只调用同源只读 API 展示 definition/run/evidence；`web/` 内禁止独立状态、回测器或文件扫描逻辑。
- AI 是直接操作者但不越层：不得直写数据库、不得 scrape UI、不得从 `planning/` 推断运行时状态、不得自行宣告 Run 成功。动作必须幂等、带 state version、可恢复，由 lease/fencing 仲裁并发。
- 产物纪律：`research context`/`research capabilities` 返回的 `artifact_policy` 是登记依据。普通研究默认内存计算；中间表只进 `StorageRoots` 受管 tmp 或 `tempfile.TemporaryDirectory`。禁止把面板、CSV/Parquet、数据库副本写进仓库根、`planning/`、`data/`、`artifacts/`、`runs/`；只有明确留存的 handoff/正式证据进入受管 objects 并登记元数据。

## 执行流程

1. 读目标仓库 `AGENTS.md` 与本次涉及的 owner（commands/research、commands/web、api 投影迁移、web/ 静态资源），确认当前分支仍提供对应能力。
2. 判断结果应出现在哪个既有投影：研究线/方向视图、definition/spec 详情、run 终态与 evidence。优先复用现有页面结构，不为单个结果新建孤立页面或新表副本。
3. 走正式登记链路：先登记 spec/定义，再 `research run-spec` 执行；成功状态、metrics、evidence 由系统一起登记。**完成依据只认 `research context --run-id` 的终态及证据**——脚本打印 DONE、生成 CSV、Git 提交或 `spec_json.dev_result` 都不算已登记。
4. Run 身份必须可复用且可复现：spec、phase、代码 commit、实际 Python/引擎依赖版本、规范化 parameters、pinned run_inputs 缺一不可；dataset 变化后不得把旧 Run 冒充新结果。
5. 需要新的展示字段或投影时，先加迁移（唯一链、只追加）与 `api` 读模型，再改 `web.py` API，最后改 `web/` 展示；三层共用同一份数据，禁止在 JS 里二次聚合出"自己的真相"。
6. 展示真实状态：进行中、完成、未通过、失败、归档，以及失败分类（工程阻断返回结构化原因，不写策略 workaround）。未通过的 Run 保留结论和原因，不得删除记录伪装成从未研究过。
7. 没有可靠值就显示未知/待补或 `NULL`；禁止为维持卡片数、百分比或曲线补零、复制旧指标或造 mock。`web.py`/API 遇到缺失产物必须失败关闭并标注 missing/quarantined，不得静默跳过。
8. 验证后才准报告完成：相关 pytest（含 `tests/test_repository_map.py` 的主线合同检查）、迁移在干净库执行通过、同源 API 冒烟能查到本次 run_id 的终态与 evidence、`web/` 页面冒烟展示正确。任何一步失败，研究任务不得报完成。

## 登记硬门槛（每次产生真实回测曲线、订单、成交或持仓时）

1. 成功 Run 的终态、metrics、evidence 必须来自同一登记事务；出现"曲线存在但查不到正式 run/evidence"即 P1 实现错误，修正式 runner，不写一次性补表脚本冒充完成。
2. 需要留存的产物先按 `artifact_policy` 进受管 objects 并登记路径、大小、schema、hash；读路径以登记元数据为准做存在性与哈希校验，对象丢失立即转 `missing`/`quarantined` 并在投影中可见。
3. 投影与权威表的不一致计数必须为零：有成功终态但无 evidence 引用、有 artifacts 记录但实体不存在、或有实体文件未登记，三类都要在收尾检查中报告并清零。
4. 隔离 runtime 不背展示责任：普通回测不得创建 detached `analyze2quant-runtime-*` worktree；工程维护者按 lease、进程引用与数据库活跃状态回收，策略 Agent 不参与扫目录 GC。

## 删除、合并与重分类

资产盘点不是只增不减，但收敛必须走合同：

1. 先冻结业务范围（市场、line_key、hypothesis/spec/run ID、预期关联行数），不按名称或目录通配符直接删。
2. 区分正式回测结论、底层实验明细、失败叙事三层；底层实验可删，人能读懂的"试过什么、为什么停"的正式记录保留。
3. 数据库内变更走唯一迁移链或受管 action，在同一事务按外键从子到父处理，完成后重算范围计数确认无孤儿、未误伤共享数据。禁止绕过 `migrations/` 手改生产 schema。
4. 大型产物先移入带时间戳的回收目录并登记原路径/目标路径/数量，验证后再销毁；共享原始数据、provider、源码不得跟随单次实验删除。冷档库（旧 `qrant_research_prod`）永不参与此类操作。
5. 删除或降级后，投影由权威表实时派生，无需"重新生成页面快照"；核对列表总数、详情入口与引用一致性即可。若发现仍需手工刷新，说明有人造了第二副本——那是 P1 发现，按硬门槛回修。

## 前端部署与验证

1. UI 改动只发生在 `web/` 静态资源与 `src/analyze2quant/web.py`；无独立前端构建链，不引入 bun/node 第二套打包产物进仓库。
2. 提交前：`pytest`（含仓库地图与合同测试）通过；若改了迁移，在干净库验证迁移顺序与 checksum。
3. 部署沿用 `infra/` 现有受管服务方式重启 UI server；只部署已合并到目标分支并通过上述检查的版本，不从临时 worktree 直发。
4. 重启后验证：本机入口返回新静态资源且同源 API 冒烟通过；公网入口如有认证层，未认证返回跳转属正常，本机源站必须 200。
5. 部署不等于数据正确：展示仍以 `api` 投影 + run 终态为准；投影未包含本次结果时如实显示空/未知，禁止部署时临时扫描 YAML、JSON 或 Parquet 兜底。

## 展示字段取舍

只展示用户判断价值所需、且权威数据里真实存在的字段：

- 这是什么因子/策略、哪个市场、走到哪一步、最后更新时间。
- 使用的 dataset 合同与区间，是否含交易成本与可交易性约束。
- 核心指标与是否值得继续的依据（费后口径）。
- 可追溯引用：run_id、spec_id、代码 commit、pinned inputs、受管 objects。
- 失败时：失败在假设、数据、实现、稳健性还是成本，以及对应结构化阻断原因。

## 完成条件

同时满足才算真正完成：

- Run 终态、metrics、evidence 已由正式链路登记，`research context --run-id` 可查证。
- 成功回测无一遗漏地可从同源 API 追到定义、运行、产物与数据版本；三类不一致计数为 0。
- UI 展示来自 `api` 投影，无页面快照副本、无现场计算、无文件扫描。
- 本次涉及的每个新文件/目录都在 `AGENTS.md` 责任地图有归属（`test_repository_map.py` 通过）。
- 相关迁移、合同测试与冒烟全部通过；工程阻断已按结构化原因返回，而非写入策略 workaround。
