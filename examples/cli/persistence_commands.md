# Persistence CLI Commands

## Quick Reference

```bash
# Check database connectivity
shadowbot persistence doctor \
  --conversation-url postgresql://localhost:5432/shadowbot \
  --state-url redis://localhost:6379

# Run agent with persistence
shadowbot persistence run \
  --conversation-url postgresql://localhost:5432/shadowbot \
  --session-id my-session

# Resume a session
shadowbot persistence resume \
  --conversation-url postgresql://localhost:5432/shadowbot \
  --session-id my-session

# Export session to file
shadowbot persistence export \
  --conversation-url postgresql://localhost:5432/shadowbot \
  --session-id my-session \
  --output session_backup.jsonl

# Import session from file
shadowbot persistence import \
  --conversation-url postgresql://localhost:5432/shadowbot \
  --file session_backup.jsonl

# Check schema status
shadowbot persistence status \
  --conversation-url postgresql://localhost:5432/shadowbot \
  --state-url redis://localhost:6379

# Apply migrations
shadowbot persistence migrate \
  --conversation-url postgresql://localhost:5432/shadowbot \
  --state-url redis://localhost:6379
```

## Environment Variables

Instead of CLI flags, you can use environment variables:

```bash
export PRAISON_CONVERSATION_URL=postgresql://localhost:5432/shadowbot
export PRAISON_STATE_URL=redis://localhost:6379
export PRAISON_KNOWLEDGE_URL=http://localhost:6333

# Then run without URL flags
shadowbot persistence doctor
shadowbot persistence status
```

## Docker Setup

```bash
# Start all services
docker run -d --name praison-postgres \
  -e POSTGRES_PASSWORD=praison123 \
  -e POSTGRES_DB=shadowbot \
  -p 5432:5432 postgres:16

docker run -d --name praison-redis \
  -p 6379:6379 redis:7

docker run -d --name praison-qdrant \
  -p 6333:6333 -p 6334:6334 qdrant/qdrant

# Verify
docker ps
```

## Example Workflow

```bash
# 1. Start services
docker-compose up -d

# 2. Check connectivity
shadowbot persistence doctor

# 3. Run agent
shadowbot persistence run --session-id demo-session

# 4. Export for backup
shadowbot persistence export --session-id demo-session --output backup.jsonl

# 5. Import to another environment
shadowbot persistence import --file backup.jsonl
```
