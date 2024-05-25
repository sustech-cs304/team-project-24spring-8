```sh
# 1
cd $WORK_SPACE/backend  
uvicorn main:app --reload --port 8001
# 2
cd ../frontend
npm install
npm run serve
```