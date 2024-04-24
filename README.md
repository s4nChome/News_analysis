# 环境配置教程
1. 更新系统软件包
```
sudo apt update
```
2. 安装依赖包
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
3. 添加Docker官方GPG密钥
```
sudo -i
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/trusted.gpg.d/docker-ce.gpg
```
4. 添加Docker阿里稳定版软件源
```
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
```
5. 安装最新版Docker
```
sudo apt install docker-ce docker-ce-cli containerd.io
```
6. 拉取Fakebox镜像
```
docker pull machinebox/fakebox:latest
```
7. 运行Fakebox容器,替换为自己的key
```
docker run -p 8080:8080 -e "MB_KEY=$MB_KEY" machinebox/fakebox
```
8. 克隆本仓库
```
git clone https://github.com/s4nChome/military_news_analysis.git
```
9. 安装后端依赖
```
cd backend
pip install -r requirements.txt
```
10. 启动Flask应用
```
python app.py
```
11. 安装Node.js,npm和Vue脚手架
```
cd frontend
sudo apt install nodejs
sudo apt install npm
sudo npm install -g @vue/cli
```
12. 安装前端依赖
```
sudo npm install
```
13. 启动Vue前端
```
npm run serve
```

