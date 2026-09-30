# -*- coding: utf-8 -*-
"""Build a bilingual penetration testing learning atlas with Python standard library."""
from pathlib import Path
from html import escape
from diagrams import diagram
from content import PAGES, NAV, SOURCES, TOOLS, chapter_content
ROOT = Path(__file__).parent
SITE = 'Penetration Testing Atlas'
REPO = 'penetration-testing'
def pick(lang, en, zh): return zh if lang == 'zh' else en

def href(page, lang, anchor=''):
    return f'{page}{".zh" if lang == "zh" else ""}.html' + (f'#{anchor}' if anchor else '')

def cite(lang, *ids):
    return '<p class="references">' + pick(lang, 'Read the source: ', '对应资料：') + ' · '.join(f'<a href="{SOURCES[i][2]}" target="_blank" rel="noopener noreferrer">{SOURCES[i][1 if lang == "zh" else 0]} ↗</a>' for i in ids) + '</p>'

def para(*texts): return ''.join(f'<p>{t}</p>' for t in texts)

def table(headers, rows):
    return '<div class="table-wrap" tabindex="0"><table><thead><tr>' + ''.join(f'<th scope="col">{h}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>'

def cards(items):
    return '<div class="cards">' + ''.join(f'<article class="card"><span class="eyebrow">{tag}</span><h3>{title}</h3><p>{text}</p></article>' for tag, title, text in items) + '</div>'

def callout(title, text): return f'<aside class="callout"><strong>{title}</strong><p>{text}</p></aside>'

def code(text): return '<pre><code>' + escape(text) + '</code></pre>'

def section(label, title, intro, content, ident):
    return f'<section class="chapter-section" id="{ident}"><span class="eyebrow">{label}</span><h2>{title}</h2><p class="lead">{intro}</p>{content}</section>'

def hero(lang, page, title, text, anchors=()):
    jumps = ''.join(f'<a href="#{ident}">{label}</a>' for ident, label in anchors)
    return f'<section class="page-intro"><div class="wrap"><span class="eyebrow">{NAV[lang][PAGES.index(page)]} / FIELD GUIDE</span><h1>{title}</h1><p>{text}</p><nav class="jump-links" aria-label="{pick(lang, "On this page", "本页目录")}">{jumps}</nav></div></section>'

def shell(lang, page, body):
    current = 'aria-current="page"'
    nav = ''.join(f'<a href="{href(p,lang)}" {current if p == page else ""}>{n}</a>' for p,n in zip(PAGES,NAV[lang]))
    langs = ''.join(f'<a data-atlas-lang="{l}" href="{href(page,l)}" {current if l == lang else ""}>{label}</a>' for l,label in [('en','EN'),('zh','中文')])
    title = SITE if page == 'index' else f'{NAV[lang][PAGES.index(page)]} · {SITE}'
    desc = pick(lang, 'Learn penetration testing methods, attack surfaces, tools, reporting and AI security through diagrams, primary sources and local exercises.', '通过图表、一手资料与本地练习学习渗透测试方法、攻击面、工具、报告及 AI 安全。')
    scripts = '<script src="labs.js" defer></script>' if page == 'labs' else '<script src="tools.js" defer></script>' if page == 'tools' else ''
    prevnext = ''
    if page != 'index':
        idx=PAGES.index(page)
        prevnext = '<nav class="chapter-pager" aria-label="' + pick(lang,'Chapters','章节') + '">'
        prevnext += f'<a href="{href(PAGES[idx-1],lang)}">← {NAV[lang][idx-1]}</a>'
        if idx < len(PAGES)-1: prevnext += f'<a href="{href(PAGES[idx+1],lang)}">{NAV[lang][idx+1]} →</a>'
        prevnext += '</nav>'
    return f'''<!doctype html>
<html lang="{'zh-CN' if lang == 'zh' else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#182638"><meta name="description" content="{desc}"><title>{escape(title)} · ShundaZhang</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="diagrams.css"><script src="language.js"></script>{scripts}</head>
<body><div class="topbar"><div class="wrap"><a href="https://shundazhang.github.io/">← {pick(lang,'Personal home','个人主页')}</a><nav class="languages" aria-label="{pick(lang,'Language selection','语言选择')}">{langs}</nav></div></div><a class="skip" href="#main">{pick(lang,'Skip to content','跳至正文')}</a><header><div class="wrap brand-row"><a class="brand" href="{href('index',lang)}"><span class="brand-mark">P/</span><span>{pick(lang,'PENETRATION TESTING','渗透测试')}<small>LEARNING ATLAS</small></span></a><a class="repo-link" href="https://github.com/ShundaZhang/{REPO}">GitHub ↗</a></div><nav class="chapter-nav wrap" aria-label="{pick(lang,'Main navigation','主导航')}">{nav}</nav></header><main id="main">{body}{'<div class="reading wrap">'+prevnext+'</div>' if prevnext else ''}</main><footer><div class="wrap"><div><strong>{pick(lang,SITE,'渗透测试知识地图')}</strong><p>{pick(lang,'Primary-source notes for systems and security engineers','面向系统与安全工程师的一手资料导读')}</p></div><p>{pick(lang,'Reviewed 30 Sep 2026 · EN / 中文','复核于 2026 年 9 月 30 日 · EN / 中文')}</p></div></footer></body></html>'''



def overview(lang):
    t=lambda en,zh:pick(lang,en,zh)
    map_steps=[('01',t('Property','安全属性'),t('What must this system preserve?','系统必须保护什么？')),('02',t('Principal & scope','主体与范围'),t('From which identity and vantage?','从哪种身份和位置测试？')),('03',t('Controlled comparison','受控对照'),t('What observation would disprove the hypothesis?','什么观察能推翻假设？')),('04',t('Evidence & retest','证据与复测'),t('What failed, what changed, and does the fix hold?','什么失败、修复了什么、是否有效？'))]
    graphic='<aside class="trust-map" aria-label="'+t('Four questions for a test','测试的四个问题')+'"><div class="map-label">THE TESTER’S CHECKPOINTS</div>'+''.join(f'<div class="map-step"><span>{n}</span><div><strong>{title}</strong><small>{desc}</small></div></div>' for n,title,desc in map_steps)+'<div class="map-foot">'+t('A good test connects a claim to observable behavior','好的测试把主张连接到可观察行为')+'</div></aside>'
    body='<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">PENETRATION TESTING / FIELD GUIDE</span><h1>'+t('Learn the methods<br><em>Validate the boundary</em>','掌握测试方法<br><em>验证安全边界</em>')+'</h1><p>'+t('An independent learning map for engineers: major test domains, sound reasoning, practical tools and the changing role of AI. Learn to produce evidence that makes a system easier to fix.','面向工程师的独立学习地图：主要测试方向、严谨推理、实用工具和 AI 带来的变化。学习产出能帮助系统修复的证据。')+'</p><div class="hero-actions"><a class="button" href="'+href('foundations',lang)+'">'+t('Start with foundations →','从基础与理论开始 →')+'</a><a class="text-link" href="'+href('tools',lang)+'">'+t('Explore the tool map ↗','浏览工具地图 ↗')+'</a></div><div class="hero-meta">16 CHAPTERS / 14 DIAGRAMS / 4 LOCAL EXERCISES<br>'+t('ENGLISH & 中文 · PRIMARY SOURCES · 28 TOOLS','中英双语 · 一手资料 · 28 项工具')+'</div></div>'+graphic+'</div></section><div class="reading wrap">'
    routes=[('01',t('Get oriented in two evenings','用两个晚上建立全局视野'),t('Read Foundations and Methodology. Explain scanning versus penetration testing, name a property and draft an assessment scope. Run the evidence and coverage exercises.','阅读基础与方法，解释扫描与渗透测试的区别，明确一项属性并草拟评估范围，完成证据和覆盖练习。')),('02',t('Complete one application assessment','完成一次应用评估'),t('Over one to two weeks, study Web / API with an isolated lab or Academy exercise. Capture paired requests, validate one finding, fix it and retest. Learn a proxy before adding automation.','用一到两周结合隔离靶场或 Academy 练习学习 Web / API，捕获成对请求、验证一项发现、修复并复测。加入自动化前先学会代理。')),('03',t('Choose a specialization','选择一个深入方向'),t('Spend two to four weeks on Network, Identity / AD, Cloud, Host / binary, Mobile or IoT / OT. The domains are independent: choose according to the systems you work with.','用两到四周深入网络、身份 / AD、云、主机 / 二进制、移动端或 IoT / OT。各方向独立，按接触的系统选择。')),('04',t('Add AI and a reproducible report','加入 AI 与可复现报告'),t('Study AI-assisted testing and AI system security separately. Over one to two weeks, evaluate a bounded helper task and one synthetic agent boundary. Write the evidence and retest plan.','分别学习 AI 辅助测试与 AI 系统安全，用一到两周评估一项有界辅助任务和一项示例 Agent 边界，写出证据及复测计划。'))]
    body+=section('01 / LEARNING ROUTE',t('Build depth one assessed system at a time','通过一次次系统评估建立深度'),t('Assumed background: programming and operating-system familiarity. Add HTTP, TCP/IP, identity and cloud basics when a chosen direction needs them. The schedule is optional.','预备知识：编程及操作系统常识；按所选方向补 HTTP、TCP/IP、身份及云基础。时间安排仅供参考。'),'<div class="sequence">'+''.join(f'<article><span>{n}</span><div><h3>{title}</h3><p>{desc}</p></div></article>' for n,title,desc in routes)+'</div>','route')
    descs=[t('Attacker models, trust boundaries and evidence','攻击者模型、信任边界与证据'),t('Hypotheses, comparisons, frameworks and coverage','假设、对照、框架与覆盖'),t('Authorization, injection, sessions and business logic','授权、注入、会话与业务逻辑'),t('Services, segmentation, protocols and wireless','服务、分段、协议与无线'),t('AD, Kerberos, identity graphs and human workflows','AD、Kerberos、身份图与人员流程'),t('IAM, storage, workloads, Kubernetes and CI/CD','IAM、存储、工作负载、Kubernetes 与 CI/CD'),t('Host privilege, reverse engineering and fuzzing','主机权限、逆向与模糊测试'),t('Android / iOS storage, IPC, traffic and backend trust','Android / iOS 存储、IPC、流量与后端信任'),t('Firmware, device lifecycle and physical-process constraints','固件、设备生命周期与工艺约束'),t('28 tools organized by the question they answer','按回答的问题整理 28 项工具'),t('Assistance, controlled agents, benchmarks and trends','辅助、受控 Agent、基准与趋势'),t('LLMs, RAG, connectors, model risks and evaluation','LLM、RAG、连接器、模型风险与评估'),t('Confidence, impact, root cause and regression','置信度、影响、根因与回归'),t('Four interactive exercises with synthetic local data','四项使用本地示例数据的交互练习'),t('Official guides, tool docs, labs and research','官方指南、工具文档、靶场与研究')]
    grid='<div class="topic-grid">'+''.join(f'<a class="topic-card" href="{href(page,lang)}"><span class="eyebrow">{i:02} / FIELD NOTES</span><h3>{NAV[lang][i]}</h3><p>{desc}</p></a>' for i,(page,desc) in enumerate(zip(PAGES[1:],descs),1))+'</div>'
    body+=section('02 / DIRECTIONS',t('Choose your test surface','选择测试面'),t('Each domain has its own entry point. You can use the common method without forcing every domain into one attack chain.','每个方向都有独立入口，可采用共同方法，无需把所有方向拼成一条攻击链。'),grid,'chapters')
    body+=section('03 / FIRST PROJECT',t('The smallest useful deliverable','最小但有价值的产出'),t('A first assessment should be small enough to explain every request and decision.','第一次评估应足够小，以便解释每个请求和决策。'),cards([('TEST',t('Two users, two objects, one property','两个用户、两个对象、一项属性'),t('Compare owner and non-owner reads in a training application. Keep identities and fixtures explicit.','在训练应用比较所有者与非所有者读取，明确身份及示例数据。')),('REPORT',t('One finding, one fix, one retest','一项发现、一项修复、一次复测'),t('State the expected property, observed effect and limits. Verify the fixed behavior and legitimate access.','说明预期属性、实际效果和限制，核验修复行为及合法访问。'))])+cite(lang,'academy','juice','webgoat'),'project')
    return body+'</div>'

def labs(lang):
    t=lambda en,zh:pick(lang,en,zh)
    body=hero(lang,'labs',t('Practice the reasoning<br><em>See what the result proves</em>','练习推理过程<br><em>看清结果证明什么</em>'),t('Four deterministic browser exercises with synthetic data. They make no target requests, execute no tools and use no model service. All results are local simulations.','四项使用示例数据的确定性浏览器练习，不向目标发请求、不执行工具、不调用模型服务；结果均为本地模拟。'),[('authorization',t('Authorization','授权')),('evidence',t('Evidence','证据')),('coverage',t('Coverage','覆盖')),('agent',t('Agent authority','Agent 权限'))])+'<div class="reading wrap">'
    def select(ident,label,options):return '<label for="'+ident+'">'+label+'<select id="'+ident+'">'+''.join(f'<option value="{value}">{text}</option>' for value,text in options)+'</select></label>'
    def buttons(items):return '<div class="lab-actions">'+''.join(f'<button type="button" data-action="{action}">{title}</button>' for action,title in items)+'</div>'
    def box(ident,controls,actions):return f'<div class="lab-box" data-lab="{ident}"><div class="scenario-options">{controls}</div>{buttons(actions)}<p class="lab-state" id="{ident}-state" data-pass="info" role="status" aria-live="polite">'+t('Ready — choose a case','就绪 — 选择案例')+f'</p><div class="lab-output" id="{ident}-output"></div><div id="{ident}-details" class="lab-matrix"></div></div>'
    body+='<noscript><aside class="callout">'+t('Enable JavaScript for interactive exercises. Chapter notes, diagrams and the downloadable report template remain available without it.','交互练习需要 JavaScript；章节、图表及可下载报告模板仍可阅读。')+'</aside></noscript>'
    controls=select('auth-principal',t('Principal','主体'),[('alice',t('Alice · ordinary user · tenant A','Alice · 普通用户 · 租户 A')),('carol',t('Carol · ordinary user · tenant A','Carol · 普通用户 · 租户 A')),('bob',t('Bob · ordinary user · tenant B','Bob · 普通用户 · 租户 B')),('manager',t('Manager · tenant A','Manager · 租户 A'))])+select('auth-object',t('Object','对象'),[('a1',t('A1 · Alice’s invoice · tenant A','A1 · Alice 的账单 · 租户 A')),('a2',t('A2 · Carol’s invoice · tenant A','A2 · Carol 的账单 · 租户 A')),('b1',t('B1 · Bob’s invoice · tenant B','B1 · Bob 的账单 · 租户 B'))])+select('auth-action',t('Action','动作'),[('read',t('Read','读取')),('update',t('Update','更新'))])+select('auth-policy',t('Simulated implementation','模拟实现'),[('tenant-only',t('Tenant filter only','仅租户过滤')),('manager-global',t('Manager bypasses tenant check','Manager 绕过租户检查')),('ui-only',t('UI-only restriction','仅界面限制')),('strict',t('Tenant + object + action checks','租户 + 对象 + 动作检查'))])
    body+=section('01 / AUTHORIZATION',t('Inspect the authorization matrix','检查授权矩阵'),t('Expected rule: ordinary users read only their own invoices; managers read/update within their tenant.','预期规则：普通用户仅读取自己的账单；Manager 可读取 / 更新自己租户中的账单。'),box('authorization',controls,[('auth-case',t('Check selected case','检查所选案例')),('auth-matrix',t('Run all 24 cases','运行全部 24 个案例'))])+para(t('Compare expected and observed decisions, then change the implementation. The local functions deliberately model common omissions; they are not a server or a deployment-ready access-control library. A 200 response without protected data would not by itself establish a read failure.','比较预期与观察决策，再更换实现。本地函数刻意模拟常见遗漏，不是服务端或可部署的访问控制库。没有受保护数据的 200 响应本身不能证明读取失败。'))+cite(lang,'asvs','api'),'authorization')
    controls=select('evidence-case',t('Observation','观察'),[('banner',t('Version banner matches a CVE range','版本 Banner 匹配 CVE 范围')),('status',t('HTTP 200 returns a login page','HTTP 200 返回登录页面')),('boundary',t('Other tenant’s protected fixture is returned','返回另一租户的受保护示例')),('ai',t('AI proposes an unexecuted attack path','AI 建议未执行的攻击路径')),('impact',t('Controlled workflow reaches a protected test asset','受控流程到达受保护测试资产'))])+select('evidence-answer',t('Strongest supported conclusion','证据能支持的最强结论'),[('signal',t('Candidate signal','候选信号')),('behavior',t('Reproduced behavior only','仅复现行为')),('boundary',t('Confirmed boundary failure','已确认边界失败')),('impact',t('Demonstrated scoped impact','已展示限定影响'))])
    body+=section('02 / EVIDENCE',t('Keep the claim within the evidence','让主张不超出证据'),t('Read the provided synthetic observation, choose a conclusion and compare the reasoning.','阅读给定示例观察，选择结论并对照推理。'),box('evidence',controls,[('evidence-show',t('Read observation','阅读观察')),('evidence-check',t('Check conclusion','检查结论'))])+para(t('The categories describe support for a claim, not severity. A severe hypothetical consequence can still be based on an unverified signal.','类别描述主张的依据，不描述严重性。严重的假设后果仍可能只基于未经验证的信号。'))+cite(lang,'nist'),'evidence')
    controls=select('coverage-ledger',t('Synthetic assessment record','示例评估记录'),[('anonymous',t('Anonymous scan only','仅匿名扫描')),('owner',t('One owner session','单个所有者会话')),('matrix',t('Role matrix with a blocked and an unrun case','角色矩阵：一项阻塞、一项未运行'))])
    body+=section('03 / COVERAGE',t('Count what you actually examined','统计实际检查了什么'),t('Planned matrix: four identities × two actions × two session states = 16 cases.','计划矩阵：四种身份 × 两种动作 × 两种会话状态 = 16 项。'),box('coverage',controls,[('coverage-load',t('Inspect coverage ledger','查看覆盖记录'))])+para(t('The ledger is synthetic and distinguishes examined, blocked and not-run cases. Its percentage measures coverage of this stated matrix, not absence of vulnerabilities or overall security. Real coverage also needs routes, inputs, vantage and business state.','记录为示例，区分已检查、阻塞和未运行。百分比仅衡量该矩阵覆盖，不代表无漏洞或整体安全。实际覆盖还需路由、输入、位置和业务状态。'))+cite(lang,'nist','wstg'),'coverage')
    controls=select('agent-origin',t('Proposal originated in','建议来源'),[('task',t('Original task context','原始任务上下文')),('document',t('Retrieved untrusted document','检索到的不可信文档'))])+select('agent-action',t('Proposed action','建议动作'),[('read',t('Read','读取')),('write',t('Write a test marker','写入测试标记'))])+select('agent-resource',t('Proposed resource','建议资源'),[('a',t('Tenant A document','租户 A 文档')),('b',t('Tenant B document','租户 B 文档'))])+select('agent-gate',t('Enforcement','执行检查'),[('credential-only',t('Connector credential only','仅检查连接器凭据')),('strict',t('Task capability + user ACL','任务能力 + 用户 ACL'))])
    body+=section('04 / AGENT AUTHORITY',t('Preserve the original task’s capability','保持原任务的能力边界'),t('Fixed task: an ordinary tenant-A user asks to read one tenant-A document. The connector has broad synthetic credentials.','固定任务：租户 A 普通用户请求读取租户 A 文档；连接器持有范围较广的示例凭据。'),box('agent',controls,[('agent-check',t('Evaluate proposed call','评估建议调用'))])+para(t('Changing the proposal’s origin does not expand the task’s allowed actions. The strict gate checks the existing task capability and user/resource permission. This is a deterministic authority simulation, not a real prompt-injection or LLM benchmark.','更改建议来源不会扩大任务允许动作。严格关口检查原有任务能力及用户 / 资源权限。本练习是确定性权限模拟，不是真实提示注入或 LLM 基准。'))+cite(lang,'agentic','mcp'),'agent')
    body+=section('05 / PRACTICE OUTSIDE THIS PAGE',t('Keep a reproducible test notebook','保留可复现测试笔记'),t('Move from simulated decisions to a small authorized training application.','从模拟决策走向小型获准训练应用。'),'<p class="download"><a href="labs/assessment-template.md" download>'+t('Download the assessment and finding template ↓','下载评估及发现模板 ↓')+'</a></p>'+para(t('Use a PortSwigger Academy lab or a local Juice Shop / WebGoat instance. Record two identities, paired requests, the expected property, an observed effect and one retest. The template includes a coverage ledger and AI-assistance provenance.','使用 PortSwigger Academy 靶场或本地 Juice Shop / WebGoat 实例，记录两个身份、成对请求、预期属性、观察效果及一次复测。模板包含覆盖记录和 AI 辅助来源。'))+cite(lang,'academy','juice','webgoat'),'practice')
    return body+'</div>'

def sources(lang):
    t=lambda en,zh:pick(lang,en,zh)
    body=hero(lang,'sources',t('Read the method<br><em>Check the instrument</em>','阅读方法<br><em>核对测量工具</em>'),t('Primary sources grouped by the question they answer. Standards, awareness lists, living documentation and research have different status and limits.','按所回答问题分组的一手资料。标准、风险认知列表、动态文档和研究有不同状态与限制。'))+'<div class="reading wrap">'
    groups=[('method',t('Scope, method and severity','范围、方法与严重性'),t('SP 800-115 is a published 2008 method reference, not a current tool guide. WSTG v4.2 and ASVS 5.0.0 are distinguished from evolving content and awareness lists.','SP 800-115 是 2008 年已发布方法资料，不是当前工具指南；WSTG v4.2、ASVS 5.0.0 与动态内容及风险列表分开标注。'),['nist','model','wstg','asvs','top10','api','attack','cwe','cvss','epss']),('learn',t('Training applications and learning material','训练应用与学习资料'),t('Academy is free training; account requirements may apply to labs or progress. Local vulnerable applications should be kept in a disposable training environment.','Academy 提供免费训练；靶场或进度功能可能需账号。本地脆弱应用应放在可丢弃训练环境。'),['academy','juice','webgoat','masvs','mastg']),('network',t('Network and application instruments','网络及应用测量工具'),t('Read the selected function and edition before interpreting a result or running a check.','解释结果或运行检查前，阅读所选功能及版本说明。'),['nmap','wireshark','aircrack','burp','zap','mitmproxy','ffuf','sqlmap','nuclei','nessus','greenbone','metasploit']),('identity',t('Identity and cloud','身份与云'),t('Use platform documentation for effective authorization and tool documentation for data collection behavior.','用平台文档核对有效授权，用工具文档核对数据收集行为。'),['kerberos','entra','bloodhound','impacket','netexec','hashcat','iam','k8s','prowler','scout','trivy','kubebench']),('code',t('Code, runtime and devices','代码、运行时及设备'),t('Offline artifact analysis, instrumentation and fuzzing are complementary. The IoT project includes historical material; OT requires process-specific context.','离线制品分析、插桩和模糊测试相互补充。IoT 项目含历史资料；OT 需要工艺背景。'),['ghidra','frida','afl','semgrep','codeql','iot','ot']),('ai',t('AI risk, protocol and evaluation','AI 风险、协议与评估'),t('Versioned risk guides organize questions. Developing projects and research benchmarks are not universal guarantees of safety or automation capability.','注明版本的风险指南用于整理问题。开发中项目和研究基准不提供通用安全或自动化能力保证。'),['llm','agentic','aml','atlas','mcp','aitg','garak','pyrit','pentestgpt','paper','benchmark'])]
    for n,(ident,title,intro,ids) in enumerate(groups,1):
        grid='<div class="source-grid">'+''.join(f'<a class="source-card" href="{SOURCES[i][2]}" target="_blank" rel="noopener noreferrer"><span class="eyebrow">{SOURCES[i][3]}</span><h3>{SOURCES[i][1 if lang=="zh" else 0]} ↗</h3></a>' for i in ids)+'</div>'
        body+=section(f'{n:02} / PRIMARY SOURCES',title,intro,grid,ident)
    return body+'</div>'

if __name__ == '__main__':
    for page in PAGES:
        for lang in ('en','zh'):
            if page=='index': body=overview(lang)
            elif page=='labs': body=labs(lang)
            elif page=='sources':body=sources(lang)
            else:
                info,parts=chapter_content(page,lang)
                body=hero(lang,page,info[0],info[1],[(p[4],p[1]) for p in parts])+'<div class="reading wrap">'
                for label,title,intro,body_text,ident,figure,refs in parts:
                    body+=section(label,title,intro,(diagram(figure,lang) if figure else '')+body_text+cite(lang,*refs),ident)
                body+='</div>'
            (ROOT/href(page,lang)).write_text(shell(lang,page,body),encoding='utf-8')
    print(f'Built {len(PAGES)*2} bilingual pages; {len(TOOLS)} tools; {len(SOURCES)} primary sources')
