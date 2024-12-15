import base64
import io
import json
import os
import boto3
from PIL import Image

# 選択したAWSリージョンでBedrock Runtimeクライアントを作成する
boto3_bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# モデルIDをStable Diffusion XL 1に設定する
modelId = "stability.stable-diffusion-xl-v1"

# プロンプトを設定する
prompt = "綺麗な山の風景"
negative_prompts = [
    "レンダリングが不十分",
    "背景の詳細が不十分",
    "形が崩れた",
]

# パラメータを設定する
width = 768
cfg_scale = 5
clip_guidance_preset = "FAST_GREEN" 
sampler = "K_DPMPP_2S_ANCESTRAL" 
seed = 42
steps = 60
style_preset = "photographic"

# モデルのネイティブ構造に従ってリクエストペイロードをフォーマットする
request = json.dumps({
    "text_prompts": (
        [{"text": prompt, "weight": 1.0}]
        + [{"text": negprompt, "weight": -1.0} for negprompt in negative_prompts]
    ),
    "width": width,
	"cfg_scale": cfg_scale,
  	"clip_guidance_preset": clip_guidance_preset,
	"sampler": sampler,
    "seed": seed,
    "steps": steps,
    "style_preset": style_preset,
})

# リクエストを送信して、レスポンスを受け取る
response = boto3_bedrock.invoke_model(body=request, modelId=modelId)

# 画像データを抽出する
response_body = json.loads(response.get("body").read())
base_64_img_str = response_body["artifacts"][0].get("base64")
image = Image.open(io.BytesIO(base64.decodebytes(bytes(base_64_img_str, "utf-8"))))

# 保存ファイル名を作成する
i, output_dir = 1, "data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
while os.path.exists(os.path.join(output_dir, f"stability_{i}.png")):
    i += 1
image_path = os.path.join(output_dir, f"stability_{i}.png")

# 画像をファイルに保存する
image.save(image_path)