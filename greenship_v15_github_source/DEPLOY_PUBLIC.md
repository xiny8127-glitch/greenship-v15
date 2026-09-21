# GreenShip V1.5 公网发布说明

如果想让不在同一个 Wi-Fi 的人也能访问，需要把项目部署到公网服务器。

推荐使用 Render、Railway、PythonAnywhere 或阿里云/腾讯云。最简单的是 Render。

## 方式一：Render 发布

1. 把 `greenship_v15` 项目上传到 GitHub。
2. 打开 Render，创建一个新的 Web Service。
3. 连接你的 GitHub 仓库。
4. 设置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. 发布完成后，Render 会给你一个公网网址，例如：

```text
https://greenship-v15.onrender.com
```

以后别人打开这个网址，就可以直接使用 GreenShip 网页。

## 方式二：云服务器发布

如果使用阿里云、腾讯云、华为云等服务器：

```bash
pip install -r requirements.txt
gunicorn -w 2 -b 0.0.0.0:5055 app:app
```

然后在服务器安全组里开放 `5055` 端口。

访问地址类似：

```text
http://服务器公网IP:5055
```

## 注意

- 局域网版地址 `192.168.x.x` 只能同 Wi-Fi 使用。
- 公网版必须部署到云服务器或平台，不能只靠自己的电脑直接给所有人稳定访问。
- 如果要正式展示，建议使用 HTTPS 公网链接。
