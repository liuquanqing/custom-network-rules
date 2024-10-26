Clash自用远程配置 #规则库 根据 https://dd.al/config 修改而来 基于https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full.ini
1、添加了Wechat的clash分流规则 
2、优化了广告分流规则
（因为微信转区之后分配的服务器是新加坡，再加上网络上普遍没有这个分流，导致跳ip之后可能对账号有一定的影响，所以自己折腾了这个远程配置）
3、包含bing、OpenAI的分流

# 使用方法
1. 以我常用的“ACL4SSR在线订阅转换”为例
2. 点击“进阶模式”
3. 导入订阅链接（机场、自建的）
4. 远程配置把这个仓库里面的“.ini”结尾的文件地址填上去

