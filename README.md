# 自定义网络分流规则

用于订阅转换的个人规则与模板。仓库提供路由规则，不提供代理节点、机场订阅或转换服务。

## 文件

| 文件 | 用途 |
| --- | --- |
| [Custom_Rule.ini](Custom_Rule.ini) | 当前订阅转换模板，包含规则来源与策略组 |
| [rules/aigc-shared.json](rules/aigc-shared.json) | 共享自定义规则的唯一维护入口，不含节点或实际策略组名称 |
| [AI.list](AI.list) | 自动生成的 AI 经典规则列表，可绑定到已有 AI 策略组 |
| [rules/AI.legacy.list](rules/AI.legacy.list) | 仅供公开模板兼容的历史规则，不整包导入现网 |
| [direct.list](direct.list) | 个人直连补充 |
| [other.list](other.list) | 其他代理补充 |
| [reject.list](reject.list) | 预留的拦截补充，目前为空 |
| [Custom_Rule_bak.ini](Custom_Rule_bak.ini) | 历史配置备份；包含旧服务引用，不作为当前推荐入口 |

## 使用方法

在你已有的、可信的订阅转换器中导入自己的节点订阅，将“自定义配置”设为：

```text
https://raw.githubusercontent.com/liuquanqing/custom-network-rules/main/Custom_Rule.ini
```

如果只需要 AI 规则，使用：

```text
https://raw.githubusercontent.com/liuquanqing/custom-network-rules/main/AI.list
```

将这份列表绑定到你已有的 AI 策略组即可，组名不必固定为 AIGC。`AI.list` 使用 `DOMAIN`、`DOMAIN-SUFFIX`、`DOMAIN-KEYWORD` 等经典规则语法，不是只含域名的 Mihomo `behavior: domain` 列表。

主模板保留历史分组名 `🤖 openAI`，该组实际接管 `AI.list` 中的多种 AI 服务。修改分组名称时，需要同步修改引用它的规则。

## 统一维护

以后更新共享的 Claude、Cursor、Grok/登录及 AIGC 补充域名，只维护 [rules/aigc-shared.json](rules/aigc-shared.json)。每个 section 声明匹配类型、域名和语义策略 `aigc` / `grok`，消费端映射到自己的分组；不要在这里填写节点、订阅链接或凭据。

- 公开 `AI.list` 由共享数据和 `rules/AI.legacy.list` 导出。共享数据中的语义策略在这个经典列表里被展平，最终分组由使用者绑定。
- 推送到 `main` 后，GitHub Actions 校验数据并自动提交有变化的 `AI.list`。无效数据不会覆盖已有导出；自动导出提交使用仓库自带的 Actions token，不需要保存个人令牌。
- 现网订阅生成器只下载共享 JSON，不执行仓库代码。每次完整刷新先将 `main` 解析为具体提交，再按不可变 SHA 取件；通过生成与配置验证后才记为已使用的版本。取件或数据校验失败时沿用上一份已验证数据，无有效缓存则保留旧订阅并报告失败。
- 现网还会核对同一 SHA 下 `AI.list` 的共享区段。如果 Actions 尚未完成导出，或公开文件与共享数据不一致，就继续沿用已验证版本，避免仓库和现网各用一套规则。
- 历史公开规则仍由 `rules/AI.legacy.list` 管理，只影响公开经典列表；它们不会因为本次统一而全部进入现网。节点、分组名称、节点选择与本地路由策略仍由各消费端管理。

### 别人的规则更新，会不会漏掉？

主模板直接引用 blackmatrix7 的 OpenAI、Claude、Copilot、Gemini、Bing，以及 ACL4SSR 的 AI 聚合源。上游在原地址更新内容后，重新转换订阅会按这些地址取件，不需要把别人的仓库手工合并到本仓库。现网也保留这些直接上游引用；实际取到的版本受 CDN、转换器缓存和下载是否成功影响，不保证实时到达，取件失败时会继续使用已验证内容。

`rules/AI.legacy.list` 是历史复制内容，属于本仓库自己的兼容补充，不会自动合并别人的改动。生成的 `AI.list` 也不是这些上游的全量实时镜像。需要完整分流时使用 `Custom_Rule.ini`，或同时配置对应上游规则；不要只下载 `AI.list` 就假定所有上游更新都已包含在里面。共享 JSON 管理的是我们自己的例外规则，新增产品域名是否已被上游收录，仍需依据官方资料核查。

本地或 PR 更新后运行：

```sh
python3 tools/render_rules.py
python3 tools/render_rules.py --check
python3 -m unittest discover -s tests -v
```

PR 会检查导出文件是否最新。直接在 GitHub 编辑 `main` 时，只需编辑共享 JSON，等待 Actions 导出成功。没有通过 Actions 或现网验证的更新，不应当作已经生效。客户端加载仍取决于其订阅刷新，仓库同步不操作客户端。

## 2026-10-29 维护

- Claude：补充 `claude.com`、`claude.app`、`claudeusercontent.com`、`claudemcpcontent.com`，覆盖新登录入口、动态预览和内容子域名。
- GitHub Copilot：补充 `githubcopilot.com` 后缀，覆盖分套餐子域名。
- Together：补充当前使用的 `together.ai` 后缀。
- OpenAI：补充 `oaistatsig.com` 后缀。
- 主模板的三个本仓库引用统一使用真实的 `main` 分支。

本次以补充明确域名为主，保留原有分组和其他规则。历史列表中部分共享登录、统计与 CDN 域名的匹配范围较宽，不能把它理解为各产品所有依赖的官方完整清单。验证规则匹配也不等于验证实际账号登录或客户端连接。

## 来源

本仓库 fork 自 [Flora-air/custom-network-rules](https://github.com/Flora-air/custom-network-rules)。主模板沿用 [ACL4SSR](https://github.com/ACL4SSR/ACL4SSR) 和 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) 的相关规则。

本次域名补充依据：

- [Claude Desktop 网络要求](https://code.claude.com/docs/en/desktop#network-access-requirements)
- [Claude Code 网络要求](https://code.claude.com/docs/en/network-config#network-access-requirements)
- [GitHub Copilot 域名清单](https://docs.github.com/en/copilot/reference/copilot-allowlist-reference)
- [Together API 文档](https://docs.together.ai/docs/inference/openai-compatibility)
- [OpenAI 网络说明](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)

