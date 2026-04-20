#!/usr/bin/env python3
"""Batch Processing - process multiple commits with cost aggregation."""
from costs.calculator import ai_cost

# Simulated batch of commits
commits = [
    {
        "hash": "abc1234",
        "message": "Fix authentication bug",
        "diff": '''diff --git a/auth.py b/auth.py
--- a/auth.py
+++ b/auth.py
@@ -10,7 +10,7 @@
 def login(username, password):
     user = db.get_user(username)
-    if user.password == password:
+    if bcrypt.checkpw(password.encode(), user.password_hash):
         return generate_token(user)
     return None
'''
    },
    {
        "hash": "def5678",
        "message": "Add rate limiting",
        "diff": '''diff --git a/middleware.py b/middleware.py
--- a/middleware.py
+++ b/middleware.py
@@ -1,5 +1,15 @@
+from redis import Redis
+
 class RateLimiter:
+    def __init__(self, redis_client: Redis):
+        self.redis = redis_client
+    
+    def is_allowed(self, key: str, max_requests: int = 100) -> bool:
+        current = self.redis.incr(f"rate_limit:{key}")
+        if current == 1:
+            self.redis.expire(f"rate_limit:{key}", 3600)
+        return current <= max_requests
'''
    },
    {
        "hash": "ghi9012",
        "message": "Update API documentation",
        "diff": '''diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -20,6 +20,12 @@
 ## API Endpoints
 
+### POST /api/v1/users
+Create a new user account.
+
+**Request:**
+- `email` (required): User email address
+- `name` (required): User full name
+- `role` (optional): User role (default: 'user')
'''
    }
]


if __name__ == "__main__":
    print("=" * 70)
    print("API Example: Batch Processing")
    print("=" * 70)

model = "claude-3.5-sonnet"
total_cost = 0
total_tokens = 0

    print(f"\nModel: {model}\n")
    print(f"{'Commit':<10} {'Message':<25} {'Tokens':>8} {'Cost':>12}")
    print("-" * 70)

for commit in commits:
    result = ai_cost(
        commit_diff=commit["diff"],
        model=model
    )
    
    total_cost += result["cost"]
    total_tokens += result["tokens"]["total"]
    
    print(f"{commit['hash']:<10} {commit['message']:<25} "
          f"{result['tokens']['total']:>8} ${result['cost']:>10.6f}")

    print("-" * 70)
    print(f"{'TOTAL':<36} {total_tokens:>8} ${total_cost:>10.6f}")

    print(f"\nValue generated: ${total_cost * 100:.2f} (100x ROI assumption)")
    print(f"Average per commit: ${total_cost / len(commits):.6f}")
