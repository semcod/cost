# AI Cost Badge Service

Standalone PHP service for generating AI cost badges for repositories.

## Installation

```bash
cd services/badge-service
composer install
php -S localhost:8080
```

### Generate badge from cost
```
GET /badge.php?cost=12.34&model=claude-4&commits=42
```

### Analyze repository
```
GET /badge.php?repo=github.com/user/repo
```

### API endpoint
```bash
curl -X POST http://localhost:8080/badge.php \
  -H "Content-Type: application/json" \
  -d '{"cost": 12.34, "model": "claude-4", "commits": 42}'
```

## Badge Colors

- Green: Cost < $1
- Yellow: $1-5
- Orange: $5-10
- Red: $10+

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
API_KEY=your_api_key
ALLOWED_ORIGINS=*
CACHE_TTL=3600
```
