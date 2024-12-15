import json
import tiktoken
import numpy as np
from collections import defaultdict

# データファイルの読み込み
data_path = "data.jsonl"
with open(data_path) as f:
  dataset = [json.loads(line) for line in f]

print("データサンプル数:", len(dataset))
print("最初のデータサンプル:")
for message in dataset[0]["messages"]:
  print(message)

# フォーマットチェック
format_errors = defaultdict(int)

for ex in dataset:
  if not isinstance(ex, dict):
    format_errors["data_type"] += 1
    continue

  messages = ex.get("messages", None)
  if not messages:
    format_errors["missing_messages_list"] += 1
    continue

  for message in messages:
    if "role" not in message or "content" not in message:
      format_errors["message_missing_key"] += 1

    if any(k not in ("role", "content", "name") for k in message):
      format_errors["message_unrecognized_key"] += 1

    if message.get("role", None) not in ("system", "user", "assistant"):
      format_errors["unrecognized_role"] += 1

    content = message.get("content", None)
    if not content or not isinstance(content, str):
      format_errors["missing_content"] += 1

  if not any(message.get("role", None) == "assistant" for message in messages):
    format_errors["example_missing_assistant_message"] += 1

if format_errors:
  print("エラーが見つかりました:")
  for k, v in format_errors.items():
      print(f"{k}: {v}")
else:
  print("エラーが見つかりませんでした。")

# トークン数カウント
encoding = tiktoken.get_encoding("cl100k_base")

def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
  num_tokens = 0
  for message in messages:
    num_tokens += tokens_per_message
    for key, value in message.items():
      num_tokens += len(encoding.encode(value))
      if key == "name":
        num_tokens += tokens_per_name
  num_tokens += 3
  return num_tokens

def num_assistant_tokens_from_messages(messages):
  num_tokens = 0
  for message in messages:
    if message["role"] == "assistant":
      num_tokens += len(encoding.encode(message["content"]))
  return num_tokens

def print_distribution(values, name):
  print(f"\n#### Distribution of {name}:")
  print(f"min / max: {min(values)}, {max(values)}")
  print(f"mean / median: {np.mean(values)}, {np.median(values)}")
  print(f"p5 / p95: {np.quantile(values, 0.1)}, {np.quantile(values, 0.9)}")

n_missing_system = 0
n_missing_user = 0
n_messages = []
convo_lens = []
assistant_message_lens = []

for ex in dataset:
  messages = ex["messages"]
  if not any(message["role"] == "system" for message in messages):
    n_missing_system += 1
  if not any(message["role"] == "user" for message in messages):
    n_missing_user += 1
  n_messages.append(len(messages))
  convo_lens.append(num_tokens_from_messages(messages))
  assistant_message_lens.append(num_assistant_tokens_from_messages(messages))

print("system メッセージが欠落しているサンプル数:", n_missing_system)
print("user メッセージが欠落しているサンプル数:", n_missing_user)
print_distribution(n_messages, "num_messages_per_example")
print_distribution(convo_lens, "num_total_tokens_per_example")
print_distribution(assistant_message_lens, "num_assistant_tokens_per_example")
n_too_long = sum(l > 4096 for l in convo_lens)
print(f"\n{n_too_long} データサンプルが 4096 トークン制限を超えている可能性があります。ファインチューニング中に切り捨てられます。")

# 価格設定とデフォルトのn_epochs推定
MAX_TOKENS_PER_EXAMPLE = 4096

MIN_TARGET_EXAMPLES = 100
MAX_TARGET_EXAMPLES = 25000
TARGET_EPOCHS = 3
MIN_EPOCHS = 1
MAX_EPOCHS = 25

n_epochs = TARGET_EPOCHS
n_train_examples = len(dataset)
if n_train_examples * TARGET_EPOCHS < MIN_TARGET_EXAMPLES:
  n_epochs = min(MAX_EPOCHS, MIN_TARGET_EXAMPLES // n_train_examples)
elif n_train_examples * TARGET_EPOCHS > MAX_TARGET_EXAMPLES:
  n_epochs = max(MIN_EPOCHS, MAX_TARGET_EXAMPLES // n_train_examples)

n_billing_tokens_in_dataset = sum(min(MAX_TOKENS_PER_EXAMPLE, length)
                                  for length in convo_lens)
print(f"データセットには、約 {n_billing_tokens_in_dataset} トークンが含まれています。")
print(f"デフォルトでは、このデータセットで {n_epochs} エポックのトレーニングが行われます。")
print(f'デフォルトでは、約 {n_epochs * n_billing_tokens_in_dataset} トークンに対して請求されます。')
print(f'コストを見積もるには、価格ページを参照してください。')