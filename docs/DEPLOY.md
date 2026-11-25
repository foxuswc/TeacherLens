# Render 部署
现有 Web Service：Python，main 分支，Build Command: python --version，Start Command: python -m teacherlens.server，Health Check Path: /healthz。无需密钥。Render PORT 自动绑定；公开环境禁止 LLM，网页隐藏不可用选项。建议保留 Free 实例与自动部署。仅模拟样本，无真实学生数据。上线后检查 /healthz、首页、批改和复核导出；本文件不代表实际线上验收已完成。
