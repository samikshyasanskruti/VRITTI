# CareerMatch AI Frontend

Professional React + Vite frontend for the existing CareerMatch AI FastAPI backend.

## Start locally

1. Open a terminal in this `frontend` folder.
2. Install dependencies:
   ```powershell
   npm install
   ```
3. Create `.env` from `.env.example` if you need a different API address:
   ```env
   VITE_API_BASE_URL=http://127.0.0.1:8000
   ```
4. Start Vite:
   ```powershell
   npm run dev
   ```
5. Keep the backend running at port 8000 and open the URL Vite prints (usually http://localhost:5173).

## Build for production

```powershell
npm run build
```

## Backend routes used

- `GET /api/health`
- `GET /api/resume`
- `GET /api/resume/{resume_id}`
- `POST /api/resume/upload`
- `GET /api/jobs`
- `POST /api/matching/run`
- `GET /api/recommendations`
- `POST /api/simulator/what-if`
- `POST /api/roadmap`
- `POST /api/recruiter/rank-candidates`

The career chat and measured model evaluation screens explicitly disclose that the current backend does not expose those endpoints/metrics. The `src/data/demo*.js` exports are empty by design: no synthetic candidates, opportunities, or scores are shown.
