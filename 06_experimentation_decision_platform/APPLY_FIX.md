# Docker import fix

Replace the project-root `Dockerfile` and `pyproject.toml` with the supplied files.

Then run:

```bash
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up
```

Verify the package inside the image:

```bash
docker compose run --rm api python -c \
  "import experimentation; print(experimentation.__file__)"
```

Verify the API:

```bash
curl http://127.0.0.1:8000/health
```
