---
name: mining-factors
description: Use when mining, discovering, iterating, batch-testing, comparing, combining, transferring, or implementing quantitative factors and factor strategies in the analyze repository. The skill focuses on producing an actual factor strategy—factor inputs, combination, entry, holding, replacement, exit, sizing, costs, and sample-out-of-sample evaluation—without turning research into an infrastructure, permission, audit, registry, or tooling project.
---

# Mining Factors

Produce the factor strategy the user asked for. The deliverable is the strategy definition, implementation, backtest, and evidence—not a new research-management system.

## Fix the strategy question first

Write one sentence before acting:

`Build and evaluate <strategy> in <market/universe>, using information known at <signal time>, trading at <execution time>, and holding for <horizon>.`

Read the current user decision, applicable `AGENTS.md`, frozen PLAN, and [references/research-lessons.md](references/research-lessons.md).

When the local Brain is available, read the original book `因子投资方法与实践` before its notes or summaries. For factor mining, the minimum original-book route is:

- chapter 2: portfolio sorting, multiple sorting, regression, incremental information, anomaly tests, and model comparison;
- chapter 6: p-hacking, multiple testing, economic explanations, costs, and sample-out-of-sample deterioration;
- chapter 7: return predictors, the six predictor criteria, return prediction, portfolio construction, constraints, cost models, factor combination, and the difficulty of factor timing.

Then read related failure records, the live strategy, `sanity`, relevant Brain notes, and available OpenMemory `investment-learning` records. The book supplies the research method; the repository and retained evidence supply the current market, data, execution, and failure constraints.

The current contract controls the research budget, candidate types, models, time split, costs, and stopping rule. This skill must not invent caps, rounds, gates, a Goal, or a simpler substitute task.

## Keep the research objects distinct

Use the book's distinctions instead of calling every column an “alpha factor”:

- A **return predictor** is a variable observed at the signal time and used to predict later asset returns.
- A **factor or anomaly portfolio** is a tradable portfolio formed from one or more predictors; its return is not the same object as the predictor value.
- A **return model** combines predictors into expected returns or scores.
- A **risk model** estimates the covariance and exposures used to control portfolio risk.
- A **trading strategy** turns the return model into positions through entry, holding, replacement, exit, sizing, and costs.

Test the object the user asked about. Predictor evidence, factor-portfolio evidence, combined-model evidence, and full-strategy evidence are related but not interchangeable.

## Define the complete strategy

Freeze the parts that determine what is bought or sold:

- market and point-in-time tradable universe;
- signal fields and the time each field becomes known;
- prediction target and holding period;
- factor direction and normalization;
- factor combination or model;
- entry rule;
- continuing-hold rule;
- replacement rule;
- exit or cash rule;
- position count, weight or sizing rule;
- signal time, order time, executable price, rebalance frequency;
- fees, spread, slippage, impact, funding or borrow cost, taxes, minimum commission, and lot or quantity rules;
- development period and sample-out-of-sample period.

If one of these is absent, complete the strategy from the frozen PLAN or live strategy before inventing new research machinery.

## Match factors to their actual job

Classify each input by what it predicts:

- Cross-sectional selection ranks assets at the same time.
- Market timing decides whether the strategy should hold risk or cash.
- Factor timing changes the weight of a factor family.
- Exit or tail-risk signals decide whether a realizable loss should be avoided.

Use a matching target and metric. Do not reject a market-wide signal because it has no cross-sectional RankIC. Do not claim an exit signal failed merely because it did not improve entry ranking.

Keep four conclusions separate:

1. whether an input contains predictive information;
2. whether inputs improve each other when combined;
3. whether the complete holding and replacement strategy works after costs;
4. whether a formal engine can execute it under real constraints.

A high-turnover strategy can fail while its weak inputs remain useful. A fixed formula can fail without rejecting every factor family it contains.

## Mine real information, not formula count

Use the budget frozen by the user. Search genuinely different economic mechanisms, data sources, state definitions, residual information, event orderings, interactions, and models. Do not spend the campaign mainly changing adjacent windows, thresholds, weights, or names.

For each candidate, record its economic mechanism, fields, formula, expected direction, horizon, applicable state, and what would disprove it. Count separately:

- formulas tested;
- distinct economic mechanisms;
- effective independent information dimensions.

Several statistics computed from the same assets, dates, and future-return label are different views of the same evidence, not independent confirmations.

Use the book's six criteria as a diagnosis and promotion checklist, not as an automatic standalone-profit gate:

- logic: identify a risk-compensation, mispricing, information-flow, or market-mechanism reason;
- persistence: check whether the relationship survives time rather than one fitted interval;
- incremental information: control existing predictors through conditional sorting, regression, or another matching test;
- robustness: vary sensible parameters, algorithms, and subperiods without changing the hypothesis;
- investability: match information decay to holding time and measure turnover, liquidity, and complete costs;
- pervasiveness: test other assets or markets only when the mechanism and data meaning transfer.

A weak legal input may remain useful in a joint model even when it is not a profitable standalone strategy. The six criteria describe the quality and limitations of evidence; they do not authorize silently changing the user's union-of-inputs question into a survivor contest.

## Keep legal weak factors for the joint strategy

Unless the user contract says otherwise, do not require every input to make money alone, cover all fees alone, pass every year, or beat the incumbent before combination.

Remove an input only when it uses future data, cannot be reproduced, produces no usable variation, has a broken mapping, uses an impossible trade, or is proven to be the same information as another input. Otherwise keep weak but legal inputs available to the combined strategy.

For the first joint baseline:

1. put every legal input on a comparable scale at each signal time;
2. combine close variants inside the same economic family;
3. combine families so a family does not gain weight merely because it has more formulas;
4. retain a simple equal-weight or score baseline;
5. run the regularized linear, nonlinear, interaction, or machine-learning combinations allowed by the frozen contract.

If the user's question is “what happens when all legal factors are combined,” run that union directly. Do not replace it with a contest in which each weak factor or weak-factor subset must defeat the original strategy first.

## Turn the factor score into a trading strategy

A cross-sectional rank answers which asset looks better than the others. It does not answer whether any asset is expected to rise enough to buy. A top percentile always exists, so it cannot by itself be an absolute entry rule or a cash switch.

Use the combined score to rank candidates. When the strategy permits cash, separately estimate expected forward absolute return for opening or exiting. For replacement, estimate the new holding's expected improvement over the current holding.

Trade only when the expected improvement over the same horizon is greater than the complete incremental cost and the frozen safety margin. Otherwise keep the current holding or cash. Ranking buffers, minimum holding time, smoothing, and a maximum number of replacements may reduce turnover, but they do not replace this comparison.

Write the position state transition explicitly:

```text
cash -> open
holding -> continue holding
holding -> replace
holding -> exit to cash
blocked or missing executable price -> no new trade
```

`HOLD`, insufficient expected improvement, and blocked execution must produce zero orders. Unchanged membership must not trigger hidden equal-weight restoration. Use the approved engine's orders and holdings to verify the strategy implementation; do not build another account or return calculation.

## Make sample-out-of-sample part of the strategy

The development and sample-out-of-sample periods belong in the strategy definition alongside the formula, weights, holding rule, and costs.

- Use development data to choose factors, directions, transforms, models, thresholds, holding rules, and cost gates.
- Before sample-out-of-sample evaluation, freeze the complete strategy: factor set, combination, entry, hold, replacement, exit, sizing, costs, universe, and dates.
- Run the frozen complete strategy once on the sample-out-of-sample period.
- Do not use that result to tune the same strategy and still call the same period sample-out-of-sample.
- If the period was already examined, label it retrospective validation; genuinely new evidence begins with later data not used to design the strategy.

Do not build database roles, permission services, separate data roots, reveal APIs, access-denied tests, or “mechanical seal” infrastructure for this skill. Use the repository's existing time split and research runner. Sample-out-of-sample discipline is a strategy and research rule unless the user explicitly asks for infrastructure enforcement.

## Implement through the existing research path

Use the local inventory to verify the fields and point-in-time coverage, then implement the factor and complete strategy through the repository's current factor, model, target-weight, and approved backtest paths.

Do not create a new CLI, database, registry, backtester, account, artifact tree, production package, or audit framework. If an actual bug prevents the requested strategy from running correctly, make the smallest repair on the existing path, rerun the strategy, and return to research. Do not turn cleanup, hashes, schemas, permissions, or architecture review into the deliverable.

Use Qlib, VectorBT Pro, or NautilusTrader only as assigned by the current repository rules. The strategy code calculates factors, predictions, trade decisions, and target holdings; the approved engine calculates orders, fills, holdings, cash, fees, and returns.

## Run and diagnose the complete result

At minimum, report:

1. the factors and economic families used;
2. the exact combination or model;
3. what is bought or sold, when, and for how long;
4. the entry, hold, replacement, exit, and sizing rules;
5. the development and sample-out-of-sample dates;
6. gross return, every material cost, net return, drawdown, turnover, and holding duration;
7. how often the strategy stayed in cash, held, replaced, or exited;
8. factor information, combination improvement, and complete-strategy performance as separate conclusions;
9. whether the result depends on one period, asset, or near-duplicate family;
10. the next strategy change supported by the evidence, or the narrow reason to stop.

Lead with the actual strategy result. Use plain Chinese and concrete trading behavior. Mention engineering only when a real defect changed or blocked the result.
