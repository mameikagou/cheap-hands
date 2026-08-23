---
name: mining-factors
description: Use when mining, discovering, iterating, batch-testing, comparing, combining, transferring, or promoting quantitative factors in the analyze repository. It keeps the user-approved research contract and repository mainline authoritative, protects truly unseen evaluation data with machine-enforced access controls, separates predictive information from portfolio and execution failures, and evaluates weak factors as combination inputs without inventing fixed budgets or parallel infrastructure.
---

# Mining Factors

Run factor research that answers the user's actual question and stays on the repository's official data, research, backtest, registry, and product paths.

## Start from the current contract

Before designing a formula or running data, write one sentence stating:

`The requested result is <deliverable>, produced through <official path>, for <market/universe/horizon>.`

Then read, in this order:

1. The current user instruction and latest frozen decision.
2. Applicable `AGENTS.md` files.
3. The current PLAN, ROAD, campaign contract, stopping condition, failure ledger, and existing results.
4. The repository's local-data skill and inventory contract.
5. The `sanity` skill, relevant Brain notes, and available OpenMemory records.

Use [references/research-lessons.md](references/research-lessons.md) when designing a campaign, combination, cross-market transfer, or promotion decision. Use [references/analyze-workflow.md](references/analyze-workflow.md) before running repository commands.

The frozen user contract overrides this skill. Do not create a Goal, change a budget, shrink a candidate family, prohibit an approved model, add a stopping rule, or open a protected sample unless the user or frozen contract authorizes it. If live code or a plan conflicts with the frozen contract, report `CONTRACT_CONFLICT` with the exact difference before continuing.

## Name the research layer

Classify the task before choosing metrics:

- `PREDICTOR`: Does a variable rank assets, identify a market state, time a factor, or predict an exit risk?
- `COMBINATION`: Does adding several predictors improve a frozen baseline or joint model?
- `PORTFOLIO`: Can a frozen score become target holdings under the strategy rules?
- `EXECUTION`: Can the approved engine trade those targets with real prices, constraints, and costs?
- `SYSTEM`: Does the implementation preserve one data path, registry, engine route, and product surface?

Do not move a conclusion between layers. A high-turnover portfolio can fail while its inputs retain weak ranking information. A negative fixed formula does not reject every family represented in that formula. An engineering or data failure is not a scientific result.

## Freeze the research question

Record the market, point-in-time universe, signal time, fields available at that time, earliest executable price, prediction target, holding period, primary metric, development and protected periods, costs, candidate/model budget, combination permission, and stopping rule.

Distinguish the signal's purpose:

- Cross-sectional selection compares assets at the same time.
- Market timing decides whether total exposure should rise, fall, or stay in cash.
- Factor timing changes how much weight a style or factor family receives.
- Exit or tail-risk signals aim to avoid a specified realizable loss.

Use a metric that can observe the declared purpose. A market-wide state can be identical for every asset and still be useful for timing; lack of cross-sectional rank correlation does not reject it.

## Use only the official local data path

Query the inventory interface for the exact scope, fields, universe, symbols, and dates. Validate a structured `data_requirement` before saving or running a factor.

If a required field, time range, symbol, point-in-time mapping, or executable price is missing:

- return `DATA_BLOCKED` with the exact gap;
- do not substitute a similar field, current membership, revised snapshot, or another price;
- do not fetch data inside factor evaluation;
- add data only through raw to canonical or mart to inventory when the task authorizes ingestion.

Missing next-open data means no fill. A held but unsellable asset remains held and continues to consume cash, capacity, and risk limits.

## Protect unseen periods with machine enforcement

Text saying “do not look” is not a seal. Before claiming validation or final data is unseen, require all of these:

1. The development process receives only development data through a restricted database view, dataset root, service role, or equivalent access boundary. Its credentials cannot read protected rows or protected metrics.
2. Status, logs, APIs, dashboards, artifacts, and error messages exclude protected dates, rankings, directions, curves, and aggregate metrics before the authorized reveal.
3. A test executed with the same identity as the mining process proves protected reads fail. A convention, hidden filename, prompt instruction, or untested permission is insufficient.
4. PostgreSQL records the development, validation, and final intervals; reveal counts; data and code hashes; and the complete candidate set.
5. Before a reveal, atomically freeze the candidate IDs, directions, transforms, model or weights, universe, labels, costs, execution rules, code hash, data snapshot, and evaluation procedure.
6. The authorized reveal is an atomic state transition. Validation or final results cannot be overwritten, re-hidden, or consumed twice.

If any person or process saw protected evidence before the freeze, mark that interval `CONTAMINATED`. It may remain retrospective evidence, but it cannot be relabeled as truly unseen. Create a successor only when a genuinely later untouched period exists; a new campaign ID does not create new sample-out-of-sample evidence.

Do not open validation or final merely because development code runs. Follow the current campaign's frozen readiness and reveal contract.

## Mine broadly without manufacturing breadth

Use the user-approved candidate, round, model, and time budget. This skill sets no default cap.

For every candidate, record its parent hypothesis, economic mechanism, required fields, transformation, expected direction, horizon, applicable state, and falsification condition. Save every attempted candidate and failure in the official registry before reading its result.

Count three different things:

1. nominal formulas;
2. distinct economic mechanisms;
3. effective independent information dimensions.

Adjacent windows, renamed formulas, similar transforms, overlapping holdings, or signals that fail in the same periods do not automatically provide independent evidence. Similarity describes and controls the pool; it does not justify early deletion unless equivalent ranking, coverage, trading meaning, and lack of conditional increment are demonstrated.

Use small-window dry runs before full evaluation to test expression parsing, point-in-time alignment, sparse starts, empty outputs, cross-year partitions, terminal calendar boundaries, resource peaks, and schema consistency. Classify a dry-run failure as engineering evidence.

## Treat weak predictors as combination inputs

Unless the frozen contract says otherwise, do not require each input to be a profitable standalone strategy, cover all costs alone, pass every year, or beat the incumbent before combination.

Remove or block an input only for a demonstrated fatal problem such as future data, an impossible trade, a constant or irreproducible output, a broken mapping, or proven duplicate information. Otherwise retain weak but legal inputs as `KEEP_WEAK_SEED`, `COMPONENT_ONLY`, `POSSIBLE_REDUNDANCY`, or `INSUFFICIENT_EVIDENCE` as supported by the evidence.

Start with an interpretable joint baseline appropriate to the contract. A useful default is robust scaling or ranking within each time point, combination within economic families, then combination across families so the family with the most formulas does not receive more weight by accident. Keep a simple baseline as a measuring stick. If the contract permits regularized linear models, nonlinear models, interactions, or machine learning, evaluate them rather than silently prohibiting them.

Do not count RankIC, quantile spread, top-N return, and win rate from the same labels, assets, and dates as independent confirmations. Report their shared evidence base.

## Separate relative selection from the decision to trade

A cross-sectional rank answers “which asset looks better than the others.” It does not answer “is any asset expected to make enough money to buy.” A top percentile always exists when the cross-section is large enough, so it cannot by itself implement an absolute entry gate or permission to hold cash.

When the strategy must choose between cash, holding, exiting, and replacing:

- calibrate an expected forward absolute return for cash entry and exit decisions;
- calibrate expected forward relative improvement for replacement decisions;
- use only information available at the decision time;
- compare prediction and full incremental cost in the same unit and over the same horizon;
- include fees, spread, slippage, impact, funding or borrow cost, taxes, minimum commissions, lot or quantity rules, and the frozen safety margin.

If the expected improvement is less than or equal to the complete incremental cost plus safety margin, the decision is `HOLD` and the order count must be zero. Ranking buffers, minimum holding periods, smoothing, and replacement limits can reduce churn but cannot replace this net-benefit test.

If the data cannot support a defensible absolute-return or cost estimate, do not invent a numeric gate. Keep the work at the predictor or research layer, mark the trading claim `INSUFFICIENT_EVIDENCE`, and fail closed for formal trading.

## Reconcile decisions to engine orders

The strategy layer emits public signals or `target_weights`; the approved engine owns orders, fills, cash, positions, fees, valuation, and profit and loss.

Reconcile every strategy decision to the engine's authoritative output. `HOLD`, `HOLD_COST`, and `BLOCKED` must produce zero orders. Unchanged membership must not trigger hidden equal-weight restoration. A small number of approved replacements combined with high order count or turnover is an implementation failure, not a strategy result.

Use the engine route declared by the current repository rules. In `analyze`, this normally means Qlib for A-share research and formal portfolio results, VectorBT Pro for crypto research portfolios, and NautilusTrader for approved formal crypto or U.S. execution. Never introduce community `vectorbt`, a handwritten account, a shadow fee or funding ledger, or another return curve.

Run expensive portfolio and formal-engine stages only after the prerequisites frozen in the current campaign contract pass. Cheap predictor diagnostics may proceed when their own data and timing gates pass; lack of later formal market detail should not block correctly labelled exploratory research unless the contract requires it.

## Preserve one mainline and one source of truth

Reuse the existing CLI, data lake, PostgreSQL registry, factor catalog, model path, target-weight contract, approved engines, artifact root, API, and frontend. Do not create a campaign-specific CLI, database, config tree, report system, artifact root, production module, account, or test tree.

Store machine state, candidates, metrics, failures, reveal counts, hashes, and relationships in PostgreSQL. Store large panels and time series once in the data lake or approved Parquet area and register their lifecycle. Write prose only for a named human reader. Do not make a dashboard reconstruct state by scanning directories.

When a new path replaces an old one, remove the old active code, entrypoint, config, test, and catalog route in the same change. Preserve planning, failures, research conclusions, and human decision history as evidence; mark obsolete instructions retired instead of deleting history.

## Classify results at the narrowest valid level

Use separate states for:

- `ENGINEERING_FAILED`
- `DATA_BLOCKED`
- `EVALUATION_MISMATCH`
- `INCONCLUSIVE`
- `FORMULA_NEGATIVE`
- `COMBINATION_NEGATIVE`
- `EXECUTION_NEGATIVE`
- `CONTAMINATED`
- `VALIDATED`

State exactly which formula, mechanism, combination, trading rule, market, horizon, and period the result covers. Do not turn one fixed formula, one batch, or one trading shell into a family-level rejection. Before stopping a campaign, compare the executed breadth and depth with the frozen contract, report untested mechanisms and retained weak seeds, and verify that the contract's stopping condition is actually satisfied.

## Report the outcome

Lead with the answer to the user's question, then report:

1. frozen scope, primary target, and official path;
2. data readiness and point-in-time gaps;
3. attempted formulas, mechanisms, and effective dimensions;
4. predictor, combination, portfolio, and execution evidence separately;
5. protected-sample state and reveal count;
6. full costs, rejected trades, order reconciliation, and engine provenance when a portfolio ran;
7. exact failure scope, remaining evidence, registry identity, and reproducibility hashes;
8. whether product/API/UI synchronization is required and complete.

Use plain Chinese. Explain what was measured, what would be bought or sold, and over what holding period. Do not use a passing test, generated artifact, or visible page as proof that the research question was answered.
