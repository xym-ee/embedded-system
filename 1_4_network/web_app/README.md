
# 现代 web 应用


hugo 静态网站生成器。

markdown 写好后，hugo 生成为 html，得到一堆静态文件。

浏览器打开就能看到页面。这类网站通常无复杂交互
- 登录，评论，实时聊天，传文件，数据库存储

把内容提前做成网页。


## 前端是什么？

前端 = 运行在用户浏览器里的部分。

主要是三样
- HTML
- CSS
- JavaScript

结构、样式、交互。

HTML 骨架，CSS 外观，JS 行为

```html
<button>点击我</button>
```

让按钮变好看
```css
button {
  color: white;
  background: blue;
}
```

js 让按钮能干事
```js
document.querySelector("button").onclick = () => {
  alert("你点了按钮");
};
```

## 后端是什么？

后端 = 运行在服务器上的程序。

处理登录，查数据库，权限，生成接口，给前端返回数据。

浏览器 → 请求服务器 → 服务器查数据库 → 返回数据 → 浏览器显示

后端常见语言和框架：

| 语言                      | 常见后端框架                 |
| ----------------------- | ---------------------- |
| Python                  | FastAPI, Django, Flask |
| JavaScript / TypeScript | Express, NestJS        |
| Java                    | Spring Boot            |
| Go                      | Gin, Echo              |
| PHP                     | Laravel                |


## 什么是前后端通信？


前端和后端不是直接“共享变量”的。它们通过网络通信。最常见的是：

```
前端 JS 发送请求
↓
后端 FastAPI 接收请求
↓
后端处理数据
↓
返回 JSON
↓
前端拿到 JSON 后更新页面
```

例如前端请求：
```js
fetch("/api/user/1")
```
后端返回：
```json
{
  "id": 1,
  "name": "Alice",
  "age": 18
}
```
这就是前后端通信。

## 什么是 API ？

API 可以理解成后端暴露给前端使用的“功能入口”。


比如后端提供这些接口：

GET  /api/articles        获取文章列表
GET  /api/articles/1      获取某篇文章
POST /api/articles        新建文章
DELETE /api/articles/1    删除文章

前端不需要知道数据库怎么查，只需要调用这些接口。

这就是所谓：

前端负责展示
后端负责数据和逻辑
API 负责连接两边




6. 什么是 HTTP？

HTTP 是浏览器和服务器通信最常用的协议。

你访问网页时：

https://example.com

本质上就是浏览器发 HTTP 请求。

常见 HTTP 方法：

方法	含义
GET	获取数据
POST	提交数据
PUT	整体更新
PATCH	部分更新
DELETE	删除

例如：

GET /api/users

意思是：我要获取用户列表。

POST /api/login

意思是：我要提交登录信息。






















