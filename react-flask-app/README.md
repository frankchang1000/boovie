# React-Flask-App Navigation

## AI modules
Backend functionality is located under the `modules` directory. The functions are routed through `app.py` and are called by the frontend. The output from the modules are stored under `data` directory.

On the first call, the `data` directory will create `books`, `summary`, `scripts`, `images`, `captions`, and `videos` directories if they don't exist.

## Frontend
The frontend is built using React and Mantine components. The components are located under the `src` directory. The main page is `App.js` and the components are stored under `components` directory.