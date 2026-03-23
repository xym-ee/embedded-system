


随便用用，

正经用用。


提示词
>用 Electron 做一个知识库应用，窗口左边是文档列表区域，右边是问答面板区域，应用需要创建并使用本地数据目录。


[claude ](https://github.com/2025Emma/vibe-coding-cn)

https://zread.ai/tukuaiai/vibe-coding-cn/4-tool-ecosystem-primer


## 设计文档

>我想设计一个用于小团队的，内网使用的项目管理工具，基于web呈现。先帮我写一个设计文档，文件名为 design-doc.md

生成文档，修改，

/init  生成全局记忆

>基于现有内容，给我一份详细的实施计划，文件保存为 plan.md。每一步要小且具体，严禁包含代码，只写清晰具体地指令即可。


新开会话。

>阅读所有文档，项目要求是否清晰，还有什么问题需要澄清？

● 让我先阅读项目中的关键文档。                                                                                                                    
  Searched for 3 patterns, read 2 files (ctrl+o to expand)     

● 文档很完整，我已阅读 design-doc.md 和 plan.md。项目要求基本清晰，但有几个细节需要确认：
                                                                                                                                                         
  需要澄清的问题：                                      
                                                                                                                                                         
  1. 项目成员管理 API 缺失                                                                                                                               
  数据模型中有 ProjectMember 表（关联项目和用户），但 API 设计中没有项目成员管理的接口（POST                                                             
  /api/projects/:id/members）。是否需要这个功能？还是说项目创建者自动成为唯一成员，其他成员通过任务指派来参与？                                          
  1. 全局任务列表 
  前端 /tasks 页面需要展示所有任务，但后端只提供了 GET /api/projects/:id/tasks（按项目获取）。是否有必要新增 GET /api/tasks                              
  全局接口？还是前端通过调用多个项目接口自己聚合？                                                                                                       
  1. JWT Refresh Token                                                                                                                                   
  设计文档提到"支持 refresh"，但 plan 中只实现了 access_token（24小时）。是否需要实现 refresh token 机制？                                               
  1. admin vs owner 角色混淆                                                                                                                             
    - User.role（admin/member）— 系统级角色                                                                                                              
    - ProjectMember.role（owner/member）— 项目级角色                                                                                                     
  这两个维度的权限如何配合？例如：普通 member 能否创建项目？非 owner 的 admin 能否删除项目？                                                             
  1. 项目归档后的行为                                                                                                                                    
  归档（archived）的项目是否还能编辑任务？是否还能在看板中显示？                                                                                         
                                                                                                                                                         
  这些问题会影响 API 设计和前端逻辑，请确认一下。


> 1.项目创建者为唯一成员  
> 2.可以新增全局接口                                                                                                                                     
> 3.需要实现                                                                                                                                             
> 4.admin有所有权限，任意修改。普通member也可以创建项目                                                                                                  
> 5.归档不可编辑，能在看板中显示

明白了，项目要求现在完全清晰。让我更新 plan.md 来反映这些决策。




>我想开发一个个人博客，平时使用markdown写作，然后自动套用样式生成网页内容。帮我写一个设计文档，名为design-doc.md



