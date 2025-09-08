FROM node:20-slim

WORKDIR /app
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN if [ -f pnpm-lock.yaml ]; then npm i -g pnpm && pnpm i --frozen-lockfile;     elif [ -f yarn.lock ]; then npm i -g corepack && corepack enable && yarn install --frozen-lockfile;     elif [ -f package-lock.json ]; then npm ci;     else npm i; fi

COPY . /app
RUN npm run build

EXPOSE 3000
CMD ["node",".next/standalone/server.js"]
