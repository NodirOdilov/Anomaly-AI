# syntax=docker/dockerfile:1.7
# === Build stage: компилируем Vite в статический dist ===
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund || npm install --no-audit --no-fund

COPY . .
RUN npm run build


# === Runtime stage: nginx раздаёт статические файлы ===
FROM nginx:1.27-alpine AS runtime

# Кастомная конфигурация: SPA fallback на index.html, агрессивное кеширование Vite-ассетов.
RUN rm /etc/nginx/conf.d/default.conf
COPY <<'EOF' /etc/nginx/conf.d/anomaly.conf
server {
    listen 5173;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 5173

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q -O - http://localhost:5173/ > /dev/null || exit 1

CMD ["nginx", "-g", "daemon off;"]
