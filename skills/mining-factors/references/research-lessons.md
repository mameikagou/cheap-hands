# Research lessons from retained evidence

Read this file before designing a factor campaign, factor combination, cross-market transfer, or promotion decision. The frozen user contract and live repository remain authoritative.

## Evidence hierarchy

Use, in order:

1. Current user instruction and frozen PLAN or campaign contract.
2. The original `因子投资方法与实践` book sections relevant to the research object.
3. Live strategy code, point-in-time data, and approved-engine output.
4. `.planning/quant-qlib/failures/` and related reports.
5. Brain notes, papers, and OpenMemory `investment-learning` records.

Do not claim that OpenMemory was checked when its query fails. Do not replace it with an unrelated local store.

## Repeated failures and their durable corrections

### The experiment answered the wrong question

- ETF research copied a daily high-turnover trading shell when the user wanted weak inputs extracted for an existing low-turnover combination.
- A sentiment project evaluated market state with an individual-asset ranking pipeline and selected long-horizon price trends instead of market sentiment.
- A dynamic-theme project substituted a stable industry classification after the required theme data failed its data gate, then reported engineering completion as business completion.
- A combined-factor request was turned into a contest between the original strategy and a filtered weak-factor strategy, so the requested union was never tested.

Correction: state the requested result in one sentence, name the predictor/combination/portfolio/execution layer, and verify that every run directly answers it. A precise backtest of the wrong object is still wrong.

### Weak inputs were rejected too early

Earlier workflows required each weak input to satisfy many standalone profitability and stability gates. This removed inputs whose value could exist only after combination. Later searches relaxed the gates but mostly added adjacent windows: hundreds of formulas represented only a small number of independent directions.

Correction: at the input stage reject only fatal timing, data, reproducibility, constant-output, mapping, or proven-duplicate problems. Evaluate weak legal inputs for conditional or joint increment. Report nominal formulas, economic mechanisms, and effective independent dimensions separately.

### A formula or trading shell failure was exaggerated

- Several incomplete A-share runs were engineering failures, not evidence against factors.
- A frozen quality/value batch failed its one-time later-period test; the valid conclusion covered that batch and combination, not every quality or value mechanism.
- A fixed crypto five-input formula had negative development-period ranking information and gross losses. That rejected the fixed definition and weights, not order flow, open interest, funding, price behavior, or spot-perpetual transmission as families.
- Crypto order-flow inputs retained weak positive ranking information while an extremely high-turnover portfolio lost nearly all capital after fees, slippage, and funding.

Correction: report predictor, combination, portfolio, execution, data, and engineering conclusions separately and at the narrowest supported scope.

### Formula count was mistaken for independent information

Local campaigns produced hundreds of nominal formulas but only a small number of effective directions. Signals with low raw-value correlation still failed in the same years and represented the same economic mechanism. Several positive statistics computed from the same future-return labels were also counted as if they were independent confirmations.

Correction: preserve the complete search denominator, cluster formulas and economic mechanisms, inspect conditional increment and shared failure periods, and never count several views of the same labels and dates as independent evidence.

### Point-in-time semantics and executable prices were violated

Observed failures included current membership copied backward, same-day use of announcements without publication times, revised financial snapshots without a provable historical version, incorrect field meanings, planned management end dates treated as completed departures, incomplete protected-period coverage, and next-open orders silently filled at close.

Correction: validate official field meaning and available-at time before formula design. A date-only announcement becomes available on the next trading day unless a more precise earlier time is proved. Missing required execution prices fail closed; held unsellable assets remain held.

### Development success did not survive later data

Several A-share combinations looked strongly positive in development and all failed the once-opened later period. Repeated access to a historical period makes it known evidence even if a new campaign ID or later time split is created.

Correction: make the development and sample-out-of-sample dates part of the strategy contract. Freeze the complete factor combination and trading strategy before evaluating the later period. If that period was already examined, call it retrospective evidence and use genuinely later untouched data for the next sample-out-of-sample claim. Do not turn this rule into a permission or database-infrastructure project.

### Relative ranking was used as an absolute entry gate

In a crypto strategy, `score above the current cross-sectional 80th percentile` was intended to mean “only hold when there is a real signal.” With a sufficiently large universe, a top 20 percent always existed, so the strategy was almost always fully invested. A cross-sectional standardized score also had no natural 0-to-100 absolute scale.

Correction: use ranking only to compare assets. Cash entry and exit require a separately calibrated forward absolute-return estimate. Replacements require expected relative improvement. Both must be compared with full incremental costs over the same horizon using only information available at the decision time.

### Costs were deducted after trading instead of deciding whether to trade

Crypto combinations showed positive weak ranking information but changed members at most 4-hour checks. Gross gains were consumed by fees, slippage, and funding. Ranking buffers reduced turnover but did not ensure that a replacement was economically worthwhile.

Correction: compare expected new holding value with the existing holding or cash before emitting a target change. If the expected improvement does not strictly exceed all incremental costs and the frozen safety margin, emit `HOLD` and zero orders.

### Strategy decisions were rewritten by account behavior

An intended hold can still create trades when an account layer restores nominal equal weights. A small number of approved member changes combined with high order count or turnover proves the actual engine behavior differs from the strategy decision.

Correction: reconcile decisions to authoritative engine orders. `HOLD`, `HOLD_COST`, `BLOCKED`, and unchanged membership produce zero orders. Never maintain a second account or fee ledger to repair the approved engine.

### Engineering work became the deliverable

Some investigations focused on hashes, audit surfaces, one-off modules, reports, or extra safety layers while the requested research result remained unanswered. One-off U.S. experiments also entered long-lived source despite an existing campaign runner.

Correction: the deliverable is the implemented factor strategy and its result. Retain only the smallest correctness checks and repairs needed to run that strategy. Reuse the official runner and engines; do not create a new infrastructure surface, mechanical sample seal, audit framework, or registry project for one research round.

## Useful retained sources

- `.planning/quant-qlib/failures/README.md` and all current `F-*.md` records.
- `.planning/quant-qlib/plan/Binance_USDM_4H弱因子组合Goal执行计划-2026-08-21.md`, especially the later frozen-contract and cost-gate sections.
- Brain `因子/因子研究.md`.
- Brain `AI投研/Looping 因子挖掘：验证器捕获与真实 Alpha 边界.md`.
- Brain `币圈/Binance USD-M 4H订单流与杠杆因子研究方法及失败归因-2026-08-21.md`.
- Brain original book `投资书籍/因子投资方法与实践/chunks/`: chapter 2 sections in chunks 003–007, chapter 6 sections in chunks 023–029, and chapter 7 sections in chunks 030–037. Read these before the derived chapter notes.
- Brain `投资书籍/因子投资方法与实践/读书笔记-第6章-因子研究现状.md` as a derived local summary, not as a substitute for the original chapter.
- OpenMemory `investment-learning` memory `3254e9a0-960e-49dc-9766-f6e831db9041`: predictor evidence, combination evidence, and costed trading-policy evidence are three separate layers. Its metadata was verified as `canonical_project=investment-learning`.

These records are evidence and corrections, not a new universal contract. Resolve apparent conflict by returning to the current frozen contract, the live code path, and the original methodological source.
