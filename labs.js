/* Deterministic teaching simulations. No networking, tool execution, models or storage. */
(() => {
  'use strict';
  const zh = document.documentElement.lang.startsWith('zh');
  const t = (en, cn) => zh ? cn : en;
  const value = id => document.getElementById(id).value;
  const show = (lab, state, output, pass = 'info') => {
    const status = document.getElementById(`${lab}-state`);
    status.textContent = state;
    status.dataset.pass = String(pass);
    document.getElementById(`${lab}-output`).textContent = output;
    document.getElementById(`${lab}-details`).replaceChildren();
  };
  function renderTable(lab, headers, rows) {
    const wrap = document.createElement('div'); wrap.className = 'table-wrap'; wrap.tabIndex = 0;
    const table = document.createElement('table'); const head = document.createElement('thead'); const headRow = document.createElement('tr');
    headers.forEach(text => { const th = document.createElement('th'); th.scope = 'col'; th.textContent = text; headRow.append(th); });
    head.append(headRow); table.append(head); const body = document.createElement('tbody');
    rows.forEach(row => { const tr = document.createElement('tr'); row.forEach(text => { const td = document.createElement('td'); td.textContent = text; tr.append(td); }); body.append(tr); });
    table.append(body); wrap.append(table); document.getElementById(`${lab}-details`).append(wrap);
  }
  const principals = {
    alice: {name: 'Alice', tenant: 'A', role: 'user'},
    carol: {name: 'Carol', tenant: 'A', role: 'user'},
    bob: {name: 'Bob', tenant: 'B', role: 'user'},
    manager: {name: 'Manager', tenant: 'A', role: 'manager'}
  };
  const objects = {
    a1: {id: 'A1', tenant: 'A', owner: 'alice', fixture: 'SYNTHETIC-INVOICE-A1'},
    a2: {id: 'A2', tenant: 'A', owner: 'carol', fixture: 'SYNTHETIC-INVOICE-A2'},
    b1: {id: 'B1', tenant: 'B', owner: 'bob', fixture: 'SYNTHETIC-INVOICE-B1'}
  };
  function expected(principalId, objectId, action) {
    const p = principals[principalId], o = objects[objectId];
    return p.tenant === o.tenant && (action === 'read' ? o.owner === principalId || p.role === 'manager' : p.role === 'manager');
  }
  function observed(policy, principalId, objectId, action) {
    const p = principals[principalId], o = objects[objectId];
    if (policy === 'ui-only') return true;
    if (policy === 'tenant-only') return p.tenant === o.tenant;
    if (policy === 'manager-global') return p.role === 'manager' || expected(principalId, objectId, action);
    return expected(principalId, objectId, action);
  }
  const decision = allowed => allowed ? t('ALLOW', '允许') : t('DENY', '拒绝');
  const evidenceCases = {
    banner: {answer: 'signal', observation: t('A service returns an old version string. A scanner links the string to a CVE. Build, backports, required configuration and exploit behavior are unverified.', '服务返回旧版本字符串，扫描器关联到 CVE。构建、回补、所需配置和利用行为均未验证。'), reason: t('This supports a candidate for investigation. A version string alone does not demonstrate the vulnerability.', '这支持待调查候选。版本字符串本身不证实漏洞。')},
    status: {answer: 'behavior', observation: t('Three controlled owner/non-owner request pairs return HTTP 200. Every response body is the same login page, with no protected invoice fields. No unauthorized read is observed.', '三组受控所有者 / 非所有者请求都返回 HTTP 200，响应均为同一登录页，没有受保护账单字段，未观察到未授权读取。'), reason: t('Only the repeated response behavior is established. HTTP 200 does not establish access to the protected object.', '仅确立了重复响应行为。HTTP 200 不确立对受保护对象的访问。')},
    boundary: {answer: 'boundary', observation: t('Two tenant fixtures are owned by different test users. A controlled non-owner request repeatedly returns the other tenant’s protected synthetic invoice fields. The owner mapping and identity are recorded. No broader workflow is tested.', '两个租户示例分别属于不同测试用户。受控非所有者请求重复返回另一租户的受保护示例字段，归属及身份已记录，未测试更广工作流。'), reason: t('The tenant/object read boundary failed in this case, demonstrating a limited disclosure. Do not claim untested writes or a larger compromise.', '本案例租户 / 对象读取边界失败，展示了限定泄漏。不要声称未测试的写入或更大失陷。')},
    ai: {answer: 'signal', observation: t('An AI assistant proposes a multi-step control path from a permission export. No edge has been validated, no commands run and no protected asset accessed.', 'AI 助手根据权限导出建议一条多步控制路径。没有边经过验证，没有执行命令，也未访问受保护资产。'), reason: t('This is a proposed hypothesis, not an executed path. Validate each prerequisite before claiming the outcome.', '这是待验证假设，不是已执行路径。声称结果前须验证每个前提。')},
    impact: {answer: 'impact', observation: t('In an isolated lab, a recorded sequence crosses a confirmed delegation flaw and reads the agreed protected synthetic report. Independent service logs and the returned fixture ID verify the scoped objective. Cleanup is recorded.', '隔离靶场中，一条已记录序列跨越确认的委派缺陷并读取约定受保护示例报告。独立服务日志及返回的示例标识验证了限定目标，清理也已记录。'), reason: t('The stated objective was reached under the given lab conditions. This does not establish other environments, persistence or access to unrelated records.', '给定靶场条件下达成了声明目标；不证明其他环境、持久化或无关记录访问。')}
  };
  const conclusion = answer => ({signal:t('Candidate / hypothesis','候选 / 假设'),behavior:t('Reproduced behavior','复现行为'),boundary:t('Confirmed boundary failure','已确认边界失败'),impact:t('Demonstrated scoped impact','已展示限定影响')})[answer];
  const actions = {
    'auth-case'() {
      const pId = value('auth-principal'), oId = value('auth-object'), action = value('auth-action'), policy = value('auth-policy');
      const want = expected(pId, oId, action), got = observed(policy, pId, oId, action);
      const p = principals[pId], o = objects[oId];
      show('authorization', want === got ? t('Decision matches the expected rule for this case', '本案例决策符合预期规则') : t('Authorization boundary failure in this simulation', '本模拟出现授权边界失败'),
        `Principal: ${p.name} / tenant ${p.tenant} / ${p.role}\nObject: ${o.id} / tenant ${o.tenant} / owner ${o.owner}\nAction: ${action}\nPolicy: ${policy}\nExpected: ${decision(want)}\nObserved: ${decision(got)}\n\n` +
        (got ? action === 'read' ? `Simulated response: 200 + ${o.fixture}` : t('Simulated effect: test marker would be updated', '模拟效果：测试标记将被更新') : t('Simulated response: denied, no protected fields', '模拟响应：拒绝，不返回受保护字段')), want === got);
    },
    'auth-matrix'() {
      const policy = value('auth-policy'); const rows = []; let failures = 0;
      Object.keys(principals).forEach(pId => Object.keys(objects).forEach(oId => ['read','update'].forEach(action => {
        const want = expected(pId,oId,action), got = observed(policy,pId,oId,action); const match = want === got;
        if (!match) failures++;
        rows.push([principals[pId].name, objects[oId].id, action, decision(want), decision(got), match ? t('MATCH','一致') : t('VIOLATION','违反')]);
      })));
      show('authorization', t(`${failures} violations across 24 synthetic cases`, `24 项示例案例中有 ${failures} 项违反`), t('Every principal × object × action combination was evaluated by local simulation. This is not evidence about any live application.', '本地模拟评估了全部主体 × 对象 × 动作组合，不是关于任何实际应用的证据。'), failures === 0);
      renderTable('authorization',[t('Principal','主体'),t('Object','对象'),t('Action','动作'),t('Expected','预期'),t('Observed','观察'),t('Result','结果')],rows);
    },
    'evidence-show'() {
      const item = evidenceCases[value('evidence-case')];
      show('evidence',t('Read the observation, then choose the strongest supported claim','阅读观察后选择证据能支持的最强主张'),item.observation);
    },
    'evidence-check'() {
      const item = evidenceCases[value('evidence-case')]; const correct = value('evidence-answer') === item.answer;
      show('evidence',correct ? t('The conclusion stays within the evidence','结论没有超出证据') : t('Reconsider the evidence boundary','重新考虑证据边界'),
        item.observation+'\n\n'+t('Supported conclusion: ','有依据的结论：')+conclusion(item.answer)+'\n'+item.reason+'\n\n'+t('These are teaching labels. A confirmed boundary failure can already demonstrate a limited impact; the larger objective must be evidenced separately.', '这些是教学标签。确认边界失败可能已展示限定影响；更大的目标需要独立证据。'),correct);
    },
    'coverage-load'() {
      const mode = value('coverage-ledger'); const rows = []; let examined = 0, blocked = 0; let i = 0;
      ['owner','peer','other-tenant','anonymous'].forEach(principal => ['read','update'].forEach(action => ['active','revoked'].forEach(session => {
        let status = 'not-run';
        if (mode === 'anonymous' && principal === 'anonymous' && session === 'active') status = 'examined';
        if (mode === 'owner' && principal === 'owner' && session === 'active') status = 'examined';
        if (mode === 'matrix') status = i === 7 ? 'blocked' : i === 15 ? 'not-run' : 'examined';
        if (status === 'examined') examined++; if (status === 'blocked') blocked++;
        rows.push([principal,action,session,{examined:t('Examined','已检查'),blocked:t('Blocked','阻塞'),'not-run':t('Not run','未运行')}[status]]); i++;
      })));
      const percentage = examined / 16 * 100;
      show('coverage',t(`${examined}/16 planned cases examined (${percentage}%)`, `计划 16 项中检查 ${examined} 项（${percentage}%）`),
        t(`Synthetic ledger only\nExamined: ${examined}\nBlocked: ${blocked}\nNot run: ${16-examined-blocked}\n\nCoverage is not a guarantee that no vulnerabilities exist.`, `仅为示例记录\n已检查：${examined}\n阻塞：${blocked}\n未运行：${16-examined-blocked}\n\n覆盖不保证不存在漏洞。`));
      renderTable('coverage',[t('Identity','身份'),t('Action','动作'),t('Session','会话'),t('Ledger state','记录状态')],rows);
    },
    'agent-check'() {
      const origin = value('agent-origin'), action = value('agent-action'), resource = value('agent-resource'), gate = value('agent-gate');
      // Fixed original task and user ACL permit only read(A); provenance cannot widen them.
      const allowed = action === 'read' && resource === 'a';
      const observed = gate === 'credential-only' || allowed;
      show('agent', allowed === observed ? t('The current proposal preserves the task boundary','当前建议保持任务边界') : t('Broad connector credentials exceeded the user task','广泛连接器凭据超出了用户任务'),
        `Original task: read tenant-A document\nUser permission: tenant-A read\nConnector credential: broad read/write (synthetic)\nProposal origin: ${origin}\nProposed call: ${action}(tenant-${resource.toUpperCase()})\nEnforcement: ${gate}\nExpected: ${decision(allowed)}\nObserved: ${decision(observed)}\n\n`+
        (observed ? action === 'read' ? `Simulated result: SYNTHETIC-TENANT-${resource.toUpperCase()}-DOCUMENT` : t('Simulated effect: a test marker would be written', '模拟效果：将写入测试标记') : t('Call rejected before resource access', '资源访问前拒绝调用'))+
        '\n\n'+t('No tool or model was called. Proposal origin does not grant a new capability.', '未调用工具或模型。建议来源不授予新能力。'),allowed === observed);
    }
  };
  document.querySelectorAll('[data-action]').forEach(button => button.addEventListener('click',() => actions[button.dataset.action]()));
  document.querySelectorAll('[data-lab]').forEach(box => {
    if (box.dataset.lab === 'evidence') return;
    box.querySelectorAll('select').forEach(select => select.addEventListener('change',() => {
      show(box.dataset.lab,t('Selection changed — run this case again','选择已改变 — 请重新运行案例'),'');
    }));
  });
  ['evidence-case','evidence-answer'].forEach(id => document.getElementById(id).addEventListener('change',() => {
    show('evidence',t('Selection changed — read the case and check again','选择已改变 — 阅读案例后重新检查'),evidenceCases[value('evidence-case')].observation);
  }));
})();
