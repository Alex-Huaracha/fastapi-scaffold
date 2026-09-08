set -euo pipefail

docker compose up --build -d --wait

echo
echo "API:   http://localhost:8000"
echo "Docs:  http://localhost:8000/docs"
echo
echo "Logs:  docker compose logs -f api"
echo "Stop:  docker compose down"