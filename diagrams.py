# -*- coding: utf-8 -*-
"""Original teaching figures, rendered as accessible native HTML."""
from diagram_core import tr,node,arrow,flow,frame
from content import SOURCES

def diagram(name,lang):
 t=lambda en,zh:tr(lang,en,zh)
 if name=='trust-boundary':
  title=t('The property lives at a trust boundary','安全属性位于信任边界')
  body='<div class="viz-two">'+node(t('Principal A','主体 A'),t('Ordinary user · tenant A','普通用户 · 租户 A'),'neutral')+node(t('Principal B','主体 B'),t('Owner · tenant B','所有者 · 租户 B'),'neutral')+'</div>'+arrow(t('Both can reach the same API','两者都能访问同一 API'),'down')+node(t('Server-side authorization','服务端授权'),t('Principal + tenant + object + action','主体 + 租户 + 对象 + 动作'),'protected')+'<div class="viz-fork"><div class="viz-branch">'+node(t('Allow B','允许 B'),t('Owner reads their fixture','所有者读取自己的示例'),'protected')+'</div><div class="viz-branch">'+node(t('Deny A','拒绝 A'),t('No protected tenant-B data','不返回租户 B 的受保护数据'),'outside')+'</div></div>'
  caption=t('Synthetic tenant example. Reachability and a valid login do not grant object ownership.','示例租户模型。可达和登录成功不授予对象所有权。');src='asvs'
 elif name=='assessment-loop':
  title=t('A test produces evidence and a next decision','测试产出证据和下一项决策')
  body=flow([node(t('Plan','规划'),t('Goal · scope · identities','目标 · 范围 · 身份'),'neutral'),arrow(),node(t('Discover','发现'),t('Assets · behavior · boundaries','资产 · 行为 · 边界'),'neutral'),arrow(),node(t('Hypothesize','提出假设'),t('A falsifiable expectation','可证伪的预期'),'protected')])+arrow(t('Choose a controlled comparison','选择受控对照'),'down')+flow([node(t('Validate','验证'),t('Observe actual effects','观察实际效果'),'protected'),arrow(),node(t('Explain / fix','解释 / 修复'),t('Root cause + evidence','根因 + 证据'),'neutral'),arrow(),node(t('Retest','复测'),t('Property + legitimate use','属性 + 合法用途'),'protected')])+'<div class="viz-strip">'+t('New observations feed the next hypothesis. Blocked and untested paths remain in the coverage ledger.','新观察反馈给下一条假设。阻塞与未测试路径保留在覆盖记录中。')+'</div>'
  caption=t('An original summary of the assessment loop, not a claim that every engagement uses one fixed order.','对评估闭环的原创概括；不意味着所有评估必须采用固定顺序。');src='nist'
 elif name=='web-request':
  title=t('One request crosses several interpretation boundaries','一次请求跨越多种解释边界')
  body=flow([node(t('Client / proxy','客户端 / 代理'),t('Identity · method · object · input','身份 · 方法 · 对象 · 输入'),'neutral'),arrow(),node(t('Application','应用'),t('Authenticate → authorize → validate state','认证 → 授权 → 验证状态'),'protected'),arrow(),node(t('Backend','后端'),t('Data store · renderer · outbound service','数据库 · 渲染器 · 出站服务'),'neutral')])+'<div class="viz-two">'+node(t('Authorization test','授权测试'),t('Who may perform this action on this object?','谁可对该对象执行此动作？'),'protected')+node(t('Parser / logic test','解析 / 逻辑测试'),t('How does input acquire meaning or change state?','输入如何获得语义或改变状态？'),'outside')+'</div>'
  caption=t('The diagram suggests test questions. It does not imply that every application has all these components.','图示用于提出测试问题，不表示每个应用都有全部组件。');src='api'
 elif name=='segmentation':
  title=t('Test paths from named zones','从明确区域测试路径')
  body='<div class="viz-three"><div class="viz-zone">'+node(t('User zone','用户区'),t('Ordinary workstation','普通工作站'),'neutral')+'</div><div class="viz-zone">'+node(t('Application zone','应用区'),t('Public application service','公开应用服务'),'neutral')+'</div><div class="viz-zone">'+node(t('Management zone','管理区'),t('Administrative control plane','管理控制平面'),'protected')+'</div></div><div class="viz-path-list">'+node(t('User → application','用户 → 应用'),t('Expected allowed path: validate the application identity too','预期允许路径：仍需核验应用身份'),'protected')+node(t('User → management','用户 → 管理'),t('Expected denied path: compare with routing and service controls','预期拒绝路径：结合路由及服务对照'),'outside')+node(t('Admin → management','管理员 → 管理'),t('Expected allowed path only with designated identity and source','仅指定身份和源位置预期允许'),'protected')+'</div>'
  caption=t('Example policy, not a universal architecture. A timeout is ambiguous; an allowed path still needs authentication and authorization.','这是示例策略，不是通用架构。超时有歧义；允许路径仍需认证和授权。');src='nist'
 elif name=='identity-path':
  title=t('A control path is a chain of conditional edges','控制路径由带条件的边组成')
  body=flow([node(t('Test principal','测试主体'),t('Membership / ACL grant','成员关系 / ACL 授权'),'neutral'),arrow(t('Can control?','能够控制？')),node(t('Service identity','服务身份'),t('Delegation / session / credential','委派 / 会话 / 凭据'),'neutral'),arrow(t('Can access?','能够访问？')),node(t('Protected asset','受保护资产'),t('Effective permission + live state','有效权限 + 当前状态'),'protected')])+'<div class="viz-strip">'+t('Collected relationship → validated edge → demonstrated complete path. Do not skip the middle step.','已收集关系 → 已验证边 → 已展示完整路径。不要跳过中间步骤。')+'</div>'
  caption=t('A synthetic relationship graph. The arrows pose questions; they do not represent an executed exploit.','示例关系图。箭头提出问题，不表示已执行利用。');src='bloodhound'
 elif name=='cloud-path':
  title=t('Evaluate the principal and the operation together','结合主体与动作求值')
  body=flow([node(t('Principal / session','主体 / 会话'),t('Issuer · audience · role trust','签发者 · 受众 · 角色信任'),'neutral'),arrow(),node(t('Applicable policy','适用策略'),t('Identity, resource and other policy constraints','身份、资源及其他策略约束'),'protected'),arrow(),node(t('Action on resource','对资源执行动作'),t('Read · write · assume · deploy','读取 · 写入 · 承担角色 · 部署'),'neutral')])+'<div class="viz-two">'+node(t('Policy observation','策略观察'),t('A permission looks possible','某权限看似可能'),'neutral')+node(t('Runtime validation','运行验证'),t('The stated identity performs the scoped action','给定身份执行限定动作'),'protected')+'</div>'
  caption=t('AWS policy interactions have specific rules; this is a reasoning map, not an implementation of IAM evaluation.','AWS 策略交互有具体规则；这是推理图，不是 IAM 求值实现。');src='iam'
 elif name=='host-boundary':
  title=t('Connect writable input to privileged consumption','把可写输入与特权消费连接起来')
  body=flow([node(t('Low-privilege actor','低权限主体'),t('Can write a configuration or artifact?','能写入配置或制品？'),'outside'),arrow(t('Input path','输入路径')),node(t('Privileged consumer','特权消费端'),t('Service · scheduled job · parser','服务 · 定时任务 · 解析器'),'neutral'),arrow(t('Observable effect','可观察效果')),node(t('Security boundary','安全边界'),t('Higher authority or protected data','更高权限或受保护数据'),'protected')])
  caption=t('Prove both control of input and its security-relevant consumption. A writable file alone is not a completed privilege-escalation finding.','同时证明输入可控及其安全相关消费；仅有可写文件不是已完成的提权发现。');src='attack'
 elif name=='mobile-boundary':
  title=t('The device and the server enforce different properties','设备与服务端执行不同属性')
  body='<div class="viz-two"><div class="viz-zone">'+node(t('Device / app','设备 / App'),t('Local storage · IPC · key store · UI','本地存储 · IPC · 密钥库 · UI'),'neutral')+'</div><div class="viz-zone">'+node(t('Server / API','服务端 / API'),t('Identity · object permission · transaction state','身份 · 对象权限 · 事务状态'),'protected')+'</div></div>'+arrow(t('Network request crosses this boundary','网络请求跨越该边界'),'down')+node(t('Test both sides','分别测试两端'),t('Observe a modified client, then check the backend’s decision','观察修改客户端，再检查后端决策'),'protected')
  caption=t('Client tampering is evaluated under the stated device model. It does not by itself prove unauthorized backend access.','客户端篡改按设备模型评价，本身不证明未授权后端访问。');src='mastg'
 elif name=='device-lifecycle':
  title=t('Device trust changes across the lifecycle','设备信任随生命周期变化')
  body=flow([node(t('Enroll','注册'),t('Identity · ownership · initial secrets','身份 · 所有权 · 初始秘密'),'neutral'),arrow(),node(t('Operate / update','运行 / 更新'),t('Commands · firmware verification · rollback','命令 · 固件验证 · 回滚'),'protected'),arrow(),node(t('Reset / retire','重置 / 退役'),t('Secret deletion · ownership transfer','秘密删除 · 所有权转移'),'neutral')])+'<div class="viz-strip">'+t('Device interfaces, companion apps and cloud APIs are separate test surfaces at each phase.','各阶段的设备接口、配套 App 和云 API 都是独立测试面。')+'</div>'
  caption=t('A generic device model. For OT, validate active behavior on an agreed test rig and process-specific schedule.','通用设备模型；OT 的主动行为需在约定测试台和工艺时间安排下验证。');src='iot'
 elif name=='tool-pipeline':
  title=t('A tool result must pass through validation','工具结果必须经过核验')
  body=flow([node(t('Question','问题'),t('Property + identity + scope','属性 + 身份 + 范围'),'protected'),arrow(),node(t('Instrument','测量工具'),t('Known configuration and effects','明确配置与影响'),'neutral'),arrow(),node(t('Observation','观察'),t('Saved raw response or policy state','保存原始响应或策略状态'),'neutral')])+arrow(t('Compare with a control','与控制样本比较'),'down')+node(t('Supported conclusion','有依据的结论'),t('Confidence · impact · limits','置信度 · 影响 · 限制'),'protected')
  caption=t('A template match is an observation. Confirm the boundary failure and report the actual tested impact.','模板命中是观察；应确认边界失败，并报告实际测试影响。');src='nist'
 elif name=='ai-test-loop':
  title=t('Separate proposal, permission and execution','分离建议、权限与执行')
  body=flow([node(t('AI planner','AI 规划器'),t('Suggest hypothesis and action','建议假设和动作'),'neutral'),arrow(t('Proposal','建议')),node(t('Policy runner','策略执行器'),t('Scope · capability · budget checks','范围 · 能力 · 预算检查'),'protected'),arrow(t('Allowed call','允许调用')),node(t('Tool / lab','工具 / 靶场'),t('Bounded operation + raw result','有界操作 + 原始结果'),'neutral')])+arrow(t('Recorded evidence returns to the evaluator','记录证据返回评估器'),'down')+node(t('Evaluate / next hypothesis','评估 / 下一条假设'),t('Deterministic effect checks + human review','确定性效果检查 + 人工评审'),'protected')
  caption=t('An original recommended architecture. A model suggestion or retrieved instruction cannot expand the runner’s authority.','原创建议架构。模型建议或检索指令不能扩大执行器权限。');src='agentic'
 elif name=='agent-boundary':
  title=t('Retrieved content is data, not new authority','检索内容是数据，不是新增权限')
  body='<div class="viz-two">'+node(t('User task / policy','用户任务 / 策略'),t('Defines permitted goal and capability','定义允许目标及能力'),'protected')+node(t('Document / web / memory','文档 / 网页 / 记忆'),t('Potentially attacker-controlled content','可能由攻击者控制的内容'),'outside')+'</div>'+arrow(t('Both may enter context; their trust is different','都可能进入上下文，但信任级别不同'),'down')+flow([node(t('Model / orchestrator','模型 / 编排器'),t('Produces output and tool proposals','产生输出及工具建议'),'neutral'),arrow(),node(t('Independent authorization','独立授权'),t('Checks user + resource + action','检查用户 + 资源 + 动作'),'protected')])
  caption=t('The protected boundary is the eventual resource or action. A prompt injection becomes a finding when a stated security property is violated.','最终资源或动作才是保护边界；提示注入在违反给定安全属性时成为发现。');src='llm'
 elif name=='delegated-tool':
  title=t('The connector must preserve the user’s authority','连接器必须保持用户权限边界')
  body=flow([node(t('Ordinary user','普通用户'),t('Only tenant-A read permission','仅有租户 A 读取权限'),'neutral'),arrow(),node(t('Agent + connector','Agent + 连接器'),t('Carries a tool identity and user context','携带工具身份及用户上下文'),'neutral'),arrow(),node(t('Resource gate','资源授权关口'),t('Enforce tenant-A read only','强制仅允许租户 A 读取'),'protected')])+'<div class="viz-fork"><div class="viz-branch">'+node(t('Tenant A fixture','租户 A 示例'),t('Expected: allow','预期：允许'),'protected')+'</div><div class="viz-branch">'+node(t('Tenant B fixture','租户 B 示例'),t('Expected: deny even if connector has broader credentials','即使连接器凭据更广，也预期拒绝'),'outside')+'</div></div>'
  caption=t('A synthetic confused-deputy test. Transport authentication does not replace per-user resource authorization.','示例困惑代理测试。传输认证不替代逐用户资源授权。');src='mcp'
 elif name=='evidence-ladder':
  title=t('Keep certainty and impact separate','区分确定性与影响')
  stages=[(t('Signal','信号'),t('Banner / alert / unusual response','Banner / 告警 / 异常响应')),(t('Reproduced behavior','复现行为'),t('Controlled comparison repeats','受控对照可重复')),(t('Boundary failure','边界失败'),t('Expected-denied operation succeeds on a fixture','示例中的应拒绝动作成功')),(t('Demonstrated impact','展示影响'),t('The scoped protected asset is reached','到达限定受保护资产'))]
  body='<div class="viz-evidence">'+''.join(node(title,text,'neutral' if i<2 else 'protected',f'{i+1:02}')+(arrow(direction='down') if i<3 else '') for i,(title,text) in enumerate(stages))+'</div>'
  caption=t('The ladder illustrates increasing support for a claim. Severity and business priority must still be evaluated separately.','阶梯表示主张依据逐步增强；严重性和业务优先级仍需独立评价。');src='nist'
 else:raise ValueError(name)
 source=SOURCES[src]
 return frame(lang,name+'-diagram',title,body,caption,source[2],source[1 if lang=='zh' else 0])
