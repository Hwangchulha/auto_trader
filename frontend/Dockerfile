# --- Build stage ---
FROM node:20-slim AS build
WORKDIR /app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN if [ -f pnpm-lock.yaml ]; then npm i -g pnpm && pnpm i --frozen-lockfile;         elif [ -f yarn.lock ]; then npm i -g corepack && corepack enable && yarn install --frozen-lockfile;         elif [ -f package-lock.json ]; then npm ci; else npm i; fi
COPY . /app
RUN npm run build

# --- Runtime stage ---
FROM node:20-slim
WORKDIR /app
# Copy Next standalone output
COPY --from=build /app/.next/standalone ./
COPY --from=build /app/.next/static ./.next/static
# Copy public assets (may be empty)
RUN mkdir -p /app/public
COPY --from=build /app/public ./public
EXPOSE 3000
CMD ["node","server.js"]
