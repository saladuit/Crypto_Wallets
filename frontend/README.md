Frontend (Vite + React)
=========================

Quick steps to run the frontend locally while developing against the FastAPI backend.

Development (with proxy)
- Install dependencies:
  ```bash
  cd frontend
  npm install
  ```
- Start the Vite dev server (proxy configured for `/api` -> `http://127.0.0.1:8000`):
  ```bash
  npm run dev
  ```

The app will be available at the Vite URL (usually `http://localhost:5173`).
When the frontend calls `/api/wallets` the dev server will proxy that to
`http://127.0.0.1:8000/wallets`.

Production (build + serve with backend)
- Build the frontend:
  ```bash
  cd frontend
  npm run build
  ```
- The built files will be in `frontend/dist`. The backend is already configured
  to serve `frontend/dist` at `/` when present. Start the backend and visit
  `http://127.0.0.1:8000`.
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

Add UI Form: implement an “Add wallet” form in Wallets.jsx to POST new wallets.
Wire Update/Delete: add buttons and handlers to update and delete wallets from the UI.
Pagination/Filtering: add query params and backend support for paging or filtering by address/currency.
Polish & Errors: show friendly error messages, loading states, and a success toast.
Test & Docs: add a simple integration test or update README with exact dev/run commands.