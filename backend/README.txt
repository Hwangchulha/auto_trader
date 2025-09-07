Dual-router frontend patch for /keys:

Copy the folder contents into your FRONTEND project root.
- If your project uses App Router: ensure file exists at app/keys/page.tsx
- If your project uses Pages Router: ensure file exists at pages/keys.tsx

Then rebuild the frontend:
  docker compose up -d --build frontend
or
  npm run build && npm start  (if you run it locally)

Open: http://localhost:3000/keys  (or http://<server-ip>:3000/keys)
