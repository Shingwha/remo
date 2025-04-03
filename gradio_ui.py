import gradio as gr
from test import agent

def respond(message, history):
    """处理用户输入并返回AI回复"""
    # 调用agent生成回复
    response = agent.generate(message)
    # 将消息转换为Gradio Chatbot组件要求的格式
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response}
    ]
    # 返回对话结果和更新后的记忆
    return "", history, get_memory()

def clear_context():
    """清空对话上下文"""
    agent.conversation.clear()
    return []

def get_memory():
    """获取当前记忆内容，以列表形式显示"""
    memory_dict = agent.memory_bank.to_dict()
    formatted_memory = []
    
    # 将记忆字典转换为列表形式
    for memory_id, memory in memory_dict.items():
        memory_type = memory.get('type', '未知类型')
        summary = memory.get('summary', '无摘要')
        time = memory.get('time', '未知时间')
        # 格式化每条记忆
        memory_item = f"ID: {memory_id}\n类型: {memory_type}\n摘要: {summary}\n时间: {time}\n"
        formatted_memory.append(memory_item)
    
    # 如果没有记忆，返回提示信息
    if not formatted_memory:
        return "暂无记忆内容"
    
    # 将所有记忆项连接成一个字符串，每项之间用分隔线分开
    return "\n----------\n".join(formatted_memory)

# 创建Gradio界面
with gr.Blocks(title="Remo AI对话助手") as demo:
    with gr.Column(scale=1):
        gr.Markdown("# Remo AI对话助手")
        
        with gr.Row():
            with gr.Column(scale=2):
                # 对话区域
                chatbot = gr.Chatbot(height=600, type="messages")
                with gr.Row():
                    msg = gr.Textbox(
                        label="发送消息",
                        placeholder="在这里输入您的问题...",
                        lines=3,
                        scale=4
                    )
                    with gr.Column(scale=1):
                        submit_btn = gr.Button("发送", variant="primary")
                        clear_btn = gr.Button("清空上下文", variant="secondary")
            
            with gr.Column(scale=1):
                # 记忆展示区域
                gr.Markdown("### 当前记忆")
                memory_display = gr.TextArea(
                    label="记忆内容",
                    interactive=False,
                    value=get_memory(),
                    lines=25
                )
                refresh_memory_btn = gr.Button("刷新记忆", variant="secondary")
    
    # 设置事件处理
    msg.submit(respond, [msg, chatbot], [msg, chatbot, memory_display])
    submit_btn.click(respond, [msg, chatbot], [msg, chatbot, memory_display])
    clear_btn.click(clear_context, [], [chatbot])
    refresh_memory_btn.click(get_memory, [], [memory_display])

# 启动应用
if __name__ == "__main__":
    demo.launch()