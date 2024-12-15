import base64
import io
import json
import os
import boto3
from PIL import Image

def image_to_base64(img) -> str:
    '''PIL画像またはローカルの画像ファイルパスをbase64文字列に変換する'''
    if isinstance(img, str):
        if os.path.isfile(img):
            print(f"ファイルパスから画像を読み込む: {img}")
            with open(img, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        else:
            raise FileNotFoundError(f"File {img} does not exist")
    elif isinstance(img, Image.Image):
        print("PIL画像からbase64文字列に変換する")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    else:
        raise ValueError(f"画像ファイルパスまたはPIL画像を指定してください。")

# 選択したAWSリージョンでBedrock Runtimeクライアントを作成する
boto3_bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# モデルIDをStable Diffusion XL 1に設定する
modelId = "stability.stable-diffusion-xl-v1"

# パラメータを設定する
width = 768
cfg_scale = 5
clip_guidance_preset = "FAST_GREEN" 
sampler = "K_DPMPP_2S_ANCESTRAL" 
seed = 42
steps = 60
style_preset = "photographic"

# ファイルパスを指定して画像を読み込む
init_image_b64 = image_to_base64("data/stability_1.png")

# 画像編集プロンプトを設定する
change_prompt = "道に沿って歩く人々を追加する"

# モデルのネイティブ構造に従ってリクエストペイロードをフォーマットする
request = json.dumps({
    "text_prompts": (
        [{"text": change_prompt, "weight": 1.0}]
    ),
    "cfg_scale": cfg_scale,
    "init_image": init_image_b64,
    "seed": seed,
    "steps": steps,
    "style_preset": style_preset,
    "clip_guidance_preset": clip_guidance_preset,
    "sampler": sampler,
})

# リクエストを送信して、レスポンスを受け取る
response = boto3_bedrock.invoke_model(body=request, modelId=modelId)
response_body = json.loads(response.get("body").read())

# 画像データを抽出する
image_b64_str = response_body["artifacts"][0].get("base64")
image = Image.open(io.BytesIO(base64.decodebytes(bytes(image_b64_str, "utf-8"))))

# 画像をファイルに保存する
image.save("data/stability_edit.png")
