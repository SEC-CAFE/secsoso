# secsoso
SECSOSO，中文称为安全搜搜，是一个AI驱动的网络安全内容聚合搜索引擎。它基于互联网元搜索引擎、安全知识库、大模型、RAG等技术构建，旨在为网络安全领域提供精准的内容检索和问答服务。SECSOSO通过整合大量的安全知识库和搜索引擎结果，利用RAG技术与大模型相结合，为用户提供网络安全知识、最新漏洞情报、工具、论文等资源的一键获取服务。

#### 功能特点
* 网络安全知识检索：用户可以通过SECSOSO快速检索到网络安全相关的知识、信息和解决方案。
* 最新漏洞情报获取：提供最新的网络安全漏洞情报，帮助用户及时了解和防范安全威胁。
* 工具和资源下载：用户可以找到并下载各种网络安全相关的工具和资源。
* 论文和研究报告：提供网络安全领域的学术论文和研究报告，支持学术研究和深入学习。
使用体验

SECSOSO的网址是 [https://secsoso.com](https://secsoso.com)，用户可以通过这个网址访问SECSOSO，体验其提供的网络安全内容搜索和AI助手服务。SECSOSO致力于为用户提供一个高效、便捷的网络安全信息获取平台。

通过SECSOSO，用户可以更加方便地获取到所需的网络安全信息和资源，提高网络安全工作的效率和效果。

> 以上为SECSOSO自动生成结果

### SECSOSO与其他大模型对话或AI搜索引擎的区别

SECSOSO 安全搜搜是针对网络安全领域的AI搜索引擎。

SECSOSO利用RAG技术结合大模型(使用moonshot-v1-8k)，结合私有安全知识库及安全分类搜索引擎的搜索结果，再补充通用的搜索结果(当前使用bing)，并针对网络安全内容类型的(如漏洞)进行prompts优化，理解问题意图真针对性进行RAG处理，输出用户想要的结果。

在通用问题及知识领域，取决于LLM本身知识库及搜素引擎通用结果增强，所以不会有太大差异，但一些针对性的知识或查询，则取决于专用知识库及分类搜索引擎，则会存在明显差异，SECSOSO可以做到更实时、更精确。



具体差异可参考以下对比搜索(截图时间2024/09/12)：
或参考 https://secsoso.com/about#how_to_search

#### 查询最新漏洞
##### SECSOSO 
![最新漏洞_secsoso](imgs/最新漏洞_secsoso.jpg)
##### chatgpt 
![最新漏洞_chatgpt](imgs/最新漏洞_chatgpt.jpg)
##### metaso 
![最新漏洞_metaso](imgs/最新漏洞_metaso.jpg)

#### wordpress漏洞
##### SECSOSO 
![wordpress漏洞_secsoso](imgs/wordpress漏洞_secsoso.jpg)
##### chatgpt 
![wordpress漏洞_chatgpt](imgs/wordpress漏洞_chatgpt.jpg)
##### metaso 
![wordpress漏洞_metaso](imgs/wordpress漏洞_metaso.jpg)

#### 专有知识库查询AI安全应用
##### SECSOSO 
![AI安全应用_secsoso](imgs/AI安全应用_secsoso.jpg)
##### chatgpt 
![AI安全应用_chatgpt](imgs/AI安全应用_chatgpt.jpg)
##### metaso 
![AI安全应用_metaso](imgs/AI安全应用_metaso.jpg)

#### 渗透测试工具
##### SECSOSO 
![渗透测试工具_secsoso](imgs/渗透测试工具_secsoso.jpg)
##### chatgpt 
![渗透测试工具_chatgpt](imgs/渗透测试工具_chatgpt.jpg)
##### metaso 
![渗透测试工具_metaso](imgs/渗透测试工具_metaso.jpg)

#### ctf工具
##### SECSOSO 
![ctf工具_secsoso](imgs/ctf工具_secsoso.jpg)
##### chatgpt 
![ctf工具_chatgpt](imgs/ctf工具_chatgpt.jpg)
##### metaso 
![ctf工具_metaso](imgs/ctf工具_metaso.jpg)


