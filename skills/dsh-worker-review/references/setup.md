# DSH and OpenRouter setup

Read this only when preflight reports that `dsh` or its OpenRouter configuration is unavailable.

DeepSeek Harness (`dsh`) is the coding-agent process that edits the selected workspace and runs commands.

This skill does not install DSH automatically. Follow the official DeepSeek Harness installation instructions and verify that an executable `dsh` is on `PATH`, or pass its executable path through `--dsh-bin`. The official package can also be tried without installation with `npx @deepseek-ai/dsh web`, but the runner needs a stable executable command.

Ori is an optional OpenRouter setup program. It opens OpenRouter login, writes the provider/model settings that DSH needs, and lets `dsh` call an OpenRouter model. It does not write project code and is not required when DSH has already been configured directly with an API endpoint and key.

Do not run an installer or model-configuration command merely because it is missing. Explain the external change and obtain authorization first.

When the user chooses Ori, configure the default worker model explicitly:

```bash
ori dsh --model stealth/ox-alpha
```

Ori initializes DSH's `web` profile. This plugin executes the `headless`
profile, so a cold manual setup must also initialize that profile, install the
same Ori-provided OpenRouter plugin there, and let the web profile refresh the
per-user model catalog once:

```bash
dsh --profile headless --help
dsh plugin --profile headless add file:${DSH_HOME:-$HOME/.dsh}/ori/ori-dsh-plugin.tgz
dsh web
```

With the runner, `run --configure-with-ori` performs these headless setup steps
automatically after the user has authorized global configuration.

Then verify both commands:

```bash
command -v ori
command -v dsh
dsh --help
```

Official reference: <https://openrouter.ai/docs/guides/ori/harness>

DeepSeek Harness reference: <https://github.com/deepseek-ai/deepseek-harness>

The model name `stealth/ox-alpha` is an OpenRouter identifier. Do not describe the anonymous model as Xiaomi MiMo or another vendor model unless OpenRouter publishes that identity.
