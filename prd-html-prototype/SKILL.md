---
name: prd-html-prototype
description: 生成或组装 HTML 版 PRD 与可浏览产品原型的交付物 Skill。适用于用户要求“PRD 输出成 HTML”“HTML PRD 内嵌 iframe 原型”“把需求文档和原型放在一个页面”“生成可浏览 PRD+原型”“根据 App/H5/Web PC 原型调整 PRD 页面布局”等场景；也适用于已有 PRD Markdown/HTML 和 prototype.html，需要整合成单个评审页面时。
---

# PRD HTML Prototype

把 PRD 和低保真原型组合成一个可浏览交付物：主页面展示 HTML PRD，并通过 iframe 内嵌原型页面。布局必须根据原型终端形态自动调整，确保评审时能同时看清需求和界面。

## 工作流

1. 判断输入材料：需求想法、已有 PRD、原型说明、已有 prototype.html、截图或草稿。
2. 如缺少 PRD，先按 `prd-writer` 的方法补齐 PRD；如缺少原型，先按 `draw-product-prototype` 的方法生成低保真 HTML 原型。
3. 识别原型终端形态：App、H5、小程序、移动 Web、Web PC、SaaS、后台、桌面 Web 或混合端。
4. 生成两个核心文件：`prd.html` 作为评审入口，`prototype.html` 作为 iframe 内嵌原型。
5. 按终端形态选择 iframe 布局，并补齐评审页交互能力：预览/编辑切换、原型收起/展开、设备尺寸切换、流程图放大查看。
6. 在浏览器中检查无重叠、无横向挤压、iframe 可滚动且原型可用；如包含 Mermaid 流程图，必须验证弹框、缩放、拖动画布在 Chrome 中可用。

## 终端形态与布局

必须优先使用用户明确指定的平台；用户未指定时，根据需求内容、页面尺寸、控件密度和业务场景推断，并在输出中标注推断。

- App / H5 / 小程序 / Mobile Web：采用左右结构。左侧为 PRD，右侧为移动端 iframe 原型。移动端 iframe 应使用稳定手机宽度，推荐 390px 到 430px；高度随视口，外层可滚动。
- Web PC / SaaS / 后台 / Admin Console / Desktop Web：采用上下结构。上方为 PRD，下方为宽屏 iframe 原型。iframe 推荐宽度 100%，高度至少 720px，避免 PC 原型被横向压缩。
- 混合端：优先生成分标签或分区块；每个端使用自己的布局规则。不要把移动端和 PC 端原型强塞进同一个 iframe。

布局判断可以使用这些规范化值：

```text
app, h5, mobile, mobile-web, mini-program => side-by-side
web-pc, desktop-web, saas, admin-console, web => stacked
mixed => multi-section
```

## PRD 页面要求

`prd.html` 必须是评审入口，而不是营销页。页面中应包含：

- 标题、版本、平台、更新时间、状态。
- 背景与目标、目标用户、核心场景、范围与非目标。
- 用户流程、功能清单、详细需求、状态与异常、权限或数据规则。
- 验收标准、埋点或度量指标、风险与待确认问题。
- iframe 原型区域，标题清楚标注“原型预览”或具体端名。

PRD 内容较长时，使用侧边目录或顶部锚点；但不要让目录挤压移动端原型。页面应先服务评审阅读，再考虑视觉包装。

## 评审页交互能力

`prd.html` 默认应支持轻量评审编辑，不只是静态阅读：

- 提供“预览 / 编辑”模式切换。入口使用较小的悬浮按钮组，优先放在 PRD 模块右上角或 PRD 区域内，不能遮挡右侧原型 iframe。
- 编辑模式下，PRD 标题、基础信息和正文主要内容应可编辑；编辑结果保存到 `localStorage`，并提供恢复初始内容的能力。
- 编辑模式应聚焦 PRD 内容编辑，可临时隐藏右侧原型，避免 iframe 抢占空间。
- 提供“收起原型 / 展开原型”按钮。默认展示原型；收起后 PRD 区域占满主内容宽度，再次展开恢复原型预览。
- 所有评审控制都应是页面级辅助能力，不要喧宾夺主；按钮尺寸、阴影和层级应克制。

## 原型预览控制

当原型为 App / H5 / 小程序 / Mobile Web 时，右侧预览区应提供设备尺寸切换：

- 默认设备为 `iPhone 15 Pro`。
- 常用设备至少包含：`iPhone 15 Pro`、`iPhone 15`、`iPhone 15 Pro Max`、`iPhone SE`、`Pixel 8`、`Galaxy S24`、`iPad Mini`。
- 预览区头部应紧凑；设备下拉框、当前设备名称和尺寸说明尽量一行展示。
- 设备画布使用 CSS 变量或等价方式控制宽高，iframe 使用相对路径加载 `prototype.html`。
- 切换设备时只改变预览画布尺寸，不应影响 PRD 内容排版或 iframe 内原型状态的基础可用性。

## 流程图与 Mermaid 规范

当 PRD 包含用户流程、状态流转、异常分支或风控校验链路时，应优先将流程渲染为 Mermaid 可视化流程图，而不是只写纯文本步骤。

- 流程图应使用与正文接近的字号，推荐 14px；在不损害理解的前提下优先使用横向 `LR` 布局控制高度。
- Mermaid 面板应包含清晰标题、`Mermaid flowchart` 标识和“放大查看”入口；面板本身也应可点击打开弹框。
- 放大弹框必须兼容 Chrome。不要只依赖页面中已渲染的 SVG；应保留 Mermaid 源码，并在弹框中通过 `mermaid.render()` 重新渲染，失败时再回退复制现有 SVG 或展示源码。
- 打开弹框使用稳定外层事件绑定，例如 `.mermaid-panel` 事件委托，避免 Mermaid 替换内部 DOM 后点击失效。
- 弹框应支持关闭按钮、遮罩点击关闭、ESC 关闭、放大、缩小、重置、鼠标滚轮缩放和拖动画布查看。
- 缩放范围建议控制在 60% 到 240%，避免图形过小不可读或过大导致失控。

## 原型页面要求

`prototype.html` 应是可直接打开的低保真原型，第一屏就是核心产品界面，不要做说明型落地页。原型必须覆盖核心流程，以及必要的空态、加载态、错误态、权限态或边界态。移动端原型要使用固定设备宽度的画布；PC 原型要使用真实工作台、表格、筛选、表单或看板等宽屏结构。

## 组装脚本

当已有 Markdown PRD 和 HTML 原型文件时，可使用：

```bash
python scripts/build_prd_prototype_html.py --title "项目名" --platform app --prd prd.md --prototype prototype.html --out dist
```

脚本会生成 `dist/prd.html`，并复制原型为 `dist/prototype.html`。它只负责稳定组装；PRD 内容质量和原型设计仍由 Codex 按本 Skill 的要求判断。

## 验证清单

交付前检查：

- App/H5/移动端是否为左右结构，且 iframe 呈手机比例。
- Web PC/SaaS/后台是否为上下结构，且 iframe 没有被横向压缩。
- `prd.html` 和 `prototype.html` 均可独立打开。
- iframe 地址为相对路径，便于整体移动目录。
- 页面在桌面和窄屏下无文字重叠；窄屏下左右结构可降级为上下堆叠。
- PRD 与原型中的功能名称、流程、状态和边界保持一致。
- “预览 / 编辑”切换可用，编辑内容可保存到 `localStorage`，恢复初始内容可用。
- “收起原型 / 展开原型”可用，收起后 PRD 不留异常空白，展开后 iframe 正常恢复。
- App/H5/移动端的设备选择器可切换常用设备尺寸，默认是 `iPhone 15 Pro`。
- Mermaid 流程图能正常渲染；放大弹框可从按钮和图表区域打开。
- Mermaid 放大弹框在 Chrome 中支持滚轮缩放、拖动画布、重置和关闭。
- 如外部 CDN 不可用，关键 PRD 内容不能空白；至少保留可阅读的流程文本、Mermaid 源码或降级提示。

## 参考

需要更具体的 HTML/CSS 布局约束时，读取 `references/html-layout-guidelines.md`。
