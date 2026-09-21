# GreenShip V1.5

一个半实时绿色航运能源评价网页项目。

## 功能

- 实时模拟柴油、工业电价和岸电价格
- 手动输入船舶与航行参数
- 自动计算柴油、纯电、混合动力方案的成本和碳排放
- 给出推荐方案、成本降低比例和碳排降低比例

## 本机启动

```powershell
pip install -r requirements.txt
python app.py
```

然后打开：

```text
http://127.0.0.1:5055
```

## 让其他电脑访问

双击运行：

```text
start_lan.bat
```

启动后窗口会显示两个地址：

```text
本机打开: http://127.0.0.1:5055
其他电脑打开: http://你的电脑IP:5055
```

让其他电脑和这台电脑连接同一个 Wi-Fi 或同一个局域网，然后在浏览器输入“其他电脑打开”的地址。

如果其他电脑打不开，通常是 Windows 防火墙拦截了 5055 端口。可以允许 Python 通过防火墙，或临时添加入站规则：

```powershell
New-NetFirewallRule -DisplayName "GreenShip V1.5" -Direction Inbound -Protocol TCP -LocalPort 5055 -Action Allow
```

## 让所有人访问

如果不在同一个 Wi-Fi，需要部署到公网平台。项目已加入公网部署配置：

- `Procfile`
- `runtime.txt`
- `render.yaml`
- `DEPLOY_PUBLIC.md`

部署完成后，别人可以通过公网网址访问，例如：

```text
https://greenship-v15.onrender.com
```

详细步骤见：

```text
DEPLOY_PUBLIC.md
```
