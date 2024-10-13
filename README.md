# CORS Proxy

## 简介

本项目是一个用于处理跨域请求的 CORS 代理服务器，使用 Python 和 Flask 实现，并通过 Docker 镜像进行部署。该代理服务器支持 GET、POST、PUT、DELETE 等常见的 HTTP 请求，并通过可配置的白名单和黑名单来控制允许访问的目标域名。

## 功能特点

- **支持多种 HTTP 请求方式**：包括 GET、POST、PUT、DELETE 等。
- **跨域支持**：使用 Flask-CORS 处理跨域请求，适合在开发环境中调试跨域问题。
- **可配置的域名白名单和黑名单**：可以通过环境变量配置允许或禁止访问的目标域名。
- **Docker 部署**：通过 Dockerfile 及 Docker Compose 轻松构建和部署。

## 安装与使用

### 本地运行

#### 克隆项目

```sh
git clone https://github.com/Dreace/cors-proxy.git
cd cors-proxy
```

#### 安装依赖

```sh
pip install -r requirements.txt
pip gunicorn
```

#### 运行服务

```sh
gunicorn -b 0.0.0.0:5000 cors_proxy:app
```

### 使用 Docker 构建

#### 克隆项目

```sh
git clone https://github.com/Dreace/cors-proxy.git
cd cors-proxy
```

#### 构建 Docker 镜像

```sh
docker build -t cors-proxy .
```

#### 运行 Docker 容器

```sh
docker run -d -p 5000:5000 --name cors-proxy-container cors-proxy
```

### 使用 Docker Compose

直接使用 Docker Compose 启动

```sh
docker-compose up -d
```

### 环境变量配置

- `PROXY_TIMEOUT`：请求超时时间，单位为秒，默认 `30`。
- `PROXY_WHITE_LIST`：允许访问的域名列表，多个域名用逗号分隔。
- `PROXY_BLACK_LIST`：禁止访问的域名列表，多个域名用逗号分隔。

## GitHub Actions 自动构建

项目中提供了 GitHub Actions 工作流配置 (`.github/workflows/docker-image.yml`)，可在代码推送至 `main` 分支时，自动构建 Docker 镜像并推送至 GitHub Container Registry。

## 示例请求

可以通过以下方式访问代理

```sh
curl -X GET "http://localhost:5000/http://example.com"
```

这将把你的请求代理到 `http://example.com` 并返回响应。

---

# CORS Proxy

## Introduction

This project is a CORS proxy server built using Python and Flask, and deployed through a Docker image. It handles cross-origin requests and supports various HTTP methods like GET, POST, PUT, DELETE. It also provides configurable whitelists and blacklists to control which target domains are allowed or denied.

## Features

- **Support for various HTTP methods**: Including GET, POST, PUT, DELETE, etc.
- **CORS support**: Uses Flask-CORS to handle cross-origin requests, useful for debugging CORS issues in development.
- **Configurable whitelist and blacklist**: Domains can be controlled through environment variables.
- **Docker deployment**: Easily build and deploy with Dockerfile and Docker Compose.

## Installation & Usage

### Local Running

#### Clone the repository

```sh
git clone https://github.com/Dreace/cors-proxy.git
cd cors-proxy
```

#### Install dependencies

```sh
pip install -r requirements.txt
pip install gunicorn
```

#### Run the service

```sh
gunicorn -b 0.0.0.0:5000 cors_proxy:app
```

### Build using Docker

#### Clone the repository

```sh
git clone https://github.com/Dreace/cors-proxy.git
cd cors-proxy
```

#### Build the Docker image

```sh
docker build -t cors-proxy .
```

#### Run the Docker container

```sh
docker run -d -p 5000:5000 --name cors-proxy-container cors-proxy
```

### Use Docker Compose

Start directly with Docker Compose

```sh
docker-compose up -d
```

### Environment Variables

- `PROXY_TIMEOUT`: Request timeout in seconds, default is `30`.
- `PROXY_WHITE_LIST`: List of allowed domains, separated by commas.
- `PROXY_BLACK_LIST`: List of blocked domains, separated by commas.

## GitHub Actions for Automated Builds

The project includes a GitHub Actions workflow configuration (`.github/workflows/docker-image.yml`) to automatically build Docker images and push them to the GitHub Container Registry when code is pushed to the `main` branch.

## Example Request

You can make a request through the proxy as follows:

```sh
curl -X GET "http://localhost:5000/http://example.com"
```

This will proxy your request to `http://example.com` and return the response.

