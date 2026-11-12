# 贡献指南（CONTRIBUTING）

本文约定洪城漫游项目的分支、提交、Pull Request 与评审规则。所有进入 `main` 的变更都必须走完本文流程。

## 一、分支模型

`main` 为受保护分支，禁止直接推送。任何改动都从最新的 `main` 切出短期分支，合并后立即删除。

| 类型 | 命名格式 | 示例 |
| --- | --- | --- |
| 新功能 | `feature/<issue号>-<英文短横线简述>` | `feature/12-amap-map` |
| 缺陷修复 | `bugfix/<issue号>-<英文短横线简述>` | `bugfix/21-empty-route` |
| 紧急修复 | `hotfix/<issue号>-<英文短横线简述>` | `hotfix/30-token-leak` |
| 文档 / 构建 | `chore/<英文短横线简述>` | `chore/ci-add-coverage` |

```powershell
git switch main
git pull origin main
git switch -c feature/12-amap-map
```

分支生命周期建议不超过 3 天；长期未合并的分支要拆小或及时同步 `main`。

## 二、提交规范（Conventional Commits）

```
<type>(<scope>): <subject>
```

- `type` 取值：`feat` `fix` `docs` `test` `refactor` `style` `chore` `perf`
- `subject` 使用英文祈使句，首字母小写，结尾不加句号，一行不超过 72 字符
- 一个提交只做一件事；正文说明 **why**，不重复 **what**

```
feat(route): add nearest neighbour ordering for selected pois
fix(api): reject facility poi when creating a route
test(algorithm): cover zero and single poi routes
docs(readme): add mysql switch instructions
```

不合格示例：`update`、`修改`、`fix bug`、`final`、`真的最终版`、`asdf`。

## 三、Pull Request 流程

1. 推送分支：`git push -u origin feature/12-amap-map`
2. 在 GitHub 创建 PR，使用仓库的 PR 模板填写：关联 Issue（`Closes #12`）、变更说明、变更类型、测试说明、自查清单。
3. 至少 1 名**非作者**成员 Review 并 Approve；作者不得自评自合。
4. CI 全绿（后端测试 + 前端构建）后方可合并，合并方式统一用 Squash 或 Merge commit，不使用 Rebase 强推。
5. 合并后删除远端分支，并在 Issue 中确认已自动关闭。

单个 PR 建议控制在 400 行以内；超过 800 行必须说明理由并拆分。

## 四、评审要求

评审意见必须**有定位、有理由、有建议**，优先使用行内评论（Inline comment）指到具体代码行。

有效：

```
[backend/app/api/route.py:43] 这里用 409 表示重复点位，但前端把非 2xx 一律当作
"网络异常"提示，用户看不到"同一点位不能重复"。建议后端在 message 中给出可展示文案，
或前端按 status 分流。
```

无效：`可以`、`没问题`、`+1`、只点 Approve 不写评论。

## 五、代码要求

- Python：遵循 PEP 8，函数职责单一，公共函数写 docstring；不得提交调试 `print` 与注释掉的大段代码。
- 前端：组件单文件、命名语义化；样式使用 `styles/tokens.css` 中的设计 Token，不写魔法色值。
- 禁止提交密钥、数据库口令、`.env`、数据库文件与 `node_modules`、`.venv` 等自动生成物。
- 新增依赖须同步更新 `requirements.txt` / `package.json`，并在 PR 中说明引入理由。

## 六、测试要求

- 改动业务逻辑必须补充或更新 `backend/tests/` 下的用例，禁止空断言。
- 本地自测命令：

```powershell
cd backend
pip install -r requirements.txt -r requirements-dev.txt
pytest --cov=app/services --cov-report=term-missing
```

- 前端改动至少保证 `npm run build` 通过，并在 PR 中附截图或 GIF。

## 七、完成定义（Definition of Done）

一个任务算「完成」需同时满足：

1. 有对应 Issue，且 Issue 的验收标准逐条勾选。
2. 代码经 PR 合并到 `main`，有至少 1 条实质性评审意见。
3. CI 通过，相关测试已补充。
4. 文档（README / API / CHANGELOG）在需要时已同步。
5. Issue 由 PR 自动关闭，无遗留待办。
