# 自定义网络分流规则

用于订阅转换的个人规则与模板。仓库提供路由规则，不提供代理节点、机场订阅或转换服务。

## 文件

| 文件 | 用途 |
| --- | --- |
| [Custom_Rule.ini](Custom_Rule.ini) | 当前订阅转换模板，包含规则来源与策略组 |
| [AI.list](AI.list) | AI 服务经典规则列表，可绑定到已有 AI 策略组 |
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

主模板保留历史分组名 `🤖 openAI`，该组实际接管 `AI.list` 中的多种 AI 服务。修改分组名称时，需要同步修改引用它的规则。更新规则仓库与客户端更新节点订阅是两个独立动作；使用独立部署的订阅生成器时，需要由该生成器主动引用或同步这里的文件。

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

