import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # チャットメッセージコンテナにユーザーのメッセージを表示する
    await cl.Message(
        content=f"Received: {message.content}",
    ).send()