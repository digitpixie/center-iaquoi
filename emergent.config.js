module.exports = {
  routes: [
    {
      path: "/api/*",
      destination: "backend"
    },
    {
      path: "/*",
      destination: "frontend"
    }
  ],
  services: {
    backend: {
      port: 8001,
      build: "cd backend && pip install -r requirements.txt",
      start: "cd backend && python server.py"
    },
    frontend: {
      port: 3000,
      build: "cd frontend && yarn install && yarn build",
      start: "cd frontend && yarn start"
    }
  }
};