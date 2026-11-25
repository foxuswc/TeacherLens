# TeacherLens · 教师评价智能体

> 让 AI 理解教师的评价意图，而不是把参考答案当成唯一答案。

面向千问办公教育场景的独立解决方案原型（非官方产品）。V0.6 聚焦初中语文阅读理解：规则校准、逐项证据、人工确认、反馈归因、同源评测。全部示例为模拟数据。尚未开展真实教师试用、千问办公安装验证或钉钉接口集成。

## 快速开始
Python 3.10+，仅标准库，不需要安装第三方依赖。

```bash
python -m teacherlens.server
# 浏览器打开 http://127.0.0.1:8765
python -m teacherlens.cli --engine demo --out outputs/demo
python -m unittest discover -s tests -v
```

离线 demo 使用刻意不完美的关键词匹配，**不是大模型推理**，指标仅验证流程和计算。网页包含任务级边界校准、版本化规则、人工复核筛选、仅已确认结果统计、同源评测实验室和试点交付资料。刷新会清除本轮浏览器内存记录，请及时导出；当前无服务端持久化及多用户权限。

### 可选真实 LLM
在自己的终端设置密钥（不要提交到仓库）：

```bash
export TEACHERLENS_API_KEY='your-key'
export TEACHERLENS_MODEL='qwen-plus'
# 默认兼容 DashScope 中国区；可按账户地域及供应商设置 BASE_URL
export TEACHERLENS_BASE_URL='https://dashscope.aliyuncs.com/compatible-mode/v1'
python -m teacherlens.cli --engine llm --out outputs/llm
```

也可以重新启动本地服务，在已配置密钥且非公开模式的网页选择 LLM。Render 公开版本禁用模型调用。调用会向所配置服务商发送输入内容、产生费用；仅使用模拟/获授权材料。API 路径采用 OpenAI 兼容 Chat Completions 格式，尚未进行联网模型调用验证，模型名称、区域及服务权限以账户为准。大模型可能返回错误或非法 JSON；失败明确报错，不自动生成虚假结果。三个模式依次调用同一模型，采用相同输入；评测需另记录具体模型版本及运行配置。

## 千问办公 Skill
`skills/teacher-evaluation/` 是独立技能目录，含 SKILL.md、示例量规、校验脚本。可尝试使用客户端自定义技能功能导入（请遵循当前产品实际导入要求），随后提供模拟任务并逐步确认。没有声称已通过官方安装或兼容性测试。无需接入真实班级数据。

## 目录
- `teacherlens/`：评分接口、校验、反馈及 CLI/本地服务
- `web/`：教师评价交互原型
- `skills/`：技能指令与辅助文件
- `data/demo.json`：2 个校准样本、12 个独立模拟测试作答
- `docs/`：行业解决方案、教师访谈及 POC 设计
- `tests/`：流程与安全边界单元测试

## 核心边界
证据字面匹配不证明语义正确；复核标记尚未校准，不得作为自动放行依据。所有分数均为初评，教师确认才是最终业务结果。规则候选不自动生效。模拟参考分数仅用于开发测试；跨任务泛化、真实提效与质量指标需真实试验。禁止将学生身份信息、密钥、内部客户资料或实际访谈记录上传公开仓库。

## v0.6 交付与部署
Render 使用 Python Web Service，启动命令 `python -m teacherlens.server`，自动绑定 PORT，健康检查 /healthz；详见 [部署说明](docs/DEPLOY.md)。试点使用 [PILOT_KIT](docs/PILOT_KIT.md)、访谈及问题台账模板。在线实验室为固定模拟测试集，指标现场重新计算，不代表真实效果。

## 版本记录
- v0.2：公开演示安全、图标、Render配置。
- v0.3：两项边界选择、任务级规则版本与不确定性复核。
- v0.4：复核筛选、仅确认结果统计、过期记录检查。
- v0.5：同源评测、校准前后逐样本比较、数据集隔离检查。
- v0.6：可下载交付材料，教师试点操作与验收模板。

上述为工程原型的迭代记录，教师试点及真实大模型评估仍待开展。
