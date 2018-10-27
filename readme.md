restful_api
===

### 介绍
    restful_api是关于restful API的实践使用，用flask实践开发一个restful API的实际案例
    
    
### 关于RESTful API
    RESTful:  URL定位资源，用HTTP动词（GET,POST,PUT,DELETE)描述操作  
    POST,DELETE,PUT,GET分别对应增删改查
    Resource：资源，即数据。  Representational：某种表现形式，比如用JSON，XML，JPEG等；
    State Transfer：状态变化。通过HTTP动词（GET,POST,PUT,DELETE）实现
    
    
### RESTful API使用场景
    在当今的互联网应用的前端展示媒介很丰富。有手机、有平板电脑还有PC以及其他的展示媒介。
    那么这些前端接收到的用户请求统一由一个后台来处理并返回给不同的前端肯定是最科学和最经济的方式，
    RESTful API就是一套协议来规范多种形式的前端和同一个后台的交互方式。
    RESTful API由后台也就是SERVER来提供前端来调用。
    前端调用API向后台发起HTTP请求，后台响应请求将处理结果反馈给前端。
    也就是说RESTful 是典型的基于HTTP的协议


### RESTful API的设计原则和原则
* 资源: 一段文本，一张图片或者一首歌曲，eg: txt、html、png、jpg、json
* 统一接口: RESTful风格的数据元操CRUD分别对应HTTP方法：GET获取资源，POST新建资源（更新资源），PUT更新资源，DELETE删除资源
* URI: 可以用一个URI（统一资源定位符）指向资源，即每个URI都对应一个特定的资源  最典型的URI是URL
* 无状态: 所有的资源都可以URI定位，而且这个定位与其他资源无关，也不会因为其他资源的变化而变化
* 版本号: 将版本号放入URL or HTTP头信息中
* URL中只能有名词而不能有动词，操作的表达是使用HTTP的动词GET,POST,PUT,DELETEL。URL只标识资源的地址
* 如果记录数量很多，服务器不可能都将它们返回给用户。API应该提供参数，过滤返回结果

 
### HTTP状态码都是有意义的
* 400 -> 请求参数错误 401 -> 未授权 403 -> 禁止访问 404 -> 没有找到资源或页面
* 500 -> 服务器产生位置错误
* 200 -> 查询成功 201 -> 创建或更新成功 204 -> 删除成功
* 301 302

 
### API返回信息分类
* 业务数据信息:        例如物品的基本信息，例如标题、分类、描述、图片等
* 操作成功提示信息:    删除是否成功、新增是否成功等                                                           在utils下的error.py中实现
* 错误异常信息:        资源不存在  格式: {"msg": "xxx", "error_code": 1000, "request": HTTPMethod url}       在utils下的error.py中实现
* 以上所以内容都是json格式


