from app.llm import parse_preferences
from app.recommender import recommend

# 測試 LLM 解析
user_input = "我想要不酸、帶點巧克力味，喝起來要很有重量感"
print("用戶輸入：", user_input)

prefs = parse_preferences(user_input)
print("解析結果：", prefs)

# 把 LLM 解析的偏好丟給 ML 推薦
results = recommend(prefs, top_n=3)
print("\n推薦結果：")
for r in results:
    print(f"  {r['name']} - 相似度 {r['score']}%")