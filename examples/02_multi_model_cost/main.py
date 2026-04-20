#!/usr/bin/env python3
"""Multi-Model Cost Comparison - compare costs across providers."""
from costs.calculator import estimate_tokens, calculate_cost

# Sample git diff (realistic code review scenario)
sample_diff = '''diff --git a/src/api/routes.py b/src/api/routes.py
index 1a2b3c..4d5e6f 100644
--- a/src/api/routes.py
+++ b/src/api/routes.py
@@ -45,12 +45,25 @@ async def create_user(request: Request):
     data = await request.json()
     
     # Validate input
-    if not data.get('email'):
-        raise HTTPException(400, "Email required")
+    required_fields = ['email', 'name', 'role']
+    for field in required_fields:
+        if not data.get(field):
+            raise HTTPException(400, f"{field} is required")
     
     # Check if user exists
     existing = await db.users.find_one({"email": data['email']})
     if existing:
         raise HTTPException(409, "User already exists")
     
-    user = await db.users.insert_one(data)
-    return {"id": str(user.inserted_id)}
+    # Hash password if provided
+    if 'password' in data:
+        data['password_hash'] = bcrypt.hashpw(
+            data['password'].encode(),
+            bcrypt.gensalt()
+        )
+        del data['password']
+    
+    user = await db.users.insert_one(data)
+    return {
+        "id": str(user.inserted_id),
+        "created_at": datetime.utcnow().isoformat()
+    }
'''


if __name__ == "__main__":
    print("=" * 70)
    print("API Example: Multi-Model Cost Comparison")
    print("=" * 70)

# Models to compare
models = [
    ("openai/gpt-4o", "GPT-4o"),
    ("anthropic/claude-3.5-sonnet", "Claude 3.5 Sonnet"),
    ("anthropic/claude-3.5-haiku", "Claude 3.5 Haiku"),
    ("openrouter/qwen/qwen3-coder-next", "Qwen3 Coder Next"),
    ("openai/gpt-5.4-mini", "GPT-4o Mini"),
]

    print(f"\nSample diff: {len(sample_diff)} characters")
    print(f"Added lines: ~20, Deleted lines: ~8\n")

    print(f"{'Model':<30} {'Input':>8} {'Output':>8} {'Cost':>12}")
    print("-" * 70)

for model_id, model_name in models:
    # Estimate tokens
    tokens = estimate_tokens(sample_diff, model_id)
    
    # Calculate cost
    cost = calculate_cost(tokens, model_id)
    
    print(f"{model_name:<30} {tokens['input']:>8} {tokens['output']:>8} ${cost:>10.6f}")

    print("-" * 70)
    print("\nNote: Costs calculated using actual tokenizers (tiktoken, anthropic)")
    print("Output tokens estimated based on added lines (30 tokens per line heuristic)")
