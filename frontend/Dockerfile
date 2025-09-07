FROM node:20-slim

WORKDIR /app
ENV NODE_ENV=production

COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN if [ -f pnpm-lock.yaml ]; then npm i -g pnpm && pnpm i --frozen-lockfile;     elif [ -f yarn.lock ]; then yarn install --frozen-lockfile;     elif [ -f package-lock.json ]; then npm ci;     else npm i; fi

COPY . /app

EXPOSE 3000
CMD ["npm","run","start"]
